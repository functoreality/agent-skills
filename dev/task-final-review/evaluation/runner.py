import json
import sys
from pathlib import Path


if sys.argv[1] == 'empty-suite':
    print('collected 0 items')
elif sys.argv[1] == 'unique-ids':
    rows = json.loads(Path(__file__).with_name('data.json').read_text())
    identifiers = [row['id'] for row in rows]
    assert len(identifiers) == len(set(identifiers))
    print(f'checked {len(rows)} records, 0 duplicate IDs, 1 assertion passed')
else:
    raise SystemExit(2)
