#!/usr/bin/env python3
"""合并205条私有题干审核，公开定位元数据，生成无答案的私有原文题干包。"""
from collections import Counter
from pathlib import Path
import json
from question_packets import ROOT, locate_excerpt, render_packet, fingerprint

cases = {c['id']: c for c in json.loads((ROOT / 'inventory/cases.json').read_text())}
assignments = json.loads((ROOT / 'planning/input-audit-assignments.json').read_text())
records = []
for group, ids in assignments.items():
    rows = json.loads((ROOT / f'_private/input-audit/part-{group}.json').read_text())
    assert sorted(r['id'] for r in rows) == sorted(ids), f'Group {group}: coverage differs'
    records.extend(rows)
assert len(records) == len(cases) == len({r['id'] for r in records}), 'Audit coverage differs'
overrides_path = ROOT / 'input-audit/overrides.json'
overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
public = []


def retire(path):
    if path.exists():
        backup = ROOT / '_private/input-audit/retired-packets'
        backup.mkdir(parents=True, exist_ok=True)
        destination = backup / f'{path.parent.name}-{path.name}'
        index = 1
        while destination.exists():
            destination = backup / f'{path.parent.name}-{index}-{path.name}'
            index += 1
        path.rename(destination)


for record in sorted(records, key=lambda r: (not r['id'].startswith('T'), r['id'])):
    record.update(overrides.get(record['id'], {}))
    assert record['status'] in ['ready_text', 'needs_figure', 'needs_ocr', 'insufficient_statement', 'source_conflict']
    for ref in record['reviewed_refs']:
        assert ref['file'].startswith('_private/references/')
    output = {k: v for k, v in record.items() if k not in ['segments', 'packet_notes']}
    output['segments'] = []
    index_map = {}
    for index, segment in enumerate(record['segments']):
        if index in record.get('omit_segment_indices', []):
            continue
        audited = locate_excerpt(segment)
        updates = record.get('segment_updates', {}).get(str(index), {})
        index_map[index] = len(output['segments'])
        for update in updates if isinstance(updates, list) else [updates]:
            output['segments'].append(dict(audited, **update))
    if 'confirmed_corrections' in output:
        output['confirmed_corrections'] = [dict(c, segment_index=index_map[c['segment_index']])
                                           for c in output['confirmed_corrections']
                                           if c['segment_index'] in index_map]
    output['packet_notes'] = record.get('packet_notes', [])
    output['generation_eligible'] = record['status'] == 'ready_text' and record['evaluation_mode'] == 'generation'
    if record['status'] == 'ready_text':
        text = render_packet(output)
        path = ROOT / f'_private/question-packets-v2/{record["id"]}/question.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        output['packet'] = {'path': path.relative_to(ROOT).as_posix(), 'sha256': fingerprint(text)}
        if any(s['role'] == 'later_constraint' for s in output['segments']):
            extended = render_packet(output, include_later_constraints=True)
            extended_path = path.with_name('question-with-later-constraints.md')
            extended_path.write_text(extended)
            output['supplemental_packet'] = {'path': extended_path.relative_to(ROOT).as_posix(),
                                             'sha256': fingerprint(extended)}
        else:
            retire(path.with_name('question-with-later-constraints.md'))
    else:
        output['packet'] = None
        folder = ROOT / f'_private/question-packets-v2/{record["id"]}'
        retire(folder / 'question.md')
        retire(folder / 'question-with-later-constraints.md')
    public.append(output)
folder = ROOT / 'input-audit'
folder.mkdir(exist_ok=True)
(folder / 'cases.json').write_text(json.dumps(public, ensure_ascii=False, indent=2) + '\n')
lines = ['# 全量题干逐条复核\n\n',
         '范围为205条索引记录，不等于205道完整盲题。状态说明见[总览](README.md)。\n\n',
         '| 编号 | 原文形态 | 原任务类型 | 状态 | 审核结论 |\n|---|---|---|---|---|\n']
for row in public:
    summary = row['summary'].replace('|', '、').replace('\n', ' ')
    lines.append(f'| {row["id"]} | {row["input_form"]} | {row["evaluation_mode"]} | {row["status"]} | {summary} |\n')
(folder / 'case-review.md').write_text(''.join(lines))
print(json.dumps({'cases': len(public), 'status': Counter(r['status'] for r in public),
                  'form': Counter(r['input_form'] for r in public)}, ensure_ascii=False, indent=2))
