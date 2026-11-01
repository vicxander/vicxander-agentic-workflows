"""Validate neutral semantic contracts. Native runtime checks are separate."""
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_CONTRACT_VERSION = "3.0.0"
def validate(root=ROOT):
    errors=[]
    required=['workflow/principles.md','workflow/orchestration.md','workflow/capabilities.md','bootstrap/INITIALIZE.md','bootstrap/UPDATE.md','bootstrap/TARGET_PROFILE_TEMPLATE.md']
    required += [f'workflow/roles/{role}.md' for role in ('orchestrator','architect','coder','tester','reviewer')]
    for name in required:
        if not (root/name).is_file(): errors.append('Missing '+name)
    rules=json.loads((root/'tools/contract_rules.json').read_text(encoding='utf-8'))
    prose='\n'.join(p.read_text(encoding='utf-8') for folder in ('workflow','templates') for p in (root/folder).rglob('*.md'))
    for registry,clauses in rules.items():
        for name,pattern in clauses.items():
            if not re.search(pattern,prose,re.I|re.S): errors.append('Missing semantic clause '+registry+':'+name)
    for guide in ('INITIALIZE.md','UPDATE.md'):
        p=root/'bootstrap'/guide
        if p.is_file():
            text=p.read_text(encoding='utf-8')
            for rule in ('Missing or contradictory evidence blocks configuration writes',
                         'Dry-run is read-only', 'Keep unresolved files unchanged',
                         "Preserve the project's LICENSE", 'Reject escaping paths'):
                if rule not in text: errors.append('Missing bootstrap safeguard '+guide+': '+rule)
    for folder in ('workflow','templates','bootstrap'):
        for p in (root/folder).rglob('*.md'):
            if b'\r' in p.read_bytes(): errors.append('Non-LF text: '+str(p.relative_to(root)))
    return errors
def main():
    errors=validate()
    for error in errors: print(error)
    print(f'Neutral contract validation: {len(errors)} issue(s). Runtime acceptance not tested.')
    return bool(errors)
if __name__=='__main__': raise SystemExit(main())
