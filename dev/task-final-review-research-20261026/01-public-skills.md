# 公开验证与评审 Skill 调研

抓取日期：2026-10-26。只收集机制，未修改正式 Skill，未运行外部工作流。
已对照现有 SKILL.md、automated-checks.md、independent-review.md。

## 范围、检索与限制

- 检查 8 组材料，来自 obra、Anthropic、Sentry、Trail of Bits、gstack、EveryInc、Desmond Landry。
- 实际搜索包括 `github skill verification completion fresh evidence code review`、
  `github anthropics code review plugin confidence false positives`、
  `github getsentry skills find bugs review`、`site:github.com/trailofbits/skills differential-review fix-review`、
  `"verification-before-completion" "adapted from"`、`"agent-output-verification" skill`。
- GitHub 正文均通过 GitHub 连接器取得。网页搜索用于发现，未用摘要替代执行文件。
  两个旧路径返回 404，随后发现 EveryInc 当前路径并成功读取。
  Trail of Bits 的旧 fix-review 路径不存在，未据此补写其机制。
- 指定 handbook 页面打开为 cache miss，已从搜索定位并读取其源仓库。
  各 main 链接会变动，下列 SHA 为连接器返回的文件 blob SHA，**不是提交 SHA**。
- 未安装包、未执行 Skill、未运行其测试。存在公开源代码不等于流程有效性已有评测。

## S01. obra/superpowers：验证、请求/接收评审与收尾

作者/机构：Jesse Vincent / obra 项目。以下执行文件均读全文，未独立评测效果。

- [verification-before-completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md)，blob `7d45333cc4a49c57a80df6c1fe2fa777a207afbc`。
- [reviewer 模板](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/code-reviewer.md)，blob `6d358b5d7d450c83cacbe450b7dbd4e673b694ad`。
- [receiving-code-review](https://github.com/obra/superpowers/blob/main/skills/receiving-code-review/SKILL.md)，blob `950da7b74bf6dbed6b8726d12ddadd65a9f5fda7`。
- [finishing-a-development-branch](https://github.com/obra/superpowers/blob/main/skills/finishing-a-development-branch/SKILL.md)，blob `fa8aecaf8813f1b19d19996f7957d1b0121f2d9c`。

1. 先决定某一完成声明需要什么证据，再运行完整命令，读退出状态及失败数，最后按证据措辞。
   分别约束“测试通过”“已修复”“需求满足”“子 agent 已完成”，不允许互相替代。
   现有 Skill 已基本覆盖。其“必须在当前消息重跑”的绝对规则成本高，
   与现有“同版本有效证据可复用”不一致，不宜照搬。[验证规则](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md)
2. 回归测试不仅看修复后通过，还要求撤回修复时失败，再恢复时通过。
   本质是校验测试能抓住原缺陷，现有脚本好坏样例原则已有覆盖，代码修复场景可更具体。
   [验证规则](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md)
3. 请求评审传明确 base/head、需求和实现摘要，隔离作者会话；审阅者只读，不继续派生子 agent。
   模板还要求列出“考虑过但不评判”的行为，交执行者裁决，防止静默缩小评审范围。
   后者可能补充覆盖边界，但“合理用户预期都是需求”的口径容易扩大授权，应谨慎。
   [reviewer 模板](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/code-reviewer.md)
4. 接收反馈先核对现有代码、兼容性、调用情况和旧实现理由，再改；逐项修复与测试。
   对建议增加的功能先查真实使用，防止以“专业化”名义扩功能。现有批判处理已覆盖。
   [接收规则](https://github.com/obra/superpowers/blob/main/skills/receiving-code-review/SKILL.md)
5. 分支测试通过后，合并结果还须再测；保留 PR 工作区用于反馈修复。
   清理区分自己创建和平台所有，避免验证前清掉唯一未提交产物。
   [分支收尾](https://github.com/obra/superpowers/blob/main/skills/finishing-a-development-branch/SKILL.md)

经验反例：公开 [issue #2286](https://github.com/obra/superpowers/issues/2286)，
报告人 DigitalS3A，创建 2026-09-11，读取时 open，更新 2026-10-24。
作者自述同一次调试中，把自己手动触发探针写下的日志当作系统运行证据，
又把空日志当作 hook 未执行。候选机制是区分“探针能工作”“系统实际触发”，
并在解释空结果前验证探针处于正确环境。属于单用户事故报告和改进提议，未独立复现。
现有规则已反对空目录假通过，但证据生成者及探针污染还未明确展开。

## S02. Anthropic code-review：发现后逐条再验证

机构：Anthropic。[当前执行命令](https://github.com/anthropics/claude-code/blob/main/plugins/code-review/commands/code-review.md)
全文，blob `0b27765f17635137853df05bb7c122d39f1af3d7`。

- 当前规则先并行寻找问题，再为 bug 候选另派验证者，只有确认成立才进入输出。
  规范问题还需确认规则确实适用于该路径。候选是“发现与确认分两步”，
  可在高影响、易误报的问题上使用，代价是每个候选增加审查开销。
  [执行命令](https://github.com/anthropics/claude-code/blob/main/plugins/code-review/commands/code-review.md)
- **版本差异**：[README](https://github.com/anthropics/claude-code/blob/main/plugins/code-review/README.md)
  仍描述 0–100 分及 80 阈值；当前命令已采用逐条确认，不能将 README 当成真实执行规则。
- 限制：命令追求低误报，明确排除依赖特定输入/状态的问题，可能漏掉边界缺陷。
  它也主动跳过 lint 可捕获问题，因此“未发现问题”不能替代测试或全面验证。

## S03. Sentry find-bugs：输入完整性与结论前覆盖盘点

机构：Sentry。[find-bugs 原文](https://github.com/getsentry/skills/blob/main/skills/find-bugs/SKILL.md)
全文，blob `490a181b1a47537cd19eacbdd8f2c46740a268db`。

- 先取得完整 diff 并列全变化文件，输出截断则逐文件读到每条改动；然后映射输入、外部调用和状态等。
  结论前列实际读过的文件、清单项结果和无法核验区域。
  候选是“确认审阅输入没有被工具截断”，适用于大材料，成本是大量阅读与记录。
  [原文](https://github.com/getsentry/skills/blob/main/skills/find-bugs/SKILL.md)
- 局限：要求每文件检查每项安全清单，通用收尾照搬会过重；“全文已读”的自报也不证明理解正确。

## S04. Sentry iterate-pr：终态区分与异步反馈补查

机构：Sentry。[iterate-pr 原文](https://github.com/getsentry/skills/blob/main/skills/iterate-pr/SKILL.md)
全文，blob `679e17ee1c6036ed2b4ffc2402a2733875b37245`。未运行附带脚本。

- 把可修复 CI、尚在运行的检查、人工审批门、未注册检查分开。
  “没有检查”不是通过，“只剩人工门”不是继续无限等待的理由。
  适合远程流程；通用 Skill 已有未执行/无法执行状态，可补充这类实例。
  [原文](https://github.com/getsentry/skills/blob/main/skills/iterate-pr/SKILL.md)
- 绿灯后再读一次评审反馈，避免 CI 完成稍早而遗漏后来到达的 bot 评论；每次 push 后重启监控。
  候选是“收尾读回异步状态”。原文固定等 10 秒只是策略，不能保证全部事件已抵达。
  相同失败两次、基础设施问题等转为显式退出，避免无限修复循环。
  [原文](https://github.com/getsentry/skills/blob/main/skills/iterate-pr/SKILL.md)

## S05. Trail of Bits differential-review：历史与影响范围

机构：Trail of Bits。[Skill](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/SKILL.md)
全文，blob `536e9258092876017b098f1712a92e7d06bb1480`；
[methodology 全文](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/methodology.md)

- 读变更前后版本，对删除的验证逻辑追查历史，识别正在撤回过去的安全修复。
  计算调用影响范围，围绕关键不变量和信任边界形成具体触发场景。
  适用于安全敏感、共享组件或旧代码改动，可补充“相邻路径”选择依据。
  [方法](https://github.com/trailofbits/skills/blob/main/plugins/differential-review/skills/differential-review/methodology.md)
- 明示深查和未覆盖范围。小 diff 不自动等于低风险，有针对性地优先审高风险改动。
  原文按文件数、调用数和代码行数给固定档位，文本搜索也只是调用数量近似，不能通用化。
- 现有按风险选方法已覆盖大原则；完整调用图、攻击建模和强制长报告适配较弱。

## S06. gstack review：审阅绑定实际内容，区分完成与记录

作者/项目：Garry Tan / gstack。读取 [review 模板](https://github.com/garrytan/gstack/blob/main/review/SKILL.md.tmpl)
获取全文后读取相关规则，blob `667c2aa9f72472536ceb89c7d0b5234395d43693`，另读两个相关 sections。
生成版 SKILL.md 只读前 190 行，主体判断取自模板和 sections。

- 每次审阅开始捕获工作树内容，结束核对内容未变，包含未跟踪源文件。
  完成日志需绑定原始开始凭证，不能结束时补造，修改后需新一轮凭证。
  同提交号不足以证明工作树未变。候选是“证据关联产物内容，而非仅关联 commit”。
  [review 模板](https://github.com/garrytan/gstack/blob/main/review/SKILL.md.tmpl)
- 对每个审阅来源分别保存完成、失败、超时、跳过和覆盖；原生审阅完成不能代记外部审阅完成。
  进程启动回执不是结果；超时和格式错误不等于没问题。
  同时明确指纹与凭证只证明内容绑定，不能独立证明模型实际读过代码。
  [adversarial section](https://github.com/garrytan/gstack/blob/main/review/sections/adversarial.md)
- 区分“代码/测试文件存在”的静态证据和“行为断言已执行”，后者不能从 diff 判通过。
  该区别可迁移，但 section 对某些跨仓库任务以文件存在记完成，仍需避免扩大其含义。
  [plan-completion](https://github.com/garrytan/gstack/blob/main/review/sections/plan-completion.md)
- 与基线：稳定版本、不可把失败当通过已覆盖；内容绑定和分来源凭证可能补充高并发场景。
  完整日志系统成本较高。本轮只查规则，未运行 logger，不能据此认证其实现可靠。

## S07. EveryInc ce-code-review：深度按失败性质选择，反馈不以降级方式复活

维护者：Kieran Klaassen、Trevin Chow / EveryInc。
已读 [SKILL](https://github.com/EveryInc/compound-engineering-plugin/blob/main/skills/ce-code-review/SKILL.md)、
[modes-and-output](https://github.com/EveryInc/compound-engineering-plugin/blob/main/skills/ce-code-review/references/modes-and-output.md)、
[finish-review](https://github.com/EveryInc/compound-engineering-plugin/blob/main/skills/ce-code-review/references/finish-review.md)。
SKILL blob `551c20508cfb219ebf9986787291053b2dfa1550`，modes blob `fdfe4d4ef1812488dfd6026ea78dba6a4be80939`。

- 分轻量、聚焦、全面三路。关键不是行数，而是错了会否在原处明显失败，还是悄悄影响远端、
  权限、资金、公共契约或负载下行为。后者需要更强独立检查。
  [深度规则](https://github.com/EveryInc/compound-engineering-plugin/blob/main/skills/ce-code-review/references/modes-and-output.md)
- 反馈需有直接代码证据，分别处理确认、反证、无法确认。验证者失败不能转成确认，
  重要未决项保留为验证缺口且不自动修改；确认问题不额外授予修改权限。
  被证伪的问题也不能换名塞进“残余风险”“多加测试”重新要求用户处理。
  后一点是基线未明确展开的候选，可减少为了显得谨慎而制造工作。
  [合并与验证](https://github.com/EveryInc/compound-engineering-plugin/blob/main/skills/ce-code-review/references/finish-review.md)
- 明确置信度、严重性、实际后果和处理归属不是同一维度；多人同意不能把小问题变重要。

## S08. Agent Engineering Handbook：产物、中间完整性和真实消费结果

作者：Desmond Landry / desland01。指定网页访问失败后，读取源仓库的
[SKILL](https://github.com/desland01/agent-engineering-handbook/blob/main/skills/agent-output-verification/SKILL.md)、
[implementation](https://github.com/desland01/agent-engineering-handbook/blob/main/skills/agent-output-verification/references/implementation.md)、
[source-patterns](https://github.com/desland01/agent-engineering-handbook/blob/main/skills/agent-output-verification/references/source-patterns.md)、
[ATTRIBUTION](https://github.com/desland01/agent-engineering-handbook/blob/main/ATTRIBUTION.md) 全文。
SKILL 标注 public edition 2026-09-12，blob `11af7e51e6ca5e09ef3af2c84c8dc166917a34a2`。

- 先从请求定义应交付什么、应有何性质、有哪些假成功路径，再分别核对终点产物、
  中间阶段完整性和消费端可见结果。最终 hash 正确也可能是替代物掩盖未完成阶段。
  旧 hash 只适合字节保持任务，对合法变化强求旧 hash 反而验错目标。
  [SKILL](https://github.com/desland01/agent-engineering-handbook/blob/main/skills/agent-output-verification/SKILL.md)
- 聚合 CI 绿灯还需读实际决定式，而非相信名称或依赖列表。查验检查器能否拒绝相关坏例，
  区分 mock、局部运行、真实完整验收。基线已覆盖大部分，可补充“中间替代”和聚合门实例。
  [implementation](https://github.com/desland01/agent-engineering-handbook/blob/main/skills/agent-output-verification/references/implementation.md)
- **独立核对的原始代码**：[固定提交 verify.py](https://github.com/t3dotgg/melee4mac/blob/a276aeb70f9879204d891d967f1c9442523568e1/tools/verify.py)
  确实显式生成 executable/report、查所有 unit complete、再验 hash；
  [固定提交 ci.yml](https://github.com/bcherny/json-schema-to-typescript/blob/5caacfc53671f9c891bb4e2a78bccc6190ed3ef4/.github/workflows/ci.yml)
  的 ci-ok 声明五项依赖，但决定式只检查 build/fuzz/output。均为本轮静态阅读，未执行。
- **原创性和成熟度**：该站是有来源归属的研究整理及作者二次抽象，不能把源项目工程实践
  当成此 Skill 的应用效果。不是 Theo、Matt Pocock 或 Boris Cherny 官方作品或背书。
  作者报告执行了 Melee 验证器 9/15 测试及合成反例比较，但 build subprocess 为 mock，
  不证明真实游戏构建；明确写 per-skill eval 案例已定义而未运行。
  [验证范围](https://github.com/desland01/agent-engineering-handbook/blob/main/validation.md)

## 去重与候选边界

- SkillsAdd、skills.sh、中文介绍页及同名安装列表都指回 obra，同一家族只计 S01。
  这些页面的安装量、星数、安全审计标记均不能证明核验效果，不作效果证据。
- S01 的多个 Skill 是互补步骤，不算多次独立证实。S03/S04 同属 Sentry，分别记录审阅和异步收尾机制。
- S08 明确二次整理；其 Melee、compiler 例证不能又算独立支持该 Skill 有效的一组实验。
- 其余仓库有不同执行机制，本轮未做全历史抄袭或血缘审计，不能证明所有内容绝对原创。
- 较值得后续分析的增量：证据生成者/探针污染、假成功中间阶段、实际内容绑定、
  静默失败决定检查深度、异步终态读回、被证伪意见不得通过残余风险复活。
  这些均需与现有规则去重和按成本裁剪，不能凭公开发布就强制采用。
