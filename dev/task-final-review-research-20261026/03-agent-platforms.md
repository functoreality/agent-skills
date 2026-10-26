# Agent 平台与工程团队的验证实践

抓取日期：2026-10-26。仅收集，没有执行外部脚本、安装或修改 Skill。
已读当前 Skill 主文件及 automated-checks、behavioral-and-comparative 参考。
下文的“候选”是与现有内容的关系判断，不代表决定采纳。

## 范围、检索与证据口径

- 范围：Claude Code、Anthropic 工程实验、Codex 官方工程文章、Cursor、Aider、GitHub Copilot。
- 实际查询包括：`site:developers.openai.com Codex best practices verify tests review`、
  `site:code.claude.com/docs best practices give Claude way verify work screenshots tests`、
  `site:anthropic.com/engineering effective harnesses long-running agents end to end testing`、
  `site:cursor.com/blog agent test verify browser artifacts`、
  `site:aider.chat/docs usage lint test automatic`、
  `site:docs.github.com copilot coding agent screenshots test`。
- 所有收录网页均实际打开，并定位到相关正文。无仅凭搜索摘要收录项。
  OpenAI 部分使用 OpenAI Docs Skill，先官方域名搜索再打开原文。
- 查到 GitHub 连接器，但本路线最终只使用官方网页，没有读取仓库文件。
  OpenAI 两个 `.md` 地址因 web 工具不支持返回类型而失败，已回退 HTML 正文。
- 版本口径：这些是抓取日网页快照，均未固定网页对应提交 SHA。
  不把页面展示的示例软件版本当成当前产品版本。
- 证据分级：M＝官方机制或使用约定，U＝作者报告实际使用，
  C＝有具体比较实例但非充分受控实验，E＝可支持因果推广的系统评测。
  本路线未找到足以列为 E 的材料，产品宣传与作者自述均不升级为 E。

## P01：Claude Code 的可执行完成门槛

- 来源：[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)，Anthropic。
  无页面发布日期。已读“Give Claude a way to verify its work”完整段落及门槛分级。
- 机制（M）：先给可读的检查信号，执行、读结果、修复，再检查。
  门槛可从同一提示中的要求，升级到持久目标或 Stop hook 脚本。
  也可用新的模型上下文尝试反驳结果。要求展示命令、返回或截图等证据。
- 针对失败：模型根据“看起来完成”停止，或只有用户能发现错误。
  证据与断言分离，门槛强度不必一开始就采用 hook。
- 成本与适配：提示要求成本低，持久目标和 hook 有配置与阻塞成本。
  现有 Skill 已覆盖可观察条件和证据。可补充的是：对反复漏跑、
  判断稳定的必要检查，考虑把自然语言要求接入已有自动门槛。
  不宜把所有任务都变成不可结束的强制 gate，这是本报告的适配判断。

## P02：长期任务的功能状态与真实使用路径

- 来源：[Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents)，
  Justin Young / Anthropic，2025-11-26。原 engineering 地址重定向至 research。
  已读功能表、测试、启动核验与局限段落。
- 机制（U）：功能表最初均标未通过，附可执行步骤，验证后改状态。
  限制 agent 随意改验收定义。新会话先读状态并检查基础应用仍能运行。
  单元测试与 curl 通过仍可能漏掉整条用户流程，故显式要求浏览器操作。
- 作者观察：浏览器工具帮助发现仅读代码不明显的缺陷。
  但 Puppeteer 看不到原生 alert 等界面，工具的观察范围本身会留下盲点。
- 成本与适配：功能表和状态同步有维护成本。当前 Skill 已覆盖真实组合路径、
  用户试用与缺口说明。候选补充是明确检查“验证工具是否能观察关键结果”。
  不照搬作者为大应用列 200 多功能的规模，也不为收尾额外扩充用户需求。

## P03：验收合同、跨层核验与评审成本的实测反思

- 来源：[Harness design for long-running application development](https://www.anthropic.com/research/harness-design-long-running-apps)，
  Prithvi Rajasekaran / Anthropic Labs，2026-03-24。
  已读架构、比较实例、QA 校准和简化过程。
- 机制（U/C）：实现前把高层需求展开为可测试的 sprint contract。
  评估者用 Playwright 操作运行中的应用，并查 API 与数据库状态。
  以逐项失败反馈约束修复，避免只判断外观或代码表面。
- 具体使用证据：报告了矩形填充、删除实体、路由顺序等缺陷。
  QA 起初会发现缺陷又自行淡化，作者通过阅读日志和校准提示调整。
  多轮审美评分也可能提高复杂度，最终轮未必是作者最喜欢的一轮。
- 成本与适配：早期生成与评价需多小时。换更强模型后，作者移除 sprint，
  将逐 sprint 评估改为末尾一次，认为容易任务的评估已成为开销。
  这些是少量作者实验，不证明普遍最佳架构。
- 当前 Skill 已强调按收益选择独立评审。可补充的具体例子是：
  用户操作成功还需确认对应持久状态，以及必要时提前明确验收口径。
  后者不是默认新建 planner 或增加全套 sprint 流程。

## P04：Codex 修复循环的剩余差异与停止条件

- 来源：[Build iterative repair loops with Codex](https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex)，
  Shreekant Agrawal / OpenAI，2026-05-11。
  已读 review、validation、record 和停止策略，示例固定 Codex CLI 0.130.0。
- 机制（M/演示）：review 输出结构化候选问题，repair 修改副本，validate 执行检查。
  每轮保存问题、修改、执行与判定结果、remaining_delta，下一轮依据剩余差异。
  通过项可停止，生产循环应在通过、达到次数、差异停滞或需要人决策时停止。
- 证据限制：三份故意变旧的 notebook 按预设深度分别在一、二、三轮通过。
  是教学夹具演示，不能当成自然任务上三轮收敛的评测。
- 成本与适配：结构化记录、API 与执行环境增加成本。
  现有 Skill 有复核和重审上限。可补充的是记录“本轮还剩什么、
  是否正在减少”，避免每轮重新做全量泛评或仅凭修改次数宣称进步。
  无需照搬 JSON 框架，也不能据此绕开现有独立评审最多四轮。

## P05：Codex 工程实验中的里程碑与交接记录

- 来源：[Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex)，
  Derrick Choi / OpenAI，2026-02-23。已读实验设置、运行文件分工、验证及结果限制。
- 机制（U）：规格明确目标，计划列里程碑和验收条件，执行说明约定每阶段验证。
  持续记录状态、决策、启动与 demo 命令、已知问题，失败先修再推进。
- 使用证据与边界：作者报告 GPT-5.3-Codex 运行约 25 小时、13M tokens，
  每里程碑跑测试、lint、typecheck。作者明确是实验，结果尚非生产就绪。
  全程成本不能解释为验证本身开销，未见组件消融或重复实验。
- 适配判断：当前 Skill 已要求可追溯命令和范围。对长期交付可补充
  “可启动的 demo/最短复验路径”，四类 Markdown 文件本身不是必要机制。

## P06：Cursor 的可复验运行环境与交付证据

- 来源：[Cursor agents can now control their own computers](https://cursor.com/blog/agent-computer-use)，
  Jonas Nelle、Alexi Robbins / Cursor，2026-02-24。
  补充同一机制的当前 [Capabilities](https://cursor.com/docs/cloud-agent/capabilities) 文档。
  已读公司内部使用实例、artifacts 和 remote desktop 段落。
- 机制（M/U）：在完整隔离环境操作应用，产出视频、截图、日志作为 PR 附件。
  审核者也能接管同一桌面实际复验，无需重新搭建分支环境。
- 使用证据：作者列出逐个点击源文件链接、对有错与无错文件测试动态 lint 文案等实例。
  这些比“已测试”有可检查步骤，但并非受控质量评测。
- 成本与适配：环境配置、录制和存储有成本，长视频也增加审阅负担。
  当前文档说明嵌入 GitHub 的 artifact URL 可无需认证访问，分享前需考虑素材范围。
  候选是按关键行为保留短证据与复验入口。截图只能支持所见状态，
  无法单独证明持久化、权限或所有交互正确，这是本报告的推断。

## P07：Aider 的检查接口与格式化误报

- 来源：[Linting and testing](https://aider.chat/docs/usage/lint-test.html)，Aider 官方文档。
  无页面发布日期。已读 lint、formatter、test、compile 与 /run 段落。
  页面示例会话的 0.43.5-dev 不是本次核实的当前版本。
- 机制（M）：编辑后可自动 lint，测试命令需输出诊断并用非零退出码表示失败。
  可配置自动测试，把终端反馈交回修复循环，或者显式分享运行输出。
- 具体陷阱：某些格式化工具“已经自动改好”也返回非零码，agent 会误当缺陷。
  作者给出第二次运行确认稳定结果的 wrapper 示例。
- 成本与适配：每次编辑跑全套检查可能拖慢工作，反馈协议错误还会引发无效修复。
  当前 Skill 已区分误报与环境问题。可作为“检查器也要核实”的具体实例，
  不把非零退出码机械解释成产物有错，也不默认每次编辑都重跑全部测试。

## P08：Copilot PR 完成与 CI 实际运行的区别

- 来源：[Review output from Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/review-copilot-output)，
  GitHub 官方文档。无页面发布日期，已读整页。旧 coding-agent 地址重定向。
- 机制（M）：agent 请求 review 后仍需检查 PR，反馈可交回 agent。
  默认情况下 agent 推送不会自动运行 GitHub Actions，可配置另行允许。
  因此“PR 已生成”与“CI 已实际执行”是不同的状态。
- 成本与适配：受权限和工作流配置影响。当前 Skill 已明确未执行不能记通过。
  此材料适合作为交付状态核对的案例，不宜把平台特定的审批流程加入通用 Skill。

## 候选关系、去重与未收录

- 已覆盖，主要提供来源支撑：真实组合路径、按风险选择测试、证据留存、
  失败分类、独立评审可选、修订后重验。对应 P01、P02、P03、P05、P07、P08。
- 可能补充的具体角度：验证工具观察盲点（P02），跨 UI/API/持久状态的结果关联（P03），
  剩余差异与停滞判断（P04），短证据及可启动复验路径（P05、P06），
  必要且稳定的检查接入已有自动门槛（P01）。均应按任务选择，不构成新增通用清单。
- [Cursor agent best practices](https://cursor.com/blog/agent-best-practices) 已打开，2026-01-09，
  Lee Robinson。测试先失败、锁定测试再实现与规则保持简短均有价值，
  但与测试方法和公共 Skill 路线重叠，故不再另设来源卡片。
- Cursor Cloud Agents 概览、changelog 与产品页均复述 P06 机制，不当作独立效果证据。
- 未收录论坛扩展发布、自述“朋友觉得有用”和通用营销列表，证据弱且不是目标官方机制。
- 不把多 agent、持久目标、录屏或更多轮次本身视为质量提升。
  这里最稳的跨来源事实是：提供能被读取的真实反馈，并明确它实际覆盖什么。
  是否值得增加自动化或评审，仍取决于具体失败模式和成本。
