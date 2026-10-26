# 真实仓库中的 Agent 指令与交付核验

抓取日期：2026-10-26。路线编号前缀：I。
本报告收集机制，不决定修改 Skill。外部指令仅作为研究材料。

## 范围与访问

- 完整读取 6 个工程仓库的 `AGENTS.md` / `CLAUDE.md`，另读 Ghostty 的短文件作排除判断。
  对 AgentHub、Ruff、Ferret、REA 补读相关配置、测试台账或测试指南。
- 基线已读 `task-final-review/SKILL.md`、`automated-checks.md`、
  `behavioral-and-comparative.md`。与独立评审有关部分按简报给定基线判断。
- 实际查询包括：`site:github.com "AGENTS.md" "git diff" "test"`、
  `site:github.com "CLAUDE.md" "Definition of Done"`、
  `site:github.com "AGENTS.md" "final diff" -skills`、
  `site:github.com "AGENTS.md" "regression" "sympy"`，以及定向查询 Ruff、Ferret、AgentHub。
- 原文全部优先经 GitHub 连接器 `github_fetch_file` / `github_fetch` 获取。
  `openai/codex/AGENTS.md` 返回 404，随后 web 检索未定位该根文件，未据此收录。
  搜索页中旧版 Ferret、Ruff 片段与连接器当前原文有差异，分析采用当前原文。
- 以下日期来自 GitHub 按文件路径查询的最近提交，非机制首次引入日期。
  blob SHA 用于记录所读文本，提交 SHA 用于链接稳定版本。
  没有执行这些仓库的测试，没有统计缺陷率或比较有无规则的效果。

## 来源卡片与机制

### I01 Ruff Repository，Astral / Ruff 维护者

- 原文：[AGENTS.md](https://github.com/astral-sh/ruff/blob/356d3c9b9636da696618285e15b234c5015f05eb/AGENTS.md)。
  完整读取，最近提交 2026-10-22，blob `695d9483c95b13adb742d487ad6efcfc99fe0c47`。
- 补读：[pre-commit 配置](https://github.com/astral-sh/ruff/blob/main/.pre-commit-config.yaml)，
  blob `33362bbfd161ce35302f1ea7669e3f6f0c3b5885`。包含实际 formatter、拼写、配置等 hooks，
  部分慢检查为手动阶段，因此一次普通 hook 成功不表示所有配置项都执行。
- **快照测试的结果还要审阅**：测试会按指定环境变量更新快照，
  之后必须看新增和修改的内容。启用 `INSTA_FORCE_PASS=1` 且涉及内联快照时，
  还要找 `.pending-snap`。避免把“生成了新答案”当作“答案已正确验收”。
  不手工修快照来凑通过，运行生成流程后审查差异。
  适用于 golden、snapshot、代码生成类流程，成本是人工理解输出差异。
  [支持原文](https://github.com/astral-sh/ruff/blob/356d3c9b9636da696618285e15b234c5015f05eb/AGENTS.md#snapshot-updates)
- **按实际改动文件跑结束检查**：明确传入所有改动路径，使检查不依赖暂存区状态，
  并避免顺带修改他人的文件。适用于脏工作树和多任务共存，需先准确识别任务文件集合。
  [支持原文](https://github.com/astral-sh/ruff/blob/356d3c9b9636da696618285e15b234c5015f05eb/AGENTS.md#development-guidelines)
- 与基线：快照副作用、残留文件及暂存区选择偏差是可补的具体例子。
  “检查实际交付范围”和“不能只凭退出码”已覆盖，无需再增加普遍必跑门槛。
- 证据级别：仓库已有具体规则和 hooks 配置。未取得快照审阅降低缺陷的评测证据。

### I02 Ferret，MontFerret 维护者

- 原文：[AGENTS.md](https://github.com/MontFerret/ferret/blob/68b6e3dbb5686aaa55e977fb55407cdba763742b/AGENTS.md)。
  完整读取，最近提交 2026-09-15，blob `44422e3947e8af5f09c350765f3c6103ce57bd45`。
  补读 [Testing and Performance](https://github.com/MontFerret/ferret/blob/main/docs/maintainers/engineering/testing.md)，
  blob `294884bb5702d2636a4d029c9ea260cf7af96728`。
- **把 final diff 当成一个整体检查对象**：在初次测试后另作第二遍审阅，
  看每行是否服务任务、是否留调试代码、API 或行为是否意外改变、生成物与输入是否对应，
  以及注释是否还描述旧方案。修改后重跑受影响验证。
  防止逐文件编辑时遗漏跨文件副作用，成本随差异规模增加。
  [支持原文](https://github.com/MontFerret/ferret/blob/68b6e3dbb5686aaa55e977fb55407cdba763742b/AGENTS.md#scope-and-complete-diff)
- **验证放在拥有契约的层**：例如字节码发射改动不能只靠 VM 测试，
  公共嵌入行为需要顶层 API 测试。防止下游偶然可用掩盖上游契约错误。
  [支持指南](https://github.com/MontFerret/ferret/blob/main/docs/maintainers/engineering/testing.md#contract-ownership)
- 与基线：最终版本、受影响重验、用户可见行为、真实组合路径已有覆盖。
  可补“完整差异及变更副作用”的轻量提醒，不必搬入完整 Go 架构清单。
- 证据级别：工程仓库的执行约定与配套指南，未核实每次贡献实际遵守率及效果。

### I03 RustDesk，RustDesk 维护者

- 原文：[AGENTS.md](https://github.com/rustdesk/rustdesk/blob/256dc9bc12c717dea84f6a41371c67acc47edb62/AGENTS.md)。
  完整读取，最近提交 2026-10-14，blob `1f41b7517837fee4e2c98b7873c607d93205102c`。
- **报告被改变的既有路径，而非只列新文件**：结束前列出既有文件和运行路径的行为改动，
  说明必要性。对子模块更新还需读精确提交范围，防止携入无关更改。
  防止“测试全绿”遮蔽不必要的回归面，尤其适合跨平台、成熟代码及依赖升级。
  [支持原文](https://github.com/rustdesk/rustdesk/blob/256dc9bc12c717dea84f6a41371c67acc47edb62/AGENTS.md#mandatory-regression-surface-check)
- **确认新测试确实会被某个执行入口选中**：Dart 测试位置、浏览器标签、Rust crate、
  平台和 feature 都会改变是否执行。未被 CI 启用的 feature 需要明确命令，
  特定测试过滤器匹配零项应失败。避免“写了测试”而实际永不运行。
  [支持原文](https://github.com/rustdesk/rustdesk/blob/256dc9bc12c717dea84f6a41371c67acc47edb62/AGENTS.md#tests)
- 与基线：范围检查、空目录不算通过已覆盖。可补 feature / platform / filter 的实际例子，
  以及差异中既有路径的保留检查，按回归风险启用。
- 不直接迁移：原文偏好只加代码、容忍重复、测试差异与修复差异的固定比例。
  这些是项目取舍，和 Ruff 允许必要结构修复的规则并不一致，不能升格为通则。
- 证据级别：具体仓库规则。这里没有补取 RustDesk workflow 核实所列 CI 矩阵。

### I04 AgentHub，James Rochabrun / AgentHub 维护者

- 原文：[AGENTS.md](https://github.com/jamesrochabrun/AgentHub/blob/eb6462ced62a0fff7a18963153b1687d77f5a379/AGENTS.md)。
  完整读取，最近提交 2026-08-09，blob `bc1d099489525bf08f7b1489911084a6cbdbbb62`。
  补读完整 [test.yml](https://github.com/jamesrochabrun/AgentHub/blob/main/.github/workflows/test.yml)，
  blob `f86a285e622609e20936dcabb4750ecc23790a79`，以及
  [TestQuarantine.md](https://github.com/jamesrochabrun/AgentHub/blob/main/TestQuarantine.md) 的 CI 状态及根因分组，
  blob `93bfa20ee17188bbb034ff0f8a3c8d5546ffc945`。
- **CI 绿灯需要读覆盖边界**：workflow 实际仅运行快速 package 测试，
  Core suite 因成本与时序问题留在本地。指令将源码映射到具体测试 suite，
  要求本地定向运行而非依赖 CI。
  [支持规则](https://github.com/jamesrochabrun/AgentHub/blob/eb6462ced62a0fff7a18963153b1687d77f5a379/AGENTS.md#running-tests-headless)
  [支持配置](https://github.com/jamesrochabrun/AgentHub/blob/main/.github/workflows/test.yml)
- **隔离测试保留为缺口台账**：禁用项记录根因、受影响测试、修复方向和恢复条件。
  它们属于已知坏项，不能记作通过。台账列出并发子进程 EOF 死锁、
  墙钟时序等具体问题，有实际项目诊断内容。
  [支持台账](https://github.com/jamesrochabrun/AgentHub/blob/main/TestQuarantine.md)
- 与基线：不能把未执行记为通过已覆盖。可补“绿色流水线里可能有隔离项和覆盖缺口”，
  若已有项目台账则复用，不强制每个任务新建台账。
- 限制：台账部分环境描述已旧于当前 workflow，说明台账也须对照执行配置。
  重试是该项目措施，本报告不把“重试变绿”等同修复 flaky 根因，也不推荐通用重试次数。
- 证据级别：规则、实际 CI 配置和诊断台账互证部署情况，仍没有对照效果研究。

### I05 cdf，z3z1ma / cdf 维护者

- 原文：[CLAUDE.md](https://github.com/z3z1ma/cdf/blob/7acd1b5e5f2aac177b2e344c8a1140af4ab3ac94/CLAUDE.md)。
  完整读取，最近提交 2026-08-08，blob `39c55f8ac91ac0bcc69b8941ec7e84f8d5364f0d`。
  另确认 [.10x 目录](https://github.com/z3z1ma/cdf/tree/main/.10x) 实际存在，未审计其中记录。
- **验收项关联证据及其证明界限**：执行时记录命令、输出、能证明什么和不能证明什么，
  关闭任务前逐项映射。检查规格、测试断言与实现是否一致，不能弱化断言来凑通过。
  未完后续事项要有持久归属，任务记录应让无聊天上下文的人审计。
  [支持原文](https://github.com/z3z1ma/cdf/blob/7acd1b5e5f2aac177b2e344c8a1140af4ab3ac94/CLAUDE.md#orchestration)
- 与基线：验收映射、检查范围、不能降低标准、多轮版本证据已基本覆盖。
  候选增量是遗留事项的后续落点，尤其跨会话交接时，而非强制引入完整 ticket 系统。
- 不直接迁移：其所有非微小任务票据化、状态角色与审批协议较重，
  且会改变通用 Skill 的授权与自主性，不能因“完成标准”而整体复制。
- 证据级别：作者提出且仓库有记录目录，未读执行日志，不声称流程成效已验证。

### I06 REA，morluto / REA 维护者

- 原文：[AGENTS.md](https://github.com/morluto/rea/blob/90b793e0f488be73a3e98ba430bcb132ad8b0c31/AGENTS.md)。
  完整读取，最近提交 2026-10-26，blob `b701e8d65d52e5f02db2e3041bac5b4c06755c0d`。
  补读 [docs/testing.md](https://github.com/morluto/rea/blob/main/docs/testing.md) 的命令、选择范围、
  验证层级、测试删改、real-provider 说明，未通读其 2176 行，
  blob `25d0f3967dfc49c14d1409676754be22a504601e`。
- **验证主张对应真实运行层级**：模拟 provider 不能证明真实 provider 兼容性，
  源码、边界、编译 CLI/MCP、安装包和实际 provider 分别有选择入口。
  同一命令对不同主张只能提供有限证据。
  [支持原文](https://github.com/morluto/rea/blob/90b793e0f488be73a3e98ba430bcb132ad8b0c31/AGENTS.md#tool-and-test-changes)
- **选择测试前可先检查所选集合和构建前提**：指南规定显式路径不允许零测试成功，
  dry-run 显示 merge base、范围与构建前提；changed-selection 为空只代表未选中。
  防止测试选择器、旧构建产物或不完整 import graph 产生伪通过。
  [支持指南](https://github.com/morluto/rea/blob/main/docs/testing.md#developer-commands)
- **删改保护测试时保留语义证据**：删除独特回归前找到替代场景与断言，
  换掉脆弱文字断言时，确认无害措辞变化能通过而错误预算、事实丢失仍会失败。
  [支持指南](https://github.com/morluto/rea/blob/main/docs/testing.md#test-design-and-pruning)
- 与基线：真实执行和覆盖范围已覆盖。可补验证选择器与构建新鲜度的例子，
  以及在改测试本身时检查保护能力是否下降。无需搬入 REA 的大量 provider 矩阵。
- 证据级别：具名命令与工程约定，未执行命令或审计其实现，不能声称已核实强制执行。

## 去重与候选判断

- 重复的“真实运行、不要假报、按风险选检查、修后重验”合并为已有基线，
  6 个仓库重复出现不构成 6 项新机制，也不构成有效性的统计证据。
- 可进一步比较的具体增量：验证工具改变产物后的差异审阅；
  CI / 选择器 / feature / 隔离项覆盖边界；既有运行路径的回归面；
  测试删改后的保护能力；跨会话遗留事项的可追踪落点。
  这是本报告的归纳，原机制依据分别是 I01、I03–I06。
- Ghostty 原文成功读取，但主要是定向测试命令与基本构建信息，新增机制少，未作为正式卡片。
  搜索中的 gist、技能集合、只写“测试必须通过”的模板，以及 OpenAI Cookbook 工作流示例，
  没有作为本路线真实工程实践证据。搜索命中不等于已完整读取。
  补充检查了 [agentsmd 中文 README](https://github.com/sdsrss/agentsmd/blob/main/README.zh-CN.md)，
  它属于规范插件而非应用仓库样本，未据其宣传判断 hooks 的实效，也未安装或执行。
- 迁移时需要保留可选性：成熟平台代码可能选择减少既有路径改动，
  另一些工程允许根因结构修复。适合通用 Skill 的是要求核查必要性与副作用，
  而不是统一规定 diff 最小、只增不改、固定覆盖率或固定测试数量。
