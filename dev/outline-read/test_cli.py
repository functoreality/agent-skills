"""Automated CLI regression tests, using only the Python 3.10+ standard library.

Run from the repository root: python3 dev/outline-read/test_cli.py
"""

import json
import os
import re
import runpy
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch


SKILL = Path(os.environ.get(
    'OUTLINE_READ_SKILL_DIR',
    Path(__file__).resolve().parents[2] / 'skills' / 'outline-read'))


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='outline-cli-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tree = self.root / 'tree with spaces.md'
        self.tree.write_text(
            '* Root\n\t* Parent\n\t\t* Target {topic-123}\n'
            '\t\t\t* Child\n\t\t\t\t* Grandchild\n'
            '\t\t* Sibling\n\t\t\t* Sibling detail\n'
            '\t* Other branch\n\t\t* Other detail\n'
            '* Other root\n\t* Unrelated detail\n', encoding='utf-8')

    def call(self, script, *args, stdin=None):
        return subprocess.run(
            [sys.executable, str(SKILL / 'scripts' / script),
             '--dir', str(self.root), *args], input=stdin,
            capture_output=True, text=True,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})

    def assert_ok(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def visible_lines(self, output):
        return [int(number) for number in re.findall(
            r'^(?:>>> )?(\d+):', output, re.MULTILINE)]

    def test_coordinates_are_absolute_and_one_based(self):
        result = self.call('uid-locate', 'topic-123')
        self.assertEqual(self.assert_ok(result), f'{self.tree}:3\n')
        self.assertEqual(result.stderr, '')

    def test_flat_markdown_and_literal_identifiers(self):
        path = self.root / 'flat.md'
        identifiers = ['a', '_a', 'A', 'long-id-with-punctuation.v2',
                       '主题-甲', 'regex.*[x]+?', 'with space']
        path.write_text(''.join(f'Text {{{uid}}}  \n' for uid in identifiers)
                        + 'Mention ((reference-only))\n'
                        + 'Not an anchor {inline} trailing text\n', encoding='utf-8')
        for line, uid in enumerate(identifiers, 1):
            with self.subTest(uid=uid):
                data = json.loads(self.assert_ok(self.call(
                    'uid-locate', uid, '--format', 'json')))
                self.assertEqual(data, {'path': str(path), 'line': line, 'uid': uid})
        for uid in ['reference-only', 'inline', 'missing']:
            result = self.call('uid-locate', uid)
            self.assertEqual(result.returncode, 3)
            self.assertEqual(result.stdout, '')

    def test_wrapped_uids(self):
        for uid in ['topic-123', '((topic-123))', '{topic-123}']:
            self.assertEqual(self.assert_ok(self.call('uid-locate', uid)),
                             f'{self.tree}:3\n')

    def test_context_boundaries_and_zero(self):
        path = self.root / 'flat.md'
        path.write_text('Before\nTarget {flat}\nAfter\nOutside\n', encoding='utf-8')
        output = self.assert_ok(self.call('uid-locate', 'flat', '--context', '1'))
        self.assertIn('1: Before\n>>> 2: Target {flat}\n3: After\n', output)
        self.assertNotIn('Outside', output)
        output = self.assert_ok(self.call('uid-locate', 'flat', '--context', '0'))
        self.assertNotIn('Before', output)
        self.assertNotIn('After', output)
        output = self.assert_ok(self.call('uid-locate', 'flat', '--context', '100'))
        self.assertIn('4: Outside', output)

    def test_ambiguous_uid_never_returns_a_success_location(self):
        other = self.root / 'other.md'
        other.write_text('Duplicate {topic-123}\n', encoding='utf-8')
        for script in ['uid-locate', 'outline-read']:
            args = ['topic-123'] if script == 'uid-locate' else ['--uid', 'topic-123']
            result = self.call(script, *args)
            self.assertEqual(result.returncode, 4)
            self.assertEqual(result.stdout, '')
            self.assertIn(f'{other}:1', result.stderr)
            self.assertIn(f'{self.tree}:3', result.stderr)
        self.assertEqual(self.assert_ok(self.call(
            'uid-locate', 'topic-123', 'other')), f'{other}:1\n')

    def test_nested_paths_and_explicit_recursion(self):
        folder = self.root / 'sub folder'
        folder.mkdir()
        nested = folder / self.tree.name
        nested.write_text('* Nested\n\t* Target {nested-id}\n', encoding='utf-8')
        self.assertEqual(self.call('uid-locate', 'nested-id').returncode, 3)
        for suffix in [[], ['--recursive']]:
            args = ['nested-id', str(nested.relative_to(self.root))] if not suffix else ['nested-id', *suffix]
            data = json.loads(self.assert_ok(self.call(
                'uid-locate', *args, '--format', 'json')))
            self.assertEqual(data['path'], str(nested))
        for restriction in [str(nested), str(nested.relative_to(self.root))]:
            output = self.assert_ok(self.call('outline-read', '--uid', 'nested-id', restriction))
            self.assertIn('>>> 2: \t* Target {nested-id}', output)

    def test_read_failure_does_not_hide_a_potential_duplicate(self):
        (self.root / 'invalid.md').write_bytes(b'\xff\xfe')
        result = self.call('uid-locate', 'topic-123')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '')
        self.assertIn('cannot read', result.stderr)

    def test_fold_views_and_children_are_independent(self):
        cases = [(0, 1, [1, 2, 3, 4]), (0, 0, [1, 2, 3]),
                 (1, 1, [1, 2, 3, 4, 6]),
                 (2, 1, [1, 2, 3, 4, 6, 10]),
                 (3, 1, [1, 2, 3, 4, 6, 8, 10])]
        for expand, depth, expected in cases:
            with self.subTest(expand=expand, depth=depth):
                output = self.assert_ok(self.call(
                    'outline-read', self.tree.name, '3',
                    '--expand', str(expand), '--depth', str(depth)))
                self.assertEqual(self.visible_lines(output), expected)
                self.assertIn('>>> 3:', output)
                self.assertNotIn('Unrelated detail', output)
        output = self.assert_ok(self.call(
            'outline-read', self.tree.name, '3', '--tight', '--depth', '2'))
        self.assertIn('Grandchild', output)

    def test_direct_uid_and_json_composition_have_identical_views(self):
        direct = self.assert_ok(self.call('outline-read', self.tree.name, '3'))
        shorthand = self.assert_ok(self.call('outline-read', f'{self.tree.name}:3'))
        uid = self.assert_ok(self.call('outline-read', '--uid', 'topic-123'))
        location = self.assert_ok(self.call('uid-locate', 'topic-123', '--format', 'json'))
        piped = self.assert_ok(self.call('outline-read', '--location-stdin', stdin=location))
        self.assertEqual(direct, shorthand)
        self.assertEqual(direct, uid)
        self.assertEqual(direct, piped)

    def test_fold_indicators_include_file_edges(self):
        output = self.assert_ok(self.call(
            'outline-read', self.tree.name, '10', '--tight', '--depth', '0'))
        self.assertEqual(output,
                         '(9 lines folded)\n>>> 10: * Other root\n(1 lines folded)\n')
        output = self.assert_ok(self.call(
            'outline-read', self.tree.name, '10', '--tight', '--depth', '0',
            '--no-fold-indicators'))
        self.assertEqual(output, '>>> 10: * Other root\n')
        output = self.assert_ok(self.call(
            'outline-read', self.tree.name, '10', '--expand', '1', '--depth', '0'))
        self.assertEqual(self.visible_lines(output), [10])

    def test_toc_works_without_uids(self):
        path = self.root / 'no-uids.md'
        path.write_text('* One\n\t* Child\n* Two\n', encoding='utf-8')
        output = self.assert_ok(self.call('outline-read', 'no-uids'))
        self.assertEqual(self.visible_lines(output), [1, 3])

    def test_invalid_arguments_and_json_fail_without_output(self):
        cases = [('uid-locate', ['', '--format', 'json']),
                 ('uid-locate', ['topic-123', '--context', '-1']),
                 ('uid-locate', ['topic-123', '--format', 'json', '--context', '1']),
                 ('outline-read', [self.tree.name, '0']),
                 ('outline-read', [self.tree.name, '999']),
                 ('outline-read', [self.tree.name, '3', '--depth', '-1']),
                 ('outline-read', ['--uid', 'topic-123', self.tree.name, '3']),
                 ('outline-read', ['--location-stdin', self.tree.name])]
        for script, args in cases:
            with self.subTest(script=script, args=args):
                result = self.call(script, *args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')
        for data in ['', 'null', '{}', '[]', '{}\n{}',
                     '{"path":"relative.md","line":1}',
                     json.dumps({'path': str(self.tree), 'line': True})]:
            with self.subTest(stdin=data):
                result = self.call('outline-read', '--location-stdin', stdin=data)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')

    def test_optional_generator_uses_its_own_scheme_and_scope(self):
        generator = runpy.run_path(str(SKILL / 'scripts' / 'gen-uid'))
        stamp = datetime(2026, 10, 26, 12, 34, 50)
        core = generator['generate_core'](stamp)
        self.assertRegex(core, r'^[0-9a-z]{6}$')
        scope = self.root / 'generator-scope'
        scope.mkdir()
        nested = scope / 'nested'
        nested.mkdir()
        (nested / 'notes.md').write_text(f'Already used {{{core}}}\n', encoding='utf-8')
        with patch.dict(generator['find_unique_core'].__globals__,
                        {'generate_core': lambda: core}):
            self.assertEqual(generator['find_unique_core'](scope), (core, 0))
            result, count = generator['find_unique_core'](scope, True)
            self.assertEqual(count, 1)
            self.assertNotEqual(result, core)
        output = self.call('gen-uid')
        self.assertRegex(self.assert_ok(output), r'^\{[0-9a-z]{6}\}\n$')
        self.assertNotIn('Literature', output.stderr)
        self.assertNotIn('underscore', output.stderr)
        result = self.call('gen-uid', '--dir', str(self.root / 'missing'))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
