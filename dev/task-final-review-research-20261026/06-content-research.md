# 内容、研究与读者核验调研

抓取日期：2026-10-26。只收集候选机制，未改 Skill，未安装或运行外部项目。

## 范围、查询与限制

已读当前 `task-final-review/SKILL.md`、`content-and-presentation.md`
及 `behavioral-and-comparative.md`。重点是事实、来源、推理与实际理解，
不研究润色语气，也不重做独立 LLM 评判路线。

实际查询包括：

- `site.fullfact.org how we fact check sources claims methodology`
- `site.nist.gov technical documentation usability testing users task success`
- `site.gov.uk guidance content design usability testing content users tasks`
- `site.aclweb.org FActScore fine grained atomic evaluation factual precision text generation`
- `site.aclanthology.org "Enabling Large Language Models to Generate Text with Citations"`
- `site.cia.gov "Analysis of Competing Hypotheses" "inconsistent"`
- `site.gov.uk "content" "testing" "comprehension" "find"`
- `site.cdc.gov "Clear Communication Index" "research-based"`
- `"Effects of task structure and confirmation bias in alternative hypotheses evaluation" authors doi`
- `"Effects of task structure" "military" "2024" confirmation`

使用 web 打开机构原页和论文原文。ALCE 仓库按约定用 GitHub 连接器读取。
论文 PDF 采用已读取的 PDF Skill，通过 web 文本提取读取方法及限制，未大量看图。
Full Fact 原页返回 410，PMC 原文访问触发验证码，后者已改从出版商读全文。

## 来源卡片

### C01：FActScore

- 原作者：Sewon Min 等，EMNLP 2023，2023-12。
- 原文：[论文](https://aclanthology.org/2023.emnlp-main.741.pdf)。
  已读方法、标注示例及 limitations，重点 §3、附录 A、印刷页 12084–12085。
- 机制：把复合句拆成单一可核查信息，逐项判断指定知识源是否支持。
  整句或整篇“正确/错误”会掩盖真假混合。
- 证据：有人工标注与自动估计评测。研究对象主要为人物传记和 Wikipedia。
  文中的低误差是总体分数估计，不能解释成每条事实可靠率接近 100%。
- 限制：不测信息遗漏，删除难证实内容可能提高精确率却降低回答价值。
  作者明确限制了争议性事实、冲突知识源及复杂暗示的适用性。

### C02：ALCE，引文质量评测

- 原作者：Tianyu Gao、Howard Yen、Jiatong Yu、Danqi Chen，EMNLP 2023。
- 原文：[论文 §3.3、§6、附录 E–G](https://aclanthology.org/2023.emnlp-main.398.pdf)。
  [作者仓库](https://github.com/princeton-nlp/ALCE) README 通过连接器读取成功，
  文件 SHA 为 `b629ec7029b7cbb697bcc1675fa2ce5e1adb6d9f`，未执行代码。
- 机制：分别测正文声明是否获引文完整支持，以及所附引文是否相关。
  多个来源可共同支持一句，单个链接与主题相关仍可能不支持具体声明。
- 证据：有数据、代码及人工评测。自动评测与人工的 citation recall、precision
  一致性 kappa 分别为 0.698、0.525。
- 限制：自动 NLI 对部分支持可能误判。来源支持度和事实正确性需分开判断，
  有引文不能证明来源可靠，也不能证明答案完整。

### C03：AFP 事实核查实际工作流

- 机构：Agence France-Presse。
- 原文：[How we work](https://factcheck.afp.com/How-we-work)，已读全文。
  页面未见可靠更新日期，不能以页脚年份充当版本。
- 机制：核对中心声明的独立证据，追原始研究及方法，检查数据是否被误解，
  识别真实成分与错误语境，展示可供读者重走的证据路径。
- 证据类型：机构陈述的实际编辑工作流，并列出实地核验案例，未提供效果对照。
- 限制：其“两独立来源”是新闻机构规范，不宜转成每个任务的硬门槛。
  专家联络、实地调查超出一般收尾检查的成本与授权。

### C04：竞争假设与关键证据敏感性

- 原作者：Richards J. Heuer, Jr.，CIA，1999。
- 原文：[Psychology of Intelligence Analysis](https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf)，
  已读第 8 章相关步骤，重点印刷页 103–106。
- 机制：比较可行解释，区分能鉴别解释的证据与“都说得通”的证据。
  对真正驱动结论的少数证据或假设，问若错误、误导或另解，结论是否改变。
- 证据类型：作者的方法论及机构出版，不是对整套流程有效性的随机评测。
- 限制：原作者也说矩阵只是辅助，不可机械以正负数量决定结论。
  完整 ACH 成本高，效果还须结合 C05 判断。

### C05：ACH 特定结构的反向证据

- 原作者：Mandeep K. Dhami 等，2024-06-13，Cognitive Research。
- 原文：[Effects of task structure and confirmation bias in alternative hypotheses evaluation](https://link.springer.com/article/10.1186/s41235-024-00560-y)，
  已读研究设计、讨论及局限。PMC 验证码未绕过。
- 结果：研究一 N=161，经典 ACH 矩阵结构未体现预期的确认偏差收益，
  调转行列的结构在该实验中较好。研究二涉及 62 名荷兰军事分析员。
- 限制：作者明确只检验 ACH 的某个特征，并非完整 ACH 的总体效果。
  任务是两个假设、12 项证据，未预注册，不能推出所有反例检查无效。
- 候选含义：不能因方法出自权威机构便认定整套流程值得移植。
  保留“核查关键假设”的候选，与复制矩阵、反证计分法分别判断。

### C06：真实任务的观察式测试

- 机构：GOV.UK Service Manual，User research community。
- 原文：[Using moderated usability testing](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing)，
  已读任务设计、执行和数据/设备条件，页面版本日期未确认。
- 机制：选择实际或潜在用户，给可信的目标任务，指令不能泄露答案或路径。
  观察动作和思考，少解释少引导，对已观察的障碍再追问。
- 证据类型：政府服务的使用指南，方法本身未在该页做对照评测。
- 限制：假数据和不匹配设备会减少情境问题的发现。
  人类用户测试与 AI 模拟读者不能等同。

### C07：把“觉得清楚”与理解答案对照

- 机构：英国 Department for Education，2025-09-25。
- 原文：[Application sharing content testing](https://becoming-a-teacher.design-history.education.gov.uk/apply-for-teacher-training/application-sharing-testing/)，
  已读三轮方法、结果及方法限制。
- 实践：919 人回收的高亮测试后加理解题，再用 5 人非主持测试、8 人主持测试追因。
  一个关键可见性规则有 61% 回答错误，说明满意或自报理解不足以验收。
- 证据类型：真实服务团队公开的工作记录，具有失败发现证据，
  没有证明某次改写造成最终成功率提升。
- 限制：样本自选，非主持环节存在原型滚动、浏览器及设备障碍。
  团队承认这会干扰内容理解结论，不把测试失败全归因于文本。

### C08：CDC Clear Communication Index

- 机构：CDC，User Guide 版本为 2019-08。
- 原文：[完整指南](https://www.cdc.gov/ccindex/pdf/clear-communication-user-guide.pdf)，
  已读用途与边界、数字和风险部分。
- 机制：以目标读者、行为目标和主消息为前提，检查科学状态、行动说明、
  数字和风险。包括比较保持分母一致、提供绝对风险、避免只写“高/低”。
- 证据类型：以研究为依据的机构工具，本次未独立审计其全部支撑文献。
- 限制：健康传播专用，不能把它的 20 项评分、90 分阈值通用化。
  指南明确说评分不能替代目标读者的预试，短句可读性也不能替代有效理解。

## 可迁移机制与当前覆盖

下表“补充”仅表示存在候选细化空间，并非建议一定采纳。

| 候选机制 | 针对失败、操作及适用成本 | 与当前 Skill 的关系 |
|---|---|---|
| 高影响复合声明拆项 | 对主要结论或数字句拆成可核查断言，避免同句部分真掩护部分假。仅查关键句，控制原子化膨胀。[C01](https://aclanthology.org/2023.emnlp-main.741.pdf) | 已有优先关键事实，但未明示句内拆项，可能补充 |
| 正文到证据、引文到正文双向核对 | 问每项关键断言是否完整获支持，再问每个引用支持哪一部分。允许多个来源共同支持，不强制最少引用。[C02](https://aclanthology.org/2023.emnlp-main.398.pdf) | 已有原文支持核查，双向分离可作为操作示例 |
| 来源独立性和语境检查 | AFP 要求中心声明有独立证据并查原始方法。据此推断：多篇转载不应算多份证据，需要时追共同上游。[C03](https://factcheck.afp.com/How-we-work) | 语境/原始研究已覆盖，来源依赖关系尚未具体说明 |
| 关键假设敏感性 | 先定位一两项决定性证据，尝试删除、改判或换解释，看结论是否逆转，再定核查优先级。适合研究综述和方案选择，非每段必做。[C04](https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf) | 已有反例和独立推导，候选是明确如何找到最值得查的前提 |
| 带可判定答案的读者任务 | 让读者实际找信息或处理一个新情境，记录其答案、路径和阻塞，再和事先确定的正确结果比对。不能把标准答案交给读者。[C06](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing) | 代表性任务与隔离已充分覆盖，可细化“理解”如何落到观测 |
| 自报理解与实际理解交叉验证 | 对关键规则给少量判断或应用题，再追问错因。偏好评分和“看懂了”不能独自验收。[C07](https://becoming-a-teacher.design-history.education.gov.uk/apply-for-teacher-training/application-sharing-testing/) | 明显可补充示例，不必引入整套问卷或招募流程 |
| 量化内容的可解释性 | 核对时间范围、分母、绝对量与比较基准，让读者正确解释数值和后果，不能止于数字算对。[C08](https://www.cdc.gov/ccindex/pdf/clear-communication-user-guide.pdf) | 已有单位范围一致，面向读者的数值解释可能补充，专业情境按需 |

自己的推断：可用极轻的“关键断言、证据位置、支持范围、未决差异”记录，
将上述核验并入既有对应关系，不必新增强制全篇声明表。
高精确率和完整回答应分别核对，不能以删减所有难点换取“事实全对”。
这个提醒直接受 C01 的信息召回局限启发，当前需求覆盖机制已有相当基础。

## 去重、未收录与审慎边界

- [Full Fact](https://fullfact.org/about/how-we-fact-check/) 搜索可见机构方法，
  打开原文返回 410，未用摘要替代正文，故不作为正式来源卡片。
- [FactCheck.org Our Process](https://www.factcheck.org/our-process/) 与 AFP 的原始来源、
  逐句核验及编辑分工重叠，未为凑数量重复收录。
- NIST usability 页面与 C06 的代表用户/代表任务重复，没有额外收录。
- ALCE 论文和仓库属于同一机制，合并为 C02，不当作两份独立效果证据。
- 不收完整 ACH 为通用流程。C05 是对特定结构的限制证据，
  不是“任何竞争解释分析均无效”的证据。
- 未展开 Chain-of-Verification，避免重复独立评判路线。
  这里的重点是外部原文支持、可复查断言及读者行为结果。
- 本路线没有发现必须重建当前 Skill 架构的证据。
  多数基础原则已经覆盖，真实增量集中在可执行示例和证据边界。
