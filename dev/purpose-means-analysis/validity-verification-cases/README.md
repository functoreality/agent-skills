# CCA / PMA 案例检验

前三步已完成，当前等待用户审核三题试点。
尚未启动全量试解，两个 Skill 未修改。

- **[三题试点汇总与审核入口](pilot/summary.md)**
- [方法层面的初步观察](pilot/method-observations.md)
- [题目索引](inventory/questions.md)
- [原书解答索引](inventory/answers.md)
- [执行计划](planning/plan.md)与[阶段状态](planning/status.md)
- [三题收尾核验](reviews/pilot-review.md)

索引共有205条规范化记录，其中69道编号题、128条无编号实例、8条变体。
169条找到解答或部分解法，36条未定位。第60题在所给文本中未见编号。
这些条目不等于205个条件完整、互相独立的盲解测试样本。

试点结果：T04、T31为A-memory，T07为B。
两道核心命中均有记忆风险，本轮没有干净的独立推导成功证据。
T07的后验调整及执行遗漏在报告中逐项记录，未认定方法不适用。

## 复验与溯源

运行 `python3 scripts/build_inventory.py` 重建题解索引，
运行 `python3 scripts/check_artifacts.py` 检查引用、链接与冻结指纹。
T60是保留的来源提示，不代表脚本漏检。

- [原始需求](prompt.txt)
- [统一解题与揭答协议](protocols/solver.md)
- [资料提取协议](protocols/extraction.md)
- [来源及Skill版本指纹](sources/manifest.json)
- [答案前冻结指纹](pilot/freeze.json)
- [计划核对](reviews/plan-review.md)、[索引核对](reviews/inventory-review.md)

审核同意后继续全量队列，再生成按案例、按方法组织的两份最终总领文档。
