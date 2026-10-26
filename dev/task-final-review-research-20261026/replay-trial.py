"""Replay the local fixtures without modifying the original research materials."""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from textwrap import dedent


source = Path(__file__).resolve().parent / 'evaluation'
workspace = Path(tempfile.mkdtemp(prefix='task-final-review-replay-'))
fixture = workspace / 'evaluation'
shutil.copytree(source, fixture)
records = []


def run(name, args, cwd=fixture):
    command = [sys.executable, *args]
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    record = dict(
        name=name, command=command, cwd=str(cwd), exit_code=result.returncode,
        stdout=result.stdout, stderr=result.stderr,
    )
    records.append(record)
    print(json.dumps(record, ensure_ascii=False))


def run_python(name, code):
    run(name, ['-c', dedent(code)])


run('case-1', ['runner.py', 'empty-suite'])
run('case-2', ['-m', 'json.tool', 'event-log.json'])
run('case-3-given-check', ['runner.py', 'unique-ids'])
run_python('case-3-independent', '''
    import json
    from collections import Counter
    from pathlib import Path
    rows = json.loads(Path('data.json').read_text())
    counts = Counter(row['id'] for row in rows)
    duplicates = {key: value for key, value in counts.items() if value > 1}
    print('record_count:', len(rows))
    print('unique_id_count:', len(counts))
    print('duplicates:', duplicates)
    assert not duplicates
''')
negative = workspace / 'negative-control'
negative.mkdir()
shutil.copy2(fixture / 'runner.py', negative / 'runner.py')
(negative / 'data.json').write_text(
    json.dumps([{'id': 'alpha'}, {'id': 'alpha'}]) + '\n'
)
run('case-3-negative-control', ['runner.py', 'unique-ids'], cwd=negative)
run('case-4', ['-m', 'json.tool', 'state.json'])
run('case-5-given-check', ['weak_check.py'])
run_python('case-5-direct-behavior', '''
    from application import double
    cases = [(-3, -6), (0, 0), (2, 4), (2.5, 5.0)]
    correct = True
    for value, expected in cases:
        actual = double(value)
        print(f'input={value!r}, expected={expected!r}, actual={actual!r}')
        correct = correct and actual == expected
    raise SystemExit(0 if correct else 1)
''')
log = workspace / 'execution-log.json'
log.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
print(f'Execution record: {log}')
print('Replay finished. Inspect individual results, including intentional failures.')
