#!/usr/bin/env python3
"""检查公开文本、引用及冻结指纹，可选核验本地私有材料和Git历史。"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / '_private'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--with-private', action='store_true', help='同时核验本地原书、OCR和原始实验输入')
parser.add_argument('--history', action='store_true', help='核验所有本地分支中当前目录的已提交历史')
args = parser.parse_args()
errors, warnings = [], []
skipped_private = set()
source_cache = {}
BINARY_SUFFIXES = {'.pdf', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp',
                   '.tif', '.tiff', '.avif', '.heic', '.zip', '.7z', '.tar', '.gz',
                   '.docx', '.xlsx', '.pptx', '.mp3', '.mp4'}
MACHINE_PATH = re.compile(r'/(?:home|Users)/[^\s"\x27)]+|[A-Za-z]:[\\/](?:Users|Documents)[\\/]')


def git(*arguments, directory=ROOT):
    return subprocess.check_output(['git', '-C', str(directory), *arguments], stderr=subprocess.DEVNULL)


def private_path(path):
    return path.resolve().is_relative_to(PRIVATE)


def available(path, label):
    if private_path(path) and not args.with_private:
        skipped_private.add(str(path.relative_to(ROOT)))
        return False
    if not path.exists():
        errors.append(f'Missing {label}: {path}')
        return False
    return True


def verify_hash(item, label):
    path = ROOT / item['path']
    if available(path, label) and hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        errors.append(f'{label} fingerprint changed: {item["path"]}')


def check_public_file(name, data):
    if '_private' in Path(name).parts:
        errors.append(f'Private material tracked: {name}')
    if Path(name).suffix.lower() in BINARY_SUFFIXES:
        errors.append(f'Media or document file tracked: {name}')
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        errors.append(f'Non-text file tracked: {name}')
        return
    if '\0' in text:
        errors.append(f'Binary content tracked: {name}')
    if MACHINE_PATH.search(text) or ('file:' + '/' * 2) in text:
        errors.append(f'Machine-specific path in public text: {name}')


try:
    public_files = [ROOT / name for name in git('ls-files', '--', '.').decode().splitlines()]
except subprocess.CalledProcessError:
    public_files = [path for path in ROOT.rglob('*') if path.is_file()
                    and not private_path(path) and '__pycache__' not in path.parts]
for path in public_files:
    if path.exists():
        check_public_file(path.relative_to(ROOT).as_posix(), path.read_bytes())
    else:
        errors.append(f'Tracked public file missing: {path.relative_to(ROOT)}')

cases_path = ROOT / 'inventory/cases.json'
cases = json.loads(cases_path.read_text())
ids = [case['id'] for case in cases]
if len(set(ids)) != len(ids):
    errors.append('Repeated canonical case IDs')
missing = {f'T{i:02}' for i in range(1, 71)} - set(ids)
coverage = json.loads((ROOT / 'inventory/coverage.json').read_text())
if missing - set(coverage['unobserved_labels']):
    errors.append(f'Undocumented missing numbered cases: {sorted(missing)}')
if missing:
    warnings.append(f'Documented source numbering gaps: {sorted(missing)}')
for case in cases:
    for key in ['question_refs', 'answer_refs']:
        for ref in case[key]:
            path = ROOT / ref['file']
            if not available(path, 'reference source'):
                continue
            if path not in source_cache:
                source_cache[path] = path.read_text().splitlines()
            lines = source_cache[path]
            start, end = ref['line_start'], ref['line_end']
            if not 1 <= start <= end <= len(lines):
                errors.append(f'{case["id"]}: invalid source span {start}:{end}')
                continue
            pages = [int(match.group(1)) for line in lines[:start]
                     if (match := re.match(r'## Page (\d+)', line))]
            if not pages or str(pages[-1]) != str(ref['page']):
                errors.append(f'{case["id"]}: source page does not match span')
    if not case['question_refs']:
        warnings.append(f'{case["id"]}: no question reference')

for path in public_files:
    if path.suffix != '.md' or not path.exists():
        continue
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if target.startswith(('http:', 'https:', '#')):
            continue
        target = re.sub(r':\d+$', '', target.strip('<>')).split('#', 1)[0]
        linked = path.parent / target
        available(linked, f'link from {path.relative_to(ROOT)}')

for item in json.loads((ROOT / 'sources/manifest.json').read_text())['files']:
    verify_hash(item, 'Input')
verify_hash(json.loads((ROOT / 'sources/pdf-manifest.json').read_text()), 'PDF input')
for item in json.loads((ROOT / 'sources/private-inputs-manifest.json').read_text())['files']:
    verify_hash(item, 'Original private input')
for record in json.loads((ROOT / 'pilot/freeze.json').read_text()):
    for path, expected in [
        (ROOT / record['file'], record['sha256']),
        (ROOT / f'pilot/{record["case_id"]}/question.md', record['question_sha256']),
        (ROOT / record.get('protocol_file', 'protocols/solver.md'), record['protocol_sha256'])]:
        if available(path, 'frozen input') and hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f'Frozen input changed: {path.relative_to(ROOT)}')

history_commits = 0
if args.history:
    try:
        prefix = git('rev-parse', '--show-prefix').decode().strip()
        top = Path(git('rev-parse', '--show-toplevel').decode().strip())
        commits = git('rev-list', '--all', '--', prefix, directory=top).decode().splitlines()
        seen = set()
        for commit in commits:
            for entry in git('ls-tree', '-r', '-z', commit, '--', prefix, directory=top).split(b'\0'):
                if not entry:
                    continue
                meta, name = entry.split(b'\t', 1)
                mode, kind, oid = meta.decode().split()
                if kind != 'blob' or (name, oid) in seen:
                    continue
                seen.add((name, oid))
                check_public_file(f'{commit[:8]}:{name.decode()}', git('cat-file', 'blob', oid))
        history_commits = len(commits)
    except subprocess.CalledProcessError:
        errors.append('History validation requires a Git checkout')

print(json.dumps({'errors': errors, 'warnings': warnings, 'canonical_cases': len(cases),
                  'private_validation': 'requested' if args.with_private else 'not_requested',
                  'private_paths_skipped': len(skipped_private),
                  'history_commits_checked': history_commits}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
