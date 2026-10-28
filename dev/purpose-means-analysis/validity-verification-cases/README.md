# CCA / PMA 案例检验

前三步已完成，当前等待用户审核三题试点。
尚未启动全量试解，两个 Skill 未修改。

本目录公开纯文本的题答摘要与分析，完整PDF、OCR和截图保存在忽略的`_private/`。
本地材料路径及公开副本的使用方式见[参考材料说明](sources/README.md)。

- **[三题试点汇总与审核入口](pilot/summary.md)**
- [方法层面的初步观察](pilot/method-observations.md)
- [题目索引](inventory/questions.md)
- [原书解答索引](inventory/answers.md)
- [执行计划](planning/plan.md)与[阶段状态](planning/status.md)
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
- [统一解题与揭答协议](protocols/solver.md)
- [资料提取协议](protocols/extraction.md)
- [来源及Skill版本指纹](sources/manifest.json)
- [答案前冻结指纹](pilot/freeze.json)
- [计划核对](reviews/plan-review.md)、[索引核对](reviews/inventory-review.md)

审核同意后继续全量队列，再生成按案例、按方法组织的两份最终总领文档。
