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
def validate_profile(profile, destination, source):
    """Validate supplied evidence metadata and output containment; never writes files."""
    errors=[]
    destination=Path(destination).resolve()
    source=Path(source).resolve()
    if destination == source or source in destination.parents or destination in source.parents:
        errors.append('Source and destination overlap')
    for field in ('tool','environment','verified_on','evidence','capabilities','outputs'):
        if not profile.get(field): errors.append('Missing profile field: '+field)
    from datetime import date
    try:
        verified=date.fromisoformat(profile.get('verified_on',''))
        if verified > date.today(): errors.append('Evidence date is in the future')
    except (ValueError,TypeError): errors.append('Invalid verification date')
    for item in profile.get('evidence',[]):
        if not isinstance(item,dict) or not all(item.get(k) for k in ('location','scope','status')):
            errors.append('Incomplete evidence')
        elif item['status'] != 'verified': errors.append('Evidence not verified')
    for capability in profile.get('capabilities',[]):
        if capability.get('required') and capability.get('status') != 'verified':
            errors.append('Required capability unavailable')
        if not capability.get('required') and capability.get('status') != 'verified' and not capability.get('fallback'):
            errors.append('Optional capability needs fallback')
    for name in profile.get('outputs',[]):
        path=Path(name)
        resolved=(destination/path).resolve()
        if path.is_absolute() or resolved == destination or destination not in resolved.parents:
            errors.append('Output escapes destination: '+str(name))
    return errors

def main():
    errors=validate()
    for error in errors: print(error)
    print(f'Neutral contract validation: {len(errors)} issue(s). Runtime acceptance not tested.')
    return bool(errors)
if __name__=='__main__': raise SystemExit(main())
