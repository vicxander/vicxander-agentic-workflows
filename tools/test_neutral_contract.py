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
            self.assertEqual(67,len(v.validate(root)))

class ProfileTests(unittest.TestCase):
    def profile(self):
        return dict(tool='Example tool',environment='documented context',verified_on='2026-11-01',
                    evidence=[dict(location='local:reference',scope='entrypoint',status='verified')],
                    capabilities=[dict(required=True,status='verified')],outputs=['instructions.md'])
    def check(self,profile):
        with tempfile.TemporaryDirectory() as directory:
            return v.validate_profile(profile,Path(directory)/'destination',Path(directory)/'source')
    def test_verified_profile(self): self.assertEqual([],self.check(self.profile()))
    def test_missing_fields(self):
        for field in self.profile():
            with self.subTest(field=field):
                p=self.profile();del p[field];self.assertTrue(self.check(p))
    def test_path_escape(self):
        for name in ('../escape.md','nested/../../escape.md'):
            p=self.profile();p['outputs']=[name];self.assertTrue(self.check(p))
    def test_missing_evidence(self):
        p=self.profile();p['evidence']=[{}];self.assertTrue(self.check(p))
    def test_contradictory_evidence(self):
        p=self.profile();p['evidence'][0]['status']='contradictory';self.assertTrue(self.check(p))
    def test_required_capability(self):
        p=self.profile();p['capabilities'][0]['status']='unavailable';self.assertTrue(self.check(p))
    def test_optional_fallback(self):
        p=self.profile();p['capabilities']=[dict(required=False,status='unavailable')]
        self.assertTrue(self.check(p));p['capabilities'][0]['fallback']='sequential';self.assertEqual([],self.check(p))
    def test_source_overlap(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(v.validate_profile(self.profile(),d,d))
    def test_validation_is_read_only(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);before=list(root.rglob('*'))
            v.validate_profile(self.profile(),root/'target',root/'source')
            self.assertEqual(before,list(root.rglob('*')))

class BootstrapRegressionTests(ContractTests):
    def test_safeguards_cannot_disappear(self):
        for rule in ('Dry-run is read-only','Keep unresolved files unchanged',
                     'Missing or contradictory evidence blocks configuration writes',
                     "Preserve the project's LICENSE",'Reject escaping paths'):
            with self.subTest(rule=rule),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);self.fixture(root)
                p=root/'bootstrap/UPDATE.md';p.write_text(p.read_text().replace(rule,'REMOVED'),encoding='utf-8')
                self.assertTrue(v.validate(root))
    def test_broken_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.fixture(root)
            p=root/'workflow/principles.md';p.write_text(p.read_text()+'\n[Missing](missing.md)\n',encoding='utf-8')
            self.assertTrue(v.validate(root))
    def test_stale_evidence(self):
        p=ProfileTests().profile();p['evidence'][0]['status']='stale'
        self.assertTrue(ProfileTests().check(p))
