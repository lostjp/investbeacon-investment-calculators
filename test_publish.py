import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile
import publish_wordpress as publisher


class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.manifest, self.files = publisher.approved_release()

    def fixture(self, root, entries=None):
        manifest = dict(self.manifest)
        archive = root / manifest['archive']
        with ZipFile(archive, 'w') as package:
            for name, data in (entries or {publisher.SLUG + '/' + name: data for name, data in self.files.items()}).items():
                package.writestr(name, data)
        manifest['sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
        (root / 'release.json').write_text(json.dumps(manifest))
        return manifest

    def test_approved_artifact(self):
        self.assertEqual(self.manifest['version'], '1.0.1')
        self.assertEqual(len(self.files), 9)

    def test_modified_archive_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.fixture(root)
            with (root / self.manifest['archive']).open('ab') as file:
                file.write(b'changed')
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                publisher.approved_release(root)

    def test_traversal_is_rejected_even_with_matching_digest(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.fixture(root, {publisher.SLUG + '/../escape.php': b'bad'})
            with self.assertRaisesRegex(ValueError, 'Unsafe'):
                publisher.approved_release(root)

    def test_version_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            files = {publisher.SLUG + '/' + name: data for name, data in self.files.items()}
            files[publisher.SLUG + '/readme.txt'] = files[publisher.SLUG + '/readme.txt'].replace(b'Stable tag: 1.0.1', b'Stable tag: 9.9.9')
            self.fixture(root, files)
            with self.assertRaisesRegex(ValueError, 'version mismatch'):
                publisher.approved_release(root)

    def test_existing_release_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            work = Path(d)
            (work / 'trunk').mkdir()
            tag = work / 'tags' / self.manifest['version']
            tag.mkdir(parents=True)
            (tag / 'unexpected.txt').write_text('old release')
            with self.assertRaisesRegex(ValueError, 'refusing'):
                publisher.stage_release(work, self.manifest, self.files)

    def test_exact_existing_release_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            work = Path(d)
            (work / 'trunk').mkdir()
            tag = work / 'tags' / self.manifest['version']
            tag.mkdir(parents=True)
            for name, data in self.files.items():
                target = tag / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            self.assertFalse(publisher.stage_release(work, self.manifest, self.files))

    def test_password_is_sent_on_stdin_and_never_command_line(self):
        result = unittest.mock.Mock(returncode=0, stdout='Committed.', stderr='')
        with patch('publish_wordpress.subprocess.run', return_value=result) as run:
            publisher.run_svn(['commit', 'trunk'], password='test-only-credential')
            args, kwargs = run.call_args
            self.assertNotIn('test-only-credential', args[0])
            self.assertEqual(kwargs['input'], 'test-only-credential\n')
            self.assertIn('--no-auth-cache', args[0])


if __name__ == '__main__':
    unittest.main()
