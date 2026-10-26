---
name: outline-read
description: >-
  浏览采用 Tab 缩进、层级很深的大纲式 Markdown，通过目录和折叠展开定位局部内容。
  也可在大纲或平铺 Markdown 中，按 ((uid)) 引用定位行末的 {uid} 定义，
  返回位置或上下文。UID 无须采用特定生成算法。文件短小或层级较浅时直接阅读。
---

# outline-read

提供两项可独立使用的能力，以及一步完成定位与展开的入口：

- `outline-read`：按文件、行号展示 Tab 大纲的结构上下文，也可按 UID 定位后展开。
- `uid-locate`：按 UID 定位，不依赖缩进或大纲结构，可返回位置、连续上下文或 JSON。

需要 Python 3.10+，仅使用标准库。脚本在本 skill 的 `scripts/` 中，
以下路径均相对于本 skill 目录，实际执行时替换为安装位置。
安装不会自动把这些脚本加入 `PATH`。

## 选择入口

| 目的 | 调用 |
|------|------|
| 看大纲的顶层目录 | `scripts/outline-read --dir /path/to/notes report` |
| 看第 120 行的结构上下文 | `scripts/outline-read --dir /path/to/notes report 120` |
| UID 定位后直接展开大纲 | `scripts/outline-read --dir /path/to/notes --uid topic-123` |
| 只获取 UID 的位置 | `scripts/uid-locate --dir /path/to/notes topic-123` |
| 看 UID 前后各 4 行原文 | `scripts/uid-locate --dir /path/to/notes topic-123 --context 4` |

支持省略文件的 `.md` 后缀，以及 `report.md:120` 简写。
文件路径和行号可以直接来自 `rg -n` 的搜索结果，不需要先创建 UID。
连续原文阅读和关键词搜索仍可使用环境提供的文件读取工具与 `rg`。
`read` 若是环境的工具名，不应当作 Bash 的文件读取命令运行。

## 大纲展开

大纲层级由行首 Tab 数量确定。此工具不解析普通 Markdown 的标题层级、
空格缩进或代码块语义。应确认文件采用这种大纲格式后再使用折叠功能。

所有展开模式都会保留祖先链和目标行，目标子节点由 `--depth` 独立控制：

| `--expand` | 在祖先链和目标之外展示什么 |
|------------|--------------------------|
| `0` 或 `--tight` | 不额外展示兄弟节点 |
| `1` | 非顶层目标的同级兄弟 |
| `2` | 级别 1，加全部非空顶层行 |
| `3`，默认 | 祖先链各层的兄弟节点，加全部非空顶层行 |

```bash
scripts/outline-read --dir /path/to/notes report 120 --expand 1
scripts/outline-read --dir /path/to/notes report 120 --tight --depth 0
scripts/outline-read --dir /path/to/notes report 120 --depth 2
```

`--depth` 默认是 1，设为 0 时不展示目标子节点。
顶层目标需要 `--expand 2` 或 `3` 才会显示其他顶层行。
`--no-top` 隐藏不属于祖先链或目标的顶层行。
`--no-fold-indicators` 关闭折叠行数提示。
输出保留原文行号，`>>>` 标记目标，`(N lines folded)` 表示跳过的行，
包括文件首尾被隐藏的内容。

平铺文件缺少可折叠的层级，默认模式会显示全部非空顶层行。
这类文件应使用 `uid-locate --context N` 或原生读取工具查看连续上下文。

## UID 导航与可选生成器

在采用此锚点语法的文档中，`((uid))` 引用行末的 `{uid}`。
UID 是按原文精确匹配的标识符，大小写和前缀均有意义，
不要求固定长度、字符类别或生成算法，但必须符合单行标记语法。
大纲阅读不要求 UID，读取或定位不会添加锚点、修改文件或生成 UID。

定位、搜索范围、JSON 管道及可选 `gen-uid` 生成器的用法见
[UID 导航](references/uid-navigation.md)，需要这些功能时再读取。

## 辅助脚本

- `scripts/tree-stats FILE`：节点、深度和行数统计。
  附带统计 `：末端` 与已分析标记，仅按文本计数，不要求使用这些标记。
- `scripts/tree-validate FILE`：检查 Tab 层级跳跃及缩进行前空行。
  这些是此种大纲格式的检查项，不是所有 Markdown 文件的规范。
- `scripts/tree-shift FILE L1 L2 N`：将指定行的缩进增减 N 个 Tab，输出到 stdout。
  拒绝空行、标题行、零位移及超出已有缩进的负位移。
  若用于修改文件，先输出到另一个文件并检查 diff，再替换原文件。
