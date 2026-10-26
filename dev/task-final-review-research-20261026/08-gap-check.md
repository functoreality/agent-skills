# 补充检索与交叉核对

检索日期：2026-10-26。此阶段只记录发现，不决定整合。

## 范围与查询

- `agent completion verification checklist evidence review skill task final review agentic engineering`
- `site.simonwillison.net agentic engineering manual test review code tests`
- `AI agent review verification completion AGENTS.md CLAUDE.md checklist non coding`

优先检查跨路线遗漏和原作者实践，排除只有搜索摘要、转载或宣传的材料。

## R01：Agentic manual testing

- 作者：Simon Willison，直接读取作者网页。
- 原文：[Agentic manual testing](https://simonwillison.net/guides/agentic-engineering-patterns/agentic-manual-testing/)。
- 机制：在测试套件之外，从实际入口运行程序或浏览器操作，观察真实输出。
  让工具记录实际命令及其输出，而不是事后由模型重写“应该发生”的结果。
- 针对：套件通过却不能启动、关键界面缺失，以及演示记录与实际执行脱节。
- 证据等级：作者维护工具和工作流的经验，不是受控普遍有效性评测。
- 当前关系：实际试用及命令记录已覆盖，真实入口与模拟边界值得进一步核对。
- 限制：作者倾向普遍要求执行测试，不能直接扩展为所有文档或微小修改的硬性要求。

## R02：Your job is to deliver code you have proven to work

- 作者：Simon Willison，2025-12-18，直接读取作者网页。
- 原文：[code-proven-to-work](https://simonwillison.net/2025/Dec/18/code-proven-to-work/)。
- 机制：从已知初始状态触发改动，观察预期结果，并提供可复现证据。
  回归测试应能在撤回实现时暴露原缺陷。
- 针对：把未测试代码交给评审者，以及测试永远通过但不能区分修复前后的情况。
- 当前关系：独立预期、实际试用已覆盖，回归测试的辨别能力值得补充。
- 限制：不继承文章对所有改动必须同时手动和自动测试的绝对要求。

## R03：What to look for in a code review

- 机构：Google Engineering Practices，直接读取官方页面。
- 原文：[looking-for](https://google.github.io/eng-practices/review/reviewer/looking-for.html)。
- 机制：审查测试是否真的能发现错误，结合周围实现理解 diff，
  对行为变化同步核对文档，区分必要修正与风格偏好，并明确自己的审查范围。
- 针对：测试与实现共同犯错、局部改动脱离上下文，以及说明与实际行为不一致。
- 当前关系：避免过度工程化与按范围评审已覆盖。
  变更整体检查及测试有效性可以作为更明确的核验问题。
- 证据等级：机构工程标准，不能据此推定每个项目都必须采用相同细则。

## 未直接作为证据的线索

- Agent Engineering Handbook 的 output verification 搜索结果与目标高度相关，
  直接打开返回缓存抓取失败，已交给 Skill 路线补查原站或原仓库。
- 企业治理型 completion contract 的搜索摘要包含多层控制器、固定证据等级，
  暂不以摘要认定机制成熟或适配，优先由跨路线结果核对是否有低复杂度可迁移部分。
- AI 工作流和编码代理的新闻、播客摘要及二次总结仅用来找原始来源，
  未将其列作独立证据。

## 中文补充检索

- `"CLAUDE.md" "验收" "验证"`
- `"AGENTS.md" "完成" "测试" "检查"`
- `"AI" "交付" "验收" "skill" "验证"`

找到腾讯微信的专用验证 Skill，交由数据与操作路线读取原始执行规范。
找到 `sdsrss/agentsmd`，交由真实工程指令路线核对。
个人教程中常见的运行相关测试、检查 diff、报告未验证项与当前基线重叠较多，
未将转载或同类模板分别计作新机制。

## R04：Product Delivery Skill

- 作者：qierkang，读取公开仓库 README、根 SKILL、质量门禁文档和实际脚本。
- 来源：[quality-gates.md](https://github.com/qierkang/product-delivery-skill/blob/master/shared/references/quality-gates.md)
  与 [stage-gate.py](https://github.com/qierkang/product-delivery-skill/blob/master/shared/scripts/stage-gate.py)。
- 读取的脚本 blob：`188721b2859ebda2e1ace610b54e0feabe57cad6`。
- 机制：用需求到交付的阶段产物和状态文件跟踪完成情况，明确记录未通过阶段。
- 核实限制：实际脚本主要判断文件存在、长度、标记字符串及 JSON 字段，
  没有据此运行或核实质量规范中列出的全部业务测试和人工判断。
  因此门禁通过只能支持其实际实现的结构检查，不能证明完整交付质量。
- 当前关系：阶段缺口可作为需求覆盖的补充，
  但固定九阶段、二十多种模板、全局门禁依赖和发布审批不适合本 Skill。
- 证据等级：作者公开实现及样例说明，未独立运行其完整工作流。

## 补充检索收敛检查

七条路线完成后再次查询：

- `"skill" "output verification" "artifact" "completion"`
- `"agent" "verification" "no tests" "skipped" completion evidence`
- `"final review" "skill" "requirements" "documents" verification`

新增候选主要仍是新鲜证据、空测试、实际断言、范围检查和评判误报。
补读下面两个原作者材料，没有发现需要改变现有按需架构的新机制。
同名 superpowers 分叉、安装目录、示例评审面板不按新原创机制重复计数。

## R05：验证“缺证据”检测器本身的误报

- 作者：Vitalii Serbyn，2026-10-22。
- 原文：[proof-of-green 自查](https://serbyn.io/blog/proof-of-green-checks-every-done)。
  直接读取完整正文，包括限制段落。
- 经验：固定识别测试命令和“完成”措辞的规则，会漏掉 wrapper、直接运行的测试，
  也会把文档核验或故意失败的测试误记为缺证据。
- 作者先观察再复核，最终认为保留运行记录比普遍弹警告更有价值。
- 重要限制：复核主要由同类模型完成，作者明确尚未亲自复查全部样本。
  抽样跨时间窗口，不能把标题中的比例当作稳定准确率或普遍统计。
- 当前关系：支持已有的检查适配性与误报分析，不据此安装 hooks 或引入自动完成门禁。

## R06：Task executor 的实际断言与终态区分

- 原作者项目：shinpr / claude-code-workflows。
- 原文：[task-executor.md](https://github.com/shinpr/claude-code-workflows/blob/main/agents/task-executor.md)。
  读取完成协议、验证环境和最终核对段落，未通读前置全部责任定义。
  blob `161d9263a0462578685d003ac22cb5a9b138990b`。
- 机制：只有真正执行了与交付行为有关的断言，才把测试记通过。
  零测试、TODO 用例和恒真断言不构成证据，验证预期为空的实质断言仍可以有效。
  实现完成和最终验收完成分开，执行受限需明确受影响结论。
- 当前关系：与空测试、检查覆盖和状态说明已有原则重叠，
  可补测试有效性的具体例子，不复制其固定 JSON 协议和多阶段质量组织。
- 证据等级：公开工作流规则，未运行或独立评测其效果。
