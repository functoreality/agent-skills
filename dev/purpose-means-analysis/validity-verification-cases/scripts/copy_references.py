#!/usr/bin/env python3
"""把用户已有的PDF与三份OCR复制到忽略目录，核验版本，不记录来源绝对路径。"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pdf', required=True, type=Path)
parser.add_argument('--ocr-dir', required=True, type=Path)
args = parser.parse_args()
items = [json.loads((ROOT / 'sources/pdf-manifest.json').read_text())]
items += [item for item in json.loads((ROOT / 'sources/manifest.json').read_text())['files']
          if item['path'].startswith('_private/references/')]
copies = []
for item in items:
    destination = ROOT / item['path']
    source = args.pdf if destination.suffix == '.pdf' else args.ocr_dir / destination.name
    if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != item['sha256']:
        raise SystemExit(f'Input missing or fingerprint mismatch: {destination.name}')
    if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest() != item['sha256']:
        raise SystemExit(f'Existing local copy differs: {destination.name}')
    copies.append((source, destination))
for source, destination in copies:
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
print(f'Checked {len(copies)} local reference files.')
