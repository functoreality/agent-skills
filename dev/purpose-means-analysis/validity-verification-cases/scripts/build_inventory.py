#!/usr/bin/env python3
"""合并分段题解索引，保留各段摘要和不确定性，并生成可读索引。"""
from collections import Counter
from pathlib import Path
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]


def unique(values):
    result = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def paragraph(text):
    lines, current = [], ''
    for chunk in re.split(r'(?<=[。，；！？])', text):
        if current and len(current) + len(chunk) > 90:
            lines.append(current)
            current = ''
        current += chunk
    if current:
        lines.append(current)
    return '\n'.join(lines)


def refs_text(refs):
    result = []
    for ref in refs:
        path = os.path.relpath(ROOT / ref['file'], ROOT / 'inventory')
        start, end = ref['line_start'], ref['line_end']
        result.append(f"[Page {ref['page']}，L{start}–{end}，本地材料]({path}#page-{ref['page']})")
    return '\n'.join('- ' + item for item in result) or '未定位'


def main():
    merged = {}
    aliases_path = ROOT / 'inventory/aliases.json'
    aliases = json.loads(aliases_path.read_text()) if aliases_path.exists() else {}
    for number in range(1, 4):
        path = ROOT / f'inventory/part-{number}.json'
        records = json.loads(path.read_text())
        for record in records:
            case_id = aliases.get(record['id'], record['id'])
            case = merged.setdefault(case_id, {
                'id': case_id, 'title': record['title'], 'kind': record['kind'],
                'original_labels': [], 'statements': [], 'question_refs': [],
                'answers': [], 'answer_refs': [], 'keywords': [],
                'uncertainties': [], 'related_ids': [], 'provenance': []})
            for source, target in [('original_label', 'original_labels'),
                                   ('statement', 'statements'), ('answer', 'answers')]:
                if record.get(source):
                    case[target] = unique(case[target] + [record[source]])
            for key in ['question_refs', 'answer_refs', 'keywords',
                        'uncertainties', 'related_ids']:
                case[key] = unique(case[key] + record.get(key, []))
            case['provenance'].append(f"part-{number}:{record['id']}")
    corrections_path = ROOT / 'inventory/corrections.json'
    corrections = json.loads(corrections_path.read_text()) if corrections_path.exists() else {}
    for case_id, changes in corrections.items():
        if case_id not in merged:
            raise ValueError(f'Unknown correction id {case_id}')
        merged[case_id].update(changes)
    cases = sorted(merged.values(), key=lambda c: (not c['id'].startswith('T'), c['id']))
    for case in cases:
        case['answer_status'] = ('located' if case['answers'] and case['answer_refs']
                                 else 'not_located')
        for key in ['question_refs', 'answer_refs']:
            for ref in case[key]:
                source = ROOT / ref['file']
                if not source.exists():
                    continue
                lines = source.read_text().splitlines()
                if not 1 <= ref['line_start'] <= ref['line_end'] <= len(lines):
                    raise ValueError(f"Bad reference: {case['id']} {ref}")
    (ROOT / 'inventory/cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=2) + '\n')
    numbered = [case for case in cases if case['kind'] == 'numbered']
    status = Counter(case['answer_status'] for case in cases)
    intro = ('本轮仅建题解索引，未全量试解。编号题按机制和原题上下文合并错号引用。\n'
             '无编号实例保留分段标识，重复或高度相关实例须结合 related_ids 阅读，\n'
             '不能把条目总数当作独立测试样本数。题干摘要仅提取问题及约束，答案另表。\n'
             '引用页码取 Markdown 的 Page 标记，与书内印刷页码可能不同。\n'
             '原书PDF、完整OCR及截图不随仓库公开，本地链接使用前请看[资料说明](../sources/README.md)。\n'
             '已定点补查原PDF，核验过的条目另列PDF补充说明，其余图示仍需按必要性处理。\n\n')
    questions = ['# 题目索引\n\n', intro,
                 f'当前 {len(cases)} 条记录，其中编号题 {len(numbered)} 条。\n\n',
                 '解答见 [答案索引](answers.md)，疑点见各题及分段说明。\n\n']
    answers = ['# 原书解答索引\n\n',
               '解题 Agent 在答案前阶段不得读取本文件。\n'
               '摘要只反映已定位原文，不代表已验证原书方案正确或可行。\n\n',
               f"已定位解答或部分解法 {status['located']} 条，未定位 {status['not_located']} 条。\n\n"]
    for case in cases:
        case_id = case['id']
        questions.append(f"## {case_id} {case['title']}\n\n")
        questions.extend(f'{paragraph(text)}\n\n' for text in case['statements'])
        if not case['statements']:
            questions.append('本段仅有答案或后文引用，尚未定位完整题干。\n\n')
        questions.append(f"题干位置：\n\n{refs_text(case['question_refs'])}\n\n")
        if case['uncertainties']:
            questions.append('分段提取疑点（其中已跨段补齐的内容不再代表全书缺失）：\n\n')
            questions.extend(f'- {paragraph(item)}\n' for item in case['uncertainties'])
            questions.append('\n')
        if case['related_ids']:
            questions.append('相关条目：' + '、'.join(case['related_ids']) + '。\n\n')
        answers.append(f"## {case_id} {case['title']}\n\n")
        answers.extend(f'{paragraph(text)}\n\n' for text in case['answers'])
        if not case['answers']:
            answers.append('未定位原书解答，保持待核对。\n\n')
        answers.append(f"解答位置：\n\n{refs_text(case['answer_refs'])}\n\n")
        if case.get('pdf_verification'):
            check = case['pdf_verification']
            pdf_source = json.loads((ROOT / 'sources/pdf-manifest.json').read_text())['path']
            pdf_path = os.path.relpath(ROOT / pdf_source, ROOT / 'inventory')
            pdf_links = '、'.join(f"[PDF第{page}页]({pdf_path}#page={page})"
                                 for page in check['pages'])
            note = ('PDF补充核验：' + paragraph(check['summary']) + '\n\n' +
                    pdf_links + '。\n\n' +
                    f"[核验记录]({check['report']})。\n\n")
            questions.append(note)
            answers.append(note)

    (ROOT / 'inventory/questions.md').write_text(''.join(questions))
    (ROOT / 'inventory/answers.md').write_text(''.join(answers))
    print(json.dumps({'total': len(cases), 'numbered': len(numbered),
                      'answer_status': dict(status),
                      'private_sources_available': all((ROOT / item['file']).exists()
                          for case in cases for item in case['question_refs'] + case['answer_refs'])},
                     ensure_ascii=False))


if __name__ == '__main__':
    main()
