#!/usr/bin/env python3
"""冻结小批案例的阶段产物，校验输入且拒绝覆盖已有冻结。"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('batch')
p.add_argument('case_id')
p.add_argument('stage', choices=['cca_pma', 'resource', 'reveal'])
a = p.parse_args()
manifest_path = ROOT / 'batches' / a.batch / 'manifest.json'
m = json.loads(manifest_path.read_text())
assert a.case_id in m['case_ids'], 'Case not in batch'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for item in m['skill_files'] + [m['protocol']] + m['questions']:
    assert digest(ROOT / item['path']) == item['sha256'], f'Input changed: {item["path"]}'
records = m['freeze_records']
for record in records:
    assert digest(ROOT / record['path']) == record['sha256'], 'Frozen output changed'
assert not any(r['case_id'] == a.case_id and r['stage'] == a.stage for r in records), 'Already frozen'
required = {'cca_pma': None, 'resource': 'cca_pma', 'reveal': 'resource'}[a.stage]
if required:
    assert any(r['case_id'] == a.case_id and r['stage'] == required for r in records), 'Missing prior stage'
folder = ROOT / 'batches' / a.batch / a.case_id
filename = {'cca_pma': 'before-resource.md', 'resource': 'before-answer.md', 'reveal': 'answer.md'}[a.stage]
path = folder / filename
if a.stage == 'reveal':
    assert not path.exists(), 'Answer already exists'
    packets = json.loads((ROOT / '_private' / a.batch / 'answer-packets.json').read_text())
    content = packets[a.case_id]
    assert hashlib.sha256(content.encode()).hexdigest() == m['answer_packet_sha256'][a.case_id], 'Answer packet changed'
    path.write_text(content)
assert path.is_file() and path.stat().st_size > 100, 'Missing or empty stage output'
record = {'case_id': a.case_id, 'stage': a.stage,
          'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path),
          'recorded_at': datetime.now(timezone.utc).isoformat()}
records.append(record)
manifest_path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(record, ensure_ascii=False))
