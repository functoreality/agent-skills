"""Locate literal line-end UID anchors independently of Markdown structure."""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


class UIDError(Exception):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class Location:
    path: Path
    line: int
    uid: str

    def as_dict(self) -> dict:
        return {'path': str(self.path), 'line': self.line, 'uid': self.uid}


def clean_uid(raw: str) -> str:
    """Accept a bare identifier, ((identifier)), or {identifier}."""
    uid = raw.strip()
    if uid.startswith('((') and uid.endswith('))'):
        uid = uid[2:-2]
    elif uid.startswith('{') and uid.endswith('}'):
        uid = uid[1:-1]
    if not uid or '\n' in uid or '\r' in uid:
        raise UIDError('UID must be a non-empty, single-line identifier', 2)
    return uid


def resolve_filepath(directory: Path, name: str) -> Path | None:
    path = directory / name
    if path.is_file():
        return path.resolve()
    if not name.endswith('.md'):
        path = directory / (name + '.md')
        if path.is_file():
            return path.resolve()
    return None


def find_uid_definition(raw_uid: str, directory: Path,
                        restrict_file: str | None = None,
                        recursive: bool = False) -> Location:
    """Return exactly one match, or raise on missing/ambiguous definitions."""
    uid = clean_uid(raw_uid)
    directory = directory.resolve()
    if not directory.is_dir():
        raise UIDError(f'directory not found: {directory}', 3)

    if restrict_file is not None:
        path = resolve_filepath(directory, restrict_file)
        if path is None:
            raise UIDError(f'file not found: {restrict_file} (in {directory})', 3)
        files = [path]
    else:
        files = sorted(directory.rglob('*.md') if recursive
                       else directory.glob('*.md'))

    pattern = re.compile(r'\{' + re.escape(uid) + r'\}\s*$')
    matches = []
    for path in files:
        if not path.is_file():
            continue
        try:
            with path.open(encoding='utf-8') as stream:
                for line_number, text in enumerate(stream, 1):
                    if pattern.search(text):
                        matches.append(Location(path.resolve(), line_number, uid))
        except (OSError, UnicodeError) as error:
            raise UIDError(f'cannot read {path}: {error}') from error

    if not matches:
        scope = str(directory / restrict_file) if restrict_file else str(directory)
        raise UIDError(f'UID {uid!r} not found in: {scope}', 3)
    if len(matches) > 1:
        candidates = '\n'.join(f'  {match.path}:{match.line}' for match in matches)
        raise UIDError(
            f'UID {uid!r} has {len(matches)} definitions:\n{candidates}\n'
            'Restrict the search to a file to disambiguate.', 4)
    return matches[0]


def main():
    parser = argparse.ArgumentParser(
        description='Locate a line-end {uid} anchor in outlined or flat Markdown.')
    parser.add_argument('uid', help='Bare UID, ((uid)), or {uid}')
    parser.add_argument('file', nargs='?', help='Optional file, relative to --dir')
    parser.add_argument('--dir', '-d', type=Path, default=Path.cwd(),
                        help='Search directory (default: current working directory)')
    parser.add_argument('--recursive', action='store_true',
                        help='Also search .md files in subdirectories')
    output = parser.add_mutually_exclusive_group()
    output.add_argument('--format', choices=['text', 'json'], default='text',
                        help='Output format (default: text, absolute path:line)')
    output.add_argument('--context', type=int, metavar='N',
                        help='Show the definition and N surrounding lines on each side')
    args = parser.parse_args()
    if args.context is not None and args.context < 0:
        parser.error('--context must be non-negative')

    try:
        location = find_uid_definition(args.uid, args.dir, args.file, args.recursive)
        if args.format == 'json':
            print(json.dumps(location.as_dict(), ensure_ascii=False))
        elif args.context is None:
            print(f'{location.path}:{location.line}')
        else:
            lines = location.path.read_text(encoding='utf-8').splitlines()
            print(f'{location.path}:{location.line}')
            first = max(1, location.line - args.context)
            last = min(len(lines), location.line + args.context)
            for number in range(first, last + 1):
                prefix = '>>> ' if number == location.line else ''
                print(f'{prefix}{number}: {lines[number - 1]}')
    except UIDError as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(error.code)
    except (OSError, UnicodeError) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
