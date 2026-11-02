"""Apply a readme-only WordPress.org directory update. GPL-2.0-or-later."""
import os
from pathlib import Path
import tempfile
from publish_wordpress import ROOT, SVN_URL, approved_release, read_tree, run_svn


def main():
    manifest, original = approved_release()
    updated = (ROOT / 'listing-readme.txt').read_bytes()
    if b'Stable tag: 1.0.1\n' not in updated or b'[InvestBeacon](https://investbeacon.eu/)' not in updated:
        raise ValueError('Unexpected listing metadata.')
    expected = dict(original, **{'readme.txt': updated})
    password = os.environ.get('SVN_PASSWORD', '')
    if not password or '\n' in password or '\r' in password:
        raise ValueError('Set the SVN_PASSWORD repository secret.')
    with tempfile.TemporaryDirectory(prefix='investbeacon-listing-') as directory:
        work = Path(directory) / 'working-copy'
        run_svn(['checkout', SVN_URL, str(work)])
        paths = ['trunk', 'tags/' + manifest['version']]
        for name in paths:
            current = read_tree(work / name)
            if current not in (original, expected):
                raise ValueError('Unexpected remote files in ' + name + '; refusing update.')
        if all(read_tree(work / name) == expected for name in paths):
            print('Listing already updated; no commit needed.')
            return
        for name in paths:
            (work / name / 'readme.txt').write_bytes(updated)
        result = run_svn(['commit', *[name + '/readme.txt' for name in paths], '-m',
                          'Add InvestBeacon website and contact links to directory readme'], cwd=work, password=password)
        print(result)
        for index, name in enumerate(paths):
            export = Path(directory) / ('verified-' + str(index))
            run_svn(['export', SVN_URL + '/' + name, str(export)])
            if read_tree(export) != expected:
                raise RuntimeError('Remote verification failed; inspect before retrying.')
        print('Verified readme links in trunk and stable tag; all 8 runtime files unchanged.')


if __name__ == '__main__':
    main()
