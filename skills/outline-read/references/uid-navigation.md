# UID 导航

## 定位语法

`((uid))` 引用行末的 `{uid}`，允许定义后有空白。
定位不依赖文件是 Tab 大纲还是平铺 Markdown。
例如 `((topic-123))` 可以指向 `说明文字 {topic-123}`。

UID 按原文精确匹配，`abc`、`ABC` 和 `_abc` 是不同标识符。
定位器不解释 UID 的日期、前缀或内部组成，也不要求采用附带的生成算法。
标识符应为非空单行内容，避免使用会与 `((...))`、`{...}` 冲突的分隔符。
定位器按行末标记查找，不解析代码围栏或转义语义。

以下脚本路径相对于本 skill 目录，运行时使用实际安装路径。
带括号、空格或 shell 特殊字符的参数需要按 shell 规则引用：

```bash
scripts/uid-locate --dir /path/to/notes '((topic-123))'
scripts/uid-locate --dir /path/to/notes '{topic-123}' report.md
scripts/uid-locate --dir /path/to/notes '主题-甲' --context 4
scripts/outline-read --dir /path/to/notes --uid topic-123 --expand 1
```

## 搜索范围与结果

`--dir` 默认是当前工作目录。默认只查该目录下的 `.md` 文件，
`--recursive` 才查子目录。UID 定位和生成器的碰撞检查均支持此选项。
指定文件时，其路径相对于 `--dir`，也可以使用绝对路径，支持省略 `.md`。

```bash
scripts/uid-locate --dir /path/to/notes --recursive topic-123
scripts/outline-read --dir /path/to/notes --recursive --uid topic-123
scripts/uid-locate --dir /path/to/notes topic-123 'section/report with spaces.md'
```

只获取位置时，stdout 是绝对路径和从 1 开始的行号：

```text
/path/to/notes/report.md:120
```

`--context N` 改为输出位置及前后各 N 行原文，`N=0` 只附上定义行。
`--format json` 与 `--context` 不同时使用，JSON 输出只包含一个位置对象：

```json
{"path": "/path/to/notes/report.md", "line": 120, "uid": "topic-123"}
```

错误写入 stderr，不混入位置数据。退出码：0 成功，1 读取失败，
2 参数或输入错误，3 找不到目录、文件或 UID，4 UID 定义不唯一。
重复 UID 不自动选第一个，可缩小文件范围后重新定位。
文件读取失败也会停止，以免把不完整搜索误报为唯一匹配。

## 组合阅读

阅读大纲时通常直接调用 `outline-read --uid`，一次完成定位和展开。
需要先检查位置再决定如何阅读时，可分两次调用。
脚本之间也可以传递 JSON，不需要自行解析带空格的文件名：

```bash
scripts/uid-locate --dir /path/to/notes topic-123 --format json |
  scripts/outline-read --location-stdin --expand 1
```

`--location-stdin` 接受一个包含绝对 `path` 和正整数 `line` 的 JSON 对象，
不能与 `--uid` 或位置参数一起使用。空输入、多个结果或非法对象会报错。
行号用于即时阅读，文件编辑后应重新解析 UID，不把行号当作长期身份。

## 可选生成方案

需要新 UID 时，可以使用 `scripts/gen-uid`，也可以采用其他生成方式。
已有 UID 无须转换。生成器输出 `{uid}` 候选，信息提示写入 stderr，
不会修改文件或预留标识符。

```bash
scripts/gen-uid --dir /path/to/notes
scripts/gen-uid --dir /path/to/notes --recursive
scripts/gen-uid --no-collision-check
```

此方案将时间编码为六位小写字母数字，约每十秒变化一次。
默认检查指定目录下 `.md` 文件是否已含候选字符串，遇到冲突按 36 进制递增。
检查只针对当时可读的搜索范围，不保证跨集合或并发生成的唯一性。
连续生成但尚未写入的结果也可能相同，使用前应检查并避免重复。
自行递增得到的其他候选也需要检查冲突。

前缀用途、哪些条目需要 UID 等规则，由具体项目定义。
生成器不赋予下划线或其他前缀任何通用语义。
