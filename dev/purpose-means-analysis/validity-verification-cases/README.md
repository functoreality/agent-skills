# CCA / PMA 案例检验

三题试点、T07复盘、第一轮7道新题及全量题干保真复核已完成。
采用小批滚动检验，当前已暂停等待用户确认，两个Skill未修改。

本目录公开纯文本的题答摘要与分析，完整PDF、OCR和截图保存在忽略的`_private/`。
本地材料路径及公开副本的使用方式见[参考材料说明](sources/README.md)。

- **[205条题干保真复核](input-audit/README.md)**：未来按原文包准备输入，旧摘要不再直接试解
- [已试10题的信息差与结果限制](input-audit/existing-trials.md)
- **[第一轮7题汇总入口](batches/round-01/README.md)**
- **[候选观察台账](learnings/README.md)**
- [三题试点汇总](pilot/summary.md)
- [方法层面的初步观察](pilot/method-observations.md)
- **[T07的B类复盘完整示范](retrospectives/T07/README.md)**：两项候选指令与跨领域正反例推演，未做盲试
- [题目索引](inventory/questions.md)
- [原书解答索引](inventory/answers.md)
- [迭代计划](planning/plan-v2.md)与[阶段状态](planning/status.md)
- [三题收尾核验](reviews/pilot-review.md)
- [公开目录整理](reviews/publication-review.md)
- [原书PDF补充核验](reviews/pdf-supplement-review.md)：19页定点核对，三题分类不变

索引共有205条规范化记录，其中69道编号题、128条无编号实例、8条变体。
169条找到解答或部分解法，36条未定位。第60题在所给文本中未见编号。
这些条目不等于205个条件完整、互相独立的盲解测试样本。

试点结果：T04、T31在答案前核心命中，另附自报熟悉度备注；T07为B。
[工具日志核对](reviews/workflow-audit.md)确认三题均在冻结后才读取本次参考答案。
熟悉度自述不能证明记忆召回，方法对先前联想的贡献仍需单独判断。
T07的后验调整及执行遗漏在报告中逐项记录，未认定方法不适用。

## 复验与溯源

运行 `python3 scripts/build_inventory.py` 重建题解索引，
运行 `python3 scripts/check_artifacts.py` 检查公开文件、链接与候选指纹。
有私有材料时加`--with-private`核验原文与归档，发布前加`--history`检查本目录历史。
公开模式会明示跳过未分发资料，不将这些检查记为已通过。
T60是保留的来源提示，不代表脚本漏检。

- [原始需求](prompt.txt)
- [当前小批解题协议](protocols/batch-solver.md)与[原试点协议](protocols/solver.md)
- [资料提取协议](protocols/extraction.md)
- [来源及Skill版本指纹](sources/manifest.json)
- [答案前冻结指纹](pilot/freeze.json)
- [计划核对](reviews/plan-review.md)、[索引核对](reviews/inventory-review.md)

后续仍按每轮6至7题滚动检验，先检查[题干包规则](protocols/question-packets.md)，
每轮提供按案例、按方法的短汇总后停止等待用户。
[本轮入口](batches/round-01/README.md)与[候选观察台账](learnings/README.md)。
T07-H1/H2继续观察，尚未写入Skill。
