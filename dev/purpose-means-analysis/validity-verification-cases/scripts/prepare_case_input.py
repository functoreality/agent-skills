#!/usr/bin/env python3
"""从审核过的原文范围准备未来题干，拒绝摘要代题和未就绪记录。"""
import argparse
import json
from pathlib import Path
from question_packets import ROOT, render_packet, fingerprint

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('case_id')
p.add_argument('output', type=Path)
p.add_argument('--evaluation-mode', default='generation',
               choices=['generation', 'given_solution_analysis', 'prediction',
                        'historical_reconstruction', 'task_reconstruction'])
p.add_argument('--include-later-constraints', action='store_true')
a = p.parse_args()
records = json.loads((ROOT / 'input-audit/cases.json').read_text())
case = next(c for c in records if c['id'] == a.case_id)
if case['status'] != 'ready_text':
    p.error(f'{a.case_id}: {case["status"]}, cannot use as a complete blind input')
if case['evaluation_mode'] != a.evaluation_mode:
    p.error(f'{a.case_id}: original task is {case["evaluation_mode"]}, not {a.evaluation_mode}')
text = render_packet(case, include_later_constraints=a.include_later_constraints)
packet = case.get('supplemental_packet', case['packet']) if a.include_later_constraints else case['packet']
assert fingerprint(text) == packet['sha256'], 'Source or approved packet changed'
if a.output.exists():
    p.error('Output exists, do not replace a frozen or existing input')
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text(text)
print(json.dumps({'case_id': a.case_id, 'sha256': fingerprint(text),
                  'audit': 'input-audit/cases.json', 'input_version': 'source-v2',
                  'evaluation_mode': a.evaluation_mode,
                  'include_later_constraints': a.include_later_constraints}, ensure_ascii=False))
