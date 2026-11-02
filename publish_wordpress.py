"""Publish the approved InvestBeacon release. GPL-2.0-or-later."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
SLUG = 'investbeacon-investment-calculators'
SVN_URL = 'https://plugins.svn.wordpress.org/' + SLUG


def approved_release(root=ROOT):
    manifest = json.loads((root / 'release.json').read_text())
    version = manifest['version']
    if manifest['slug'] != SLUG or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Invalid release identity.')
    filename = manifest['archive']
    if Path(filename).name != filename or not filename.endswith('.zip'):
        raise ValueError('Invalid archive filename.')
    archive = root / filename
    if hashlib.sha256(archive.read_bytes()).hexdigest() != manifest['sha256']:
        raise ValueError('Archive differs from the approved SHA-256.')
    files = {}
    with ZipFile(archive) as package:
        for item in package.infolist():
            parts = PurePosixPath(item.filename).parts
            if not parts or parts[0] != SLUG or '..' in parts or '\\' in item.filename or item.filename.startswith('/'):
                raise ValueError('Unsafe archive path.')
            if item.is_dir():
                continue
            relative = PurePosixPath(*parts[1:]).as_posix()
            if len(parts) < 2 or relative in files or (item.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('Duplicate, invalid or symlink archive entry.')
            files[relative] = package.read(item)
    main = files[SLUG + '.php'].decode()
    readme = files['readme.txt'].decode()
    block = json.loads(files['block/block.json'])
    if not re.search(r'^ \* Version:\s*' + re.escape(version) + r'\s*$', main, re.M):
        raise ValueError('Plugin version mismatch.')
    if not re.search(r'^Stable tag:\s*' + re.escape(version) + r'\s*$', readme, re.M) or block['version'] != version:
        raise ValueError('Readme/block version mismatch.')
    required = {'LICENSE.txt', SLUG + '.php', 'readme.txt', 'block/block.json', 'assets/beacon.png', 'assets/math.js', 'assets/calculators.js', 'assets/calculators.css', 'assets/editor.js'}
    if set(files) != required:
        raise ValueError('Unexpected release files.')
    return manifest, files


def run_svn(args, cwd=None, password=None):
    command = ['svn', *args, '--non-interactive', '--no-auth-cache']
    if password is not None:
        command += ['--username', 'thankaran', '--password-from-stdin']
    result = subprocess.run(command, cwd=cwd, input=(password + '\n') if password else None,
                            text=True, capture_output=True, timeout=180, check=False)
    output = result.stdout + result.stderr
    if password:
        output = output.replace(password, '[redacted]')
    if result.returncode:
        raise RuntimeError('SVN failed: ' + output[:4000])
    return result.stdout


def read_tree(folder):
    return {p.relative_to(folder).as_posix(): p.read_bytes()
            for p in folder.rglob('*') if p.is_file() and '.svn' not in p.parts}


def stage_release(work, manifest, files):
    trunk = work / 'trunk'
    tag = work / 'tags' / manifest['version']
    if not trunk.is_dir() or not (work / 'tags').is_dir():
        raise ValueError('Unexpected WordPress repository layout.')
    if tag.exists():
        if read_tree(tag) == files:
            return False
        raise ValueError('This version already exists with different bytes; refusing to replace it.')
    existing = read_tree(trunk)
    if existing and existing != files:
        raise ValueError('Trunk contains a different release. Review it before deployment.')
    for name, data in files.items():
        target = trunk / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    run_svn(['add', '--force', 'trunk'], cwd=work)
    run_svn(['copy', 'trunk', 'tags/' + manifest['version']], cwd=work)
    status = ET.fromstring(run_svn(['status', '--xml'], cwd=work))
    for entry in status.findall('.//entry'):
        name = entry.get('path', '').replace('\\', '/')
        if not (name == 'trunk' or name.startswith('trunk/') or name == 'tags/' + manifest['version'] or name.startswith('tags/' + manifest['version'] + '/')):
            raise ValueError('Unexpected changed path: ' + name)
    if read_tree(trunk) != files or read_tree(tag) != files:
        raise ValueError('Staged files do not match the approved archive.')
    return True


def publish(manifest, files):
    password = os.environ.get('SVN_PASSWORD', '')
    if not password or '\n' in password or '\r' in password:
        raise ValueError('Set the SVN_PASSWORD repository secret before publishing.')
    with tempfile.TemporaryDirectory(prefix='investbeacon-svn-') as directory:
        work = Path(directory) / 'working-copy'
        run_svn(['checkout', SVN_URL, str(work)])
        if not stage_release(work, manifest, files):
            print('This exact version is already published; no commit was made.')
            return
        print('Publishing verified release ' + manifest['version'] + ' to WordPress.org.')
        result = run_svn(['commit', 'trunk', 'tags/' + manifest['version'], '-m',
                          'Release InvestBeacon Investment Calculators ' + manifest['version']], cwd=work, password=password)
        print(result)
        export = Path(directory) / 'verified-export'
        run_svn(['export', SVN_URL + '/tags/' + manifest['version'], str(export)])
        if read_tree(export) != files:
            raise RuntimeError('Commit completed but remote byte verification failed; inspect before retrying.')
        print('Remote SVN tag matches all approved source bytes.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true', help='Commit to WordPress.org; otherwise validate only.')
    args = parser.parse_args()
    manifest, files = approved_release()
    print('Validated: ' + SLUG + ' ' + manifest['version'] + ', ' + str(len(files)) + ' runtime files, approved SHA-256.')
    if args.publish:
        publish(manifest, files)
    else:
        print('Validation only. No credentials used and no remote changes made.')


if __name__ == '__main__':
    main()
