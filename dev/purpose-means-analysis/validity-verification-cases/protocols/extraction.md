# 例题与答案提取协议

任务是建立可追溯索引，不是试解，不作方法有效性判断。
仅处理分配的原文文件，逐页通读，可分段读取，rg 用于定位、交叉回查。

## 范围

- 收录所有明确编号“课题”，保留原编号及 OCR 原样疑点。
- 也收录无编号的实质问题实例，包括技术发明、侦探谜题、心理实验、
  标准解法中的具体实例、反例和边界例子。
- 泛泛的技术名称、没有问题与解法的历史列举可排除，但须记录范围。
- 同一实例重复讲解只设一条主记录，变体或约束变化单列子项。
- 不把理论步骤、分类条目误当例题编号。

## 输出

写入 inventory/part-N.json 和 inventory/part-N-notes.md，仅写分配文件。
JSON 为数组，每项包含：
`id`（编号题用 T01 等，无编号用 U1-001 等）、`original_label`、`title`、
`kind`（numbered/unnumbered/variant）、`statement`（完整保留关键约束的中文摘要）、
`question_refs`（数组，每个是 {file,line_start,line_end,page}）、
`answer`（原书解法摘要，未发现用 null，勿自己补解）、
`answer_refs`（同格式）、`keywords`（数组）、`uncertainties`（数组）、
`related_ids`（数组）。所有 file 用相对当前案例目录的私有原文路径，统一以`_private/references/altshuller/`开头，页码采用 ## Page 标记。
某题仅在本部分有答案而题干在别处，仍记录同一 T 编号，statement 写 null。
跨文件无法确认时标待配对，主 agent 负责合并。多个书中解法均须记录。
文字保持简洁，但题干摘要不能泄露只在答案中出现的巧思。
notes 记录已通读页段、漏页/图示/OCR 障碍、排除类型、建议的 3 题试点候选。
不要创建子 agent，不要读其他 Agent 的结果，不要修改 Skill，不要 git commit。
