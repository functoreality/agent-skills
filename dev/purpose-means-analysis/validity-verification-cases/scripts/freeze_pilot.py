#!/usr/bin/env python3
"""在解题 Agent 结束答案前阶段后调用，追加不可覆盖的指纹记录。"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
manifest = ROOT / 'pilot/freeze.json'
records = json.loads(manifest.read_text()) if manifest.exists() else []
known = {record['case_id'] for record in records}
for case_id in sys.argv[1:]:
    if case_id in known:
        raise SystemExit(f'{case_id} already frozen')
    relative = f'pilot/{case_id}/before-answer.md'
    path = ROOT / relative
    question = ROOT / f'pilot/{case_id}/question.md'
    records.append({
        'case_id': case_id,
        'file': relative,
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'question_sha256': hashlib.sha256(question.read_bytes()).hexdigest(),
        'protocol_file': 'protocols/solver.md',
        'protocol_sha256': hashlib.sha256((ROOT / 'protocols/solver.md').read_bytes()).hexdigest(),
        'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
        'stage': 'before_answer_release'})
    known.add(case_id)
manifest.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
print('Frozen:', ', '.join(sys.argv[1:]))
