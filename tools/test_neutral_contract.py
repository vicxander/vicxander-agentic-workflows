"""Regressions for neutral source semantic validation."""
import shutil
import tempfile
import unittest
from pathlib import Path
from tools import validate_workflows as v
class ContractTests(unittest.TestCase):
    def test_current_contract(self):
        self.assertEqual([],v.validate())
    def fixture(self,root):
        for folder in ('workflow','templates','bootstrap','tools'):
            shutil.copytree(v.ROOT/folder,root/folder,ignore=shutil.ignore_patterns('__pycache__'))
    def test_missing_role_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.fixture(root)
            (root/'workflow/roles/coder.md').unlink()
            self.assertIn('Missing workflow/roles/coder.md',v.validate(root))
    def test_removed_semantics_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.fixture(root)
            for folder in ('workflow','templates'):
                for p in (root/folder).rglob('*.md'):p.write_text('',encoding='utf-8')
            self.assertEqual(47,len(v.validate(root)))
