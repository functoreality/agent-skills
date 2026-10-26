# 独立评审、LLM 评判与反馈可靠性

抓取日期：2026-10-26。只收集事实及候选机制，未修改正式 Skill、安装软件或运行外部项目。

## 检索与读取

- 已读当前 `task-final-review/SKILL.md` 与 `references/independent-review.md`。
  已有上下文隔离、按视角给材料、问题与方案分开、批判处理反馈、非票决、修订后验证等机制。
- 实际英文查询包括 `Judging LLM-as-a-Judge MT-Bench Chatbot Arena position verbosity self enhancement bias paper`、
  `Large Language Models Cannot Self-Correct Reasoning Yet 2023 intrinsic self correction paper`、
  `CriticBench evaluating large language models as critic critique correction feedback 2024 paper`、
  `CriticEval Evaluating Large Language Model as Critic 2402.13764 critique feedback refinement meta feedback correctness helpfulness`、
  `Inspect AI model grading scorer manual validation model judge evaluation documentation`。
- 按 arxiv-download Skill，先读官方 HTML，再用页内检索和分段读取核查方法、结果及局限。
  八项来源均取得正文相关章节，HTML 可定位到参考文献或附录，未以摘要代替正文。
  未下载 PDF，未实际复现实验，工具现行行为依据官方文档而非本地测试。
- 发现了 GitHub 读取连接器，但本路线没有采用仓库文件作实质证据，因此未调用仓库接口。
  实验主要来自 2022–2024 年，不能直接代表 2026 年所有模型的能力。

## 来源卡片

### E01 · Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

- 作者：Lianmin Zheng 等，UC Berkeley 等。版本：v4，2023-12-24。
  [原文](https://arxiv.org/html/2306.05685v4)，重点 §3.3–3.5、§4、附录 D。
- **评测支持**：GPT-4 在所测偏好任务与人类有较高一致性，但存在位置和冗长偏差。
  原文没有将自偏好确认为普遍结论。数学小样本中，先独立生成参考答案再评判，
  误判从 14/20 降至 3/20，仍非零。少样本示例提高一致性，却未提高与人的一致程度，成本约四倍。
- **机制**：必要时交换候选顺序，两序矛盾则保留未决。多轮问题须提供足以消解指代的相关对话。
  **边界**：一致不等于正确，参考答案也可能错，小样本结果不能推出通用增益。

### E02 · Large Language Models Cannot Self-Correct Reasoning Yet

- 作者：Jie Huang、Xinyun Chen 等，Google DeepMind / UIUC。版本：v2，2024-03-14。
  [原文](https://arxiv.org/html/2310.01798v2)，重点 §3–5。
- **评测支持**：所测推理任务中，没有外部反馈的反思经常将正确答案改错。
  作者指出部分既有结果依赖实际不可得的正确性标签、较弱首轮提示，或未对齐推理成本。
  在其等响应数比较中，多 agent 辩论并未胜过自一致性基线。
- **机制**：评价评审收益时同时记录纠错与改错，并使用公平首轮及等成本基线。
  **边界**：这是否定特定旧模型及设置的证据，不能据此宣称自查、多 agent 或所有内生纠错永远无效。

### E03 · LLM Evaluators Recognize and Favor Their Own Generations

- 作者：Arjun Panickssery、Samuel R. Bowman、Shi Feng。版本：v1，2024-04-15。
  [原文](https://arxiv.org/html/2404.13076v1)，重点 §2–3、§5.2。
- **评测支持**：在 CNN/DailyMail、XSUM 摘要任务，所测模型能识别并偏爱自身输出。
  训练干预支持自识别与自偏好的关联和因果解释，作者明确保留尚未排尽混杂因素的局限。
- **机制启示，属于迁移推断**：新会话及隐藏作者身份只隔离会话信息，不能保证模型错误独立。
  关键结论优先补不同来源或不同方法的证据，不把换一个同模型实例当独立事实证据。
  **边界**：论文不证明换模型必然消除共享偏差，也不支持按模型数量或票数担保可靠性。

### E04 · Self-critiquing models for assisting human evaluators

- 作者：William Saunders、Catherine Yeh、Jeff Wu 等，OpenAI。版本：v2，2022-06-14。
  [原文](https://arxiv.org/html/2206.05802v2)，重点 §3.3、§4、§7.2。
- **评测支持**：专门微调的批评模型帮助人类发现摘要中的缺陷。
  对故意误导摘要，预先植入问题的检出率从 27±5% 到 45±5%，有效意见比例未明显下降。
  作者同时发现吹毛求疵、误导性批评及缺乏客观真值，人工评价也会错。
- **机制**：区分问题真实性、严重度及反馈可用性。评审有效性看有效且重要的问题检出，不能只数意见。
  **边界**：这是模型辅助人评的概念验证，不能等同普通提示词式 agent 评审的稳定效果。

### E05 · CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing

- 作者：Zhibin Gou、Zhihong Shao、Yeyun Gong 等，清华 / Microsoft。版本：v4，2024-02-21。
  [原文](https://arxiv.org/html/2305.11738v4)，重点 §3–4、附录 D.2、D.6。
- **评测支持**：利用检索、Python 执行等反馈改写，若干问答与程序合成任务优于无工具消融。
  收益随模型、任务变化，也有下降项。附录明确观察到本来正确的输出被错误修订。
- **机制**：争议问题优先转为可执行核验或可追踪原始来源检查，证据与结论一起保存。
  **边界**：工具提供的是局部观测。执行成功不证明题意正确，检索文本也不自动真实，反馈解释仍可能错。

### E06 · Training Language Models to Self-Correct via Reinforcement Learning

- 作者：Aviral Kumar、Vincent Zhuang、Rishabh Agarwal 等，Google DeepMind。
  版本：v2，2024-10-04。[原文](https://arxiv.org/html/2409.12917v2)，重点 §4–7。
- **评测支持，亦为 E02 的能力边界补充**：SCoRe 通过专门多轮 RL 训练取得正向内生纠错。
  MATH 中其首轮到第二轮净增 4.4 个百分点，正确答案被改错比例亦降低。
  这依赖训练设置及有可验证奖励的任务，并非仅添加一句“再检查”。
- **适配较弱**：不建议为收尾 Skill 引入训练流程。可迁移的是按当前模型、任务实际校准，
  避免把早期负结果写成永久禁令。该文未训练超过一轮纠错，多轮收益没有同等支持。

### E07 · Inspect 官方模型评分与评分政策

- 机构：UK AI Security Institute。读取现行网页，未取得页面提交或发布日期。
  [Model Grading](https://inspect.aisi.org.uk/model-graded.html)、
  [Scoring Policy](https://inspect.aisi.org.uk/scoring-policy.html)。
- **官方工具机制，未在本机试跑**：评分模板分开任务、回答、标准和指令，可按需提供历史。
  评分器可能回退到被测模型，因此需显式配置评判模型。
  无法解析评判结论应保留为未评分，而非判产物失败或通过。文档也区分运行错误与产物错误。
- **可迁移**：保存评判器配置及原输出，争议项追踪到对应证据，必要时查看重复评分差异。
  文档明确温度零也不保证完全一致。多模型多数表决只是工具功能，没有单独证明质量可靠。

### E08 · CriticEval: Evaluating Large Language Model as Critic

- 作者：Tian Lan、Wenwei Zhang、Chen Xu 等，上海人工智能实验室 / 北京理工大学。
  版本：v5，2024-10-20。[原文](https://arxiv.org/html/2402.13764v5)，重点 §4–6、附录 H。
- **评测支持**：区分反馈、比较、修订、反馈的反馈。人工校验的参考批评可改善所测模型与人评的相关性，
  仍未达到人类一致程度，且依赖该批评基准及参考质量。
- **机制**：反馈也要检查漏报、误把正确内容判错、反馈本身错误、重复无关及修订引入错误。
  原文在人评中复核题目与标准答案，排除错误基准。不能把参考答案或另一位裁判视作真值。
  **成本与局限**：需要人工标注与校准，对中文和 tool-use 的迁移不能从英文既有任务直接推定。

## 面向当前 Skill 的候选机制

以下是本路线推断，尚未决定采纳，不是论文已经验证的通用工作流。

| 候选 | 具体做法、失败模式与成本 | 与当前 Skill 的关系及依据 |
|---|---|---|
| 证据独立性提示 | 高影响判断优先原始来源、运行结果、独立重算，避免同模型重述同一错误。成本按风险决定 | 上下文隔离已覆盖，可补“隔离不等于证据独立”。[E03](https://arxiv.org/html/2404.13076v1)、[E05](https://arxiv.org/html/2305.11738v4) |
| 可复核的问题单 | 问题附位置、触发条件或证据、影响及已知不确定性。把可验证缺陷与偏好分开。无需统一复杂严重度体系 | 已有位置、影响、理由及核实反馈，可补最小复现证据。[E04](https://arxiv.org/html/2206.05802v2)、[E08](https://arxiv.org/html/2402.13764v5) |
| 材料充分性检查 | 最小上下文仍须包含判断所需标准、来源或有依赖的对话，缺材料则不能定错。只排除作者预判，不排除必要事实 | 两类评审材料差异已覆盖，可提醒避免把盲评理解成信息不足。[E01](https://arxiv.org/html/2306.05685v4)、[E07](https://inspect.aisi.org.uk/model-graded.html) |
| 争议转为核验问题 | 双方分歧拆成事实冲突、标准解释、取舍偏好，再选能裁决的来源或实验。无法裁决则保留未决及影响 | 已有证据裁决、不按票数及拒绝修改理由。分类为操作化推断，可能只需一例，无需新阶段。[E05](https://arxiv.org/html/2305.11738v4)、[E08](https://arxiv.org/html/2402.13764v5) |
| 比较时检查顺序敏感 | 对影响决策且差距小的比较交换顺序，结论变化则降低把握。重复约两倍成本，勿常规应用于全部评审 | 适合比较评估参考，静态单稿核验适配弱。[E01](https://arxiv.org/html/2306.05685v4) |
| 反馈质量校准 | 要复用自动评判流程时，用少量已知正确及有代表缺陷样本试评，检查误报和漏报。一次性小任务无需建评判基准 | 新增范围应限可复用评分器，不能每项任务多做一套评审。[E04](https://arxiv.org/html/2206.05802v2)、[E08](https://arxiv.org/html/2402.13764v5) |
| 检查修订净效果 | 关注修了什么、是否把正确内容改错，必要时保留修订前证据或样例。不要以修改量、意见数当收益 | 已有修订验证及不破坏约束，主要是补反例依据。[E02](https://arxiv.org/html/2310.01798v2)、[E06](https://arxiv.org/html/2409.12917v2) |
| 评判失败单独保留 | 资料不足、不可解析、运行失败分别记录，不把低覆盖下的少量通过包装成整体通过 | 当前已有未执行/无法判断，可借官方工具作说明例。[E07](https://inspect.aisi.org.uk/scoring-policy.html) |

## 去重、未收录与证据空缺

- 搜索出现第三方论文总结、媒体报道及综述，只作为发现线索，未用作事实证据。
- CriticBench 与 CriticEval 不是同一材料，另有曾使用 CriticBench 名称的旧稿。
  本报告采用 E08 正式命名及 arXiv v5，不叠算同系列稿件为多次独立验证。
- 未把“更多 agent”“换模型”“多数同意”“更多意见”“最终评分提高”当可靠性保证。
  E02 的等成本对照、E04 的有效意见核验及 E08 的错误分析比人数本身更接近目标。
- 未找到可证明当前 Skill 的四轮上限或固定人数最优的证据，也未找到跨领域通用的最小上下文长度。
  不应借本路线把这些工程选择包装成实验结论。
- E01、E04、E08 的“人类一致”依赖具体标注者、任务及评估协议，不等于客观正确。
  公开数据/代码有助复查，不代表本轮已经完成独立复现。
