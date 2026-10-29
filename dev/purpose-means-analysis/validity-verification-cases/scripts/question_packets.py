"""按已审核的原文范围生成盲试输入，摘要和审核意见不进入题干。"""
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]


def source_excerpt(segment):
    lines = (ROOT / segment['file']).read_text().splitlines()
    raw = '\n'.join(lines[segment['line_start'] - 1:segment['line_end']])
    return raw[segment['char_start']:segment['char_end']]


def locate_excerpt(segment):
    lines = (ROOT / segment['file']).read_text().splitlines()
    assert 1 <= segment['line_start'] <= segment['line_end'] <= len(lines)
    raw = '\n'.join(lines[segment['line_start'] - 1:segment['line_end']])
    indices = [i for i, c in enumerate(raw) if not c.isspace()]
    compact = ''.join(raw[i] for i in indices)
    target = re.sub(r'\s+', '', segment['text'])
    assert target, 'Empty source excerpt'
    start = compact.find(target)
    assert start >= 0, f'Excerpt differs from OCR: {segment["file"]}:{segment["line_start"]}'
    result = {key: segment[key] for key in ['file', 'line_start', 'line_end', 'page', 'role']}
    result.update(char_start=indices[start], char_end=indices[start + len(target) - 1] + 1)
    return result


def render_packet(case, include_later_constraints=False):
    assert case['status'] == 'ready_text', f'{case["id"]}: input not ready'
    assert case['segments'], 'No original question'
    labels = {'statement': '原题', 'context': '原题所需上下文',
              'hint': '原书提示', 'later_constraint': '后文任务重述'}
    result = [f'# {case["id"]}：原文任务\n']
    previous_role = None
    for index, segment in enumerate(case['segments']):
        if segment['role'] == 'later_constraint' and not include_later_constraints:
            continue
        text = source_excerpt(segment)
        for correction in case.get('confirmed_corrections', []):
            if correction['segment_index'] == index:
                assert correction['old'] in text, 'Correction does not match source'
                text = text.replace(correction['old'], correction['new'], 1)
        if segment['role'] != previous_role:
            result.append(f'## {labels[segment["role"]]}\n')
        result.append(text.strip())
        previous_role = segment['role']
    if case.get('confirmed_corrections'):
        result.append('## OCR校正记录\n')
        seen_corrections = set()
        for c in case['confirmed_corrections']:
            if case['segments'][c['segment_index']]['role'] == 'later_constraint' and not include_later_constraints:
                continue
            key = (c['old'], c['new'], c['pdf_page'])
            if key in seen_corrections:
                continue
            seen_corrections.add(key)
            result.append(f'- `{c["old"]}` → `{c["new"]}`，已核PDF物理页{c["pdf_page"]}。\n')
    result.append('## 来源定位\n')
    for segment in case['segments']:
        result.append(f'- `{segment["file"]}`，Page {segment["page"]}，'
                      f'行{segment["line_start"]}至{segment["line_end"]}。\n')
    result.append('来源仅供事后溯源，答案前不得读取原书、索引或审核记录。\n')
    return '\n'.join(result)


def fingerprint(text):
    return hashlib.sha256(text.encode()).hexdigest()
