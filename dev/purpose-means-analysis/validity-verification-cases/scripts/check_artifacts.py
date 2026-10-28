#!/usr/bin/env python3
"""检查题解引用、编号覆盖、试点冻结指纹与本地 Markdown 链接。"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []
source_cache = {}


def source_lines(path):
    if path not in source_cache:
        source_cache[path] = Path(path).read_text().splitlines()
    return source_cache[path]


cases_path = ROOT / 'inventory/cases.json'
if cases_path.exists():
    cases = json.loads(cases_path.read_text())
    ids = [case['id'] for case in cases]
    if len(set(ids)) != len(ids):
        errors.append('Repeated canonical case IDs')
    missing = sorted({f'T{i:02}' for i in range(1, 71)} - set(ids))
    coverage = json.loads((ROOT / 'inventory/coverage.json').read_text())
    declared = set(coverage['unobserved_labels'])
    if set(missing) - declared:
        errors.append(f'Undocumented missing numbered cases: {sorted(set(missing) - declared)}')
    if missing:
        warnings.append(f'Documented source numbering gaps: {missing}')
    for case in cases:
        for key in ['question_refs', 'answer_refs']:
            for ref in case[key]:
                lines = source_lines(ref['file'])
                start, end = ref['line_start'], ref['line_end']
                if not 1 <= start <= end <= len(lines):
                    errors.append(f"{case['id']}: invalid span {start}:{end}")
                    continue
                page = None
                for line in lines[:start]:
                    match = re.match(r'## Page (\d+)', line)
                    if match:
                        page = int(match[1])
                if str(ref['page']) != str(page):
                    warnings.append(f"{case['id']} {key}: ref page {ref['page']}, start page {page}")
        if not case['question_refs']:
            warnings.append(f"{case['id']}: no question reference")

for path in ROOT.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if target.startswith(('http:', 'https:', '#')):
            continue
        target = target.strip('<>')
        target = re.sub(r':\d+$', '', target).split('#', 1)[0]
        linked = Path(target) if target.startswith('/') else path.parent / target
        if not linked.exists():
            errors.append(f'{path.relative_to(ROOT)}: broken link {target}')

manifest_path = ROOT / 'sources/manifest.json'
if manifest_path.exists():
    for item in json.loads(manifest_path.read_text())['files']:
        actual = hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()
        if actual != item['sha256']:
            errors.append(f"Input changed since baseline: {item['path']}")

frozen_path = ROOT / 'pilot/freeze.json'
if frozen_path.exists():
    for item in json.loads(frozen_path.read_text()):
        path = ROOT / item['file']
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item['sha256']:
            errors.append(f"Frozen record changed: {item['file']}")

print(json.dumps({'errors': errors, 'warnings': warnings,
                  'canonical_cases': len(cases) if cases_path.exists() else None},
                 ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
