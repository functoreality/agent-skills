"""从Git历史读取实验输入，不依赖活动Skill的当前内容。"""
from pathlib import Path
import os
import subprocess


def historical_input(root, path, revision):
    top = Path(subprocess.check_output(
        ['git', '-C', str(root), 'rev-parse', '--show-toplevel'],
        stderr=subprocess.DEVNULL).decode().strip())
    repo_path = Path(os.path.abspath(root / path)).relative_to(top).as_posix()
    return subprocess.check_output(
        ['git', '-C', str(top), 'show', f'{revision}:{repo_path}'],
        stderr=subprocess.DEVNULL)
