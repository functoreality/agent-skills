#!/usr/bin/env python3
"""Report Markdown length, with optional list-width and prefix suggestions."""

import argparse
import re
from pathlib import Path


FRONT_MATTER = re.compile(
    r"\A---[ \t]*\n(?=(?:[ \t]*(?:#[^\n]*)?\n)*[\w-]+[ \t]*:)"
    r".*?^(?:---|\.\.\.)[ \t]*(?:\n|$)",
    re.MULTILINE | re.DOTALL,
)
HTML_BREAK = re.compile(r"<br(?:\s[^>]*)?\s*/?>", re.IGNORECASE)
HTML_WHITESPACE = re.compile(r"[ \t\r\n\f]+")


PREFIX_PUNCTUATION = ":：—，。；！？、!?"
PREFIX_PART = rf"[^{PREFIX_PUNCTUATION}]+"
MIDDLE_DOT_PART = rf"[^{PREFIX_PUNCTUATION}·]+"
PREFIX = re.compile(rf"^({PREFIX_PART})(?:—({PREFIX_PART}))?([：:])(?!//)")
MIDDLE_DOT_PREFIX = re.compile(rf"^({MIDDLE_DOT_PART})(?:—({MIDDLE_DOT_PART}))?·")
TASK_BOX = re.compile(r"^\[[ xX]\] +")


def readable_lines(inline):
    parts = []
    for token in inline.children or []:
        if token.type in ('text', 'code_inline'):
            parts.append(token.content)
        elif token.type == 'softbreak':
            parts.append(' ')
        elif token.type == 'hardbreak' or (
            token.type == 'html_inline' and HTML_BREAK.fullmatch(token.content)
        ):
            parts.append('\n')

    for line in ''.join(parts).split('\n'):
        yield HTML_WHITESPACE.sub(' ', line).strip(' ')


def prose_lines(tokens):
    for opening, inline in zip(tokens, tokens[1:]):
        if opening.type not in ('paragraph_open', 'heading_open') or inline.type != 'inline':
            continue

        first, end = opening.map
        for line in readable_lines(inline):
            yield first + 1, end, line


def prefix_suggestion(text):
    prefix = PREFIX.match(text)
    if prefix and prefix[3] == ':':
        before = (prefix[2] or prefix[1]).rstrip()
        after = text[prefix.end():prefix.end() + 1]
        if before[-1:].isdigit() and after.isdigit():
            prefix = None

    middle_dot = MIDDLE_DOT_PREFIX.match(text)
    # Prefer a colon when a single-part prefix contains a middle dot, as in a name.
    if middle_dot and (prefix is None or middle_dot[2] is not None):
        prefix = middle_dot

    add_prefix = '可考虑用短语加冒号或中点'
    if not prefix:
        return add_prefix

    phrases = [part.strip() for part in prefix.groups()[:2] if part is not None]
    if not all(phrases):
        return add_prefix

    longest = max(map(len, phrases))
    if longest > 10:
        return f'行首短语最长 {longest} 字，能否先精简？仍超 10 字时可考虑省略这一段'
    if longest > 6:
        return f'行首短语最长 {longest} 字，能否先精简？难以精简且确有需要时可保留'
    return None


def prefix_suggestions(tokens):
    for item, opening, inline in zip(tokens, tokens[1:], tokens[2:]):
        if (item.type, opening.type, inline.type) != ('list_item_open', 'paragraph_open', 'inline'):
            continue
        text = TASK_BOX.sub('', next(readable_lines(inline)))
        if text:
            suggestion = prefix_suggestion(text)
            if suggestion:
                yield opening.map[0] + 1, suggestion


def wide_lists(tokens, limit):
    stack = []
    for token in tokens:
        if token.type in ('bullet_list_open', 'ordered_list_open'):
            first, end = token.map
            stack.append((first + 1, end, 0))
        elif token.type == 'list_item_open':
            first, end, count = stack[-1]
            stack[-1] = first, end, count + 1
        elif token.type in ('bullet_list_close', 'ordered_list_close'):
            first, end, count = stack.pop()
            if count > limit:
                yield first, end, count


def main():
    args_parser = argparse.ArgumentParser(description=__doc__)
    args_parser.add_argument('files', nargs='+', type=Path)
    args_parser.add_argument('--limit', type=int, default=100, help='长度提示阈值，默认 100')
    args_parser.add_argument('--max-siblings', type=int, help='同一列表的直接子项提示阈值')
    args_parser.add_argument(
        '--check-prefix', action=argparse.BooleanOptionalAction, default=False,
        help='给出行首短语建议，默认关闭',
    )
    args = args_parser.parse_args()
    if args.limit < 1:
        args_parser.error('--limit 需要是正整数')
    if args.max_siblings is not None and args.max_siblings < 1:
        args_parser.error('--max-siblings 需要是正整数')

    try:
        from markdown_it import MarkdownIt
    except ImportError:
        args_parser.exit(2, '请先安装依赖，运行 python3 -m pip install markdown-it-py\n')

    markdown = MarkdownIt('commonmark').enable(['table', 'strikethrough'])
    prefix_hints = []
    for path in args.files:
        try:
            source = path.read_text(encoding='utf-8-sig')
        except (OSError, UnicodeError) as error:
            args_parser.exit(2, f'{path}: {error}\n')
        source = FRONT_MATTER.sub(lambda match: '\n' * match[0].count('\n'), source)
        tokens = markdown.parse(source)
        for first, end, line in prose_lines(tokens):
            if len(line) > args.limit:
                location = str(first) if first == end else f'{first}-{end}'
                print(f'{path}:{location}  {len(line)} 字符  {line}')
        if args.max_siblings is not None:
            for first, end, count in sorted(wide_lists(tokens, args.max_siblings)):
                print(f'{path}:{first}-{end}  同级 {count} 项')
        if args.check_prefix:
            prefix_hints.extend((path, line, note) for line, note in prefix_suggestions(tokens))

    for path, line, note in prefix_hints:
        print(f'{path}:{line}  行首建议  {note}')


if __name__ == '__main__':
    main()
