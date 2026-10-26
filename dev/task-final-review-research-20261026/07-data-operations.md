# 数据、操作结果、最终产物与交接完整性调研

抓取日期：2026-10-26。仅收集，不修改正式 Skill，不执行来源中的操作。
已读当前 `task-final-review/SKILL.md` 及自动检查、内容与呈现两份参考。

## 检索范围与限制

- 范围：数据关联与缺失、表格公式缓存、生成物追踪、交付包完整性、
  异步操作的实际后置条件、重跑与交接中的隐藏依赖。
- 实际查询包括 `site.gov.uk data quality framework completeness validity`、
  `site.pandas.pydata.org docs merge validate indicator many to many`、
  `site.openpyxl.readthedocs.io "never evaluates formulae" "data_only"`、
  `site.snakemake.readthedocs.io ensure non-empty checksum output files`、
  `site.rfc-editor.org rfc 8493 complete valid bag payload manifest`、
  `site.kubernetes.io kubectl wait condition observedGeneration status`、
  `site.nbconvert.readthedocs.io execute notebook kernel timeout errors`、
  `site.reproducible-builds.org documentation recording build environment checksums`。
- 微信材料由主 agent 中文补充检索发现，本路线通过 GitHub 连接器读取。
  其余为维护者官网文档，不涉及 GitHub 读取回退。
- `openpyxl/.../data_only.html` 不可访问，改读官方 Tutorial 和 Simple Formulae。
  未安装工具、实际执行数据流水线、操作集群或测量质量改进幅度。

## 来源卡片

### O01：The Government Data Quality Framework
- 机构：英国 Government Data Quality Hub。发布日期 2020-12-03。
- 原文：[Framework](https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework)。
  已读生命周期、六种质量维度、质量沟通与取舍。
- 作者做法：质量针对用途定义，完整性、唯一性、一致性、及时性、有效性、
  准确性不能互相替代。质量问题与元数据应随数据提供。
- 证据性质：政府正式实践指南，含实施案例入口。
  本次未读取案例，不能据此声称已验证其效果。

### O02：pandas.merge
- 作者：pandas 维护者。读取版本为页面自报 3.1.0，未取得对应提交日期。
- 原文：[API 文档](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)。
  已读参数、空键警告及示例。
- 已实现机制：`validate` 校验关联键基数，`indicator` 区分左右未匹配与双边匹配。
  `many_to_many` 不做检查，双边空键会互相匹配，行为区别于通常 SQL。
- 证据性质：维护者对已实现接口的说明和示例，不是效果评测。

### O03：openpyxl 的公式与工作簿读取
- 作者：openpyxl 维护者。读取版本 3.1.3，未取得页面更新日期。
- 原文：[Simple Formulae](https://openpyxl.readthedocs.io/en/stable/simple_formulae.html)、
  [Tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html#loading-from-a-file)。
  已读公式不求值说明、`data_only` 与工作表复制限制。
- 已实现行为：写入公式不负责计算，`data_only` 返回 Excel 上次存储的值。
  工作表复制也不涵盖图表、图片等全部内容。
- 证据性质：明确的工具能力边界，无新增验证流程的成效数据。

### O04：Snakemake 输出条件与自包含报告
- 作者：Johannes Köster 及 Snakemake 维护者。读取页面版本 9.27.1。
- 原文：[Rules](https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#ensuring-output-file-properties-like-non-emptyness-or-checksum-compliance)、
  [Reports](https://snakemake.readthedocs.io/en/stable/snakefiles/reporting.html)。
  已读 `ensure`、时间戳例外、report 产物、元数据与 partial reports。
- 已实现机制：任务成功前可验证输出非空或可信预期 checksum。
  报告可包含 provenance、工作流结构和指定结果，封装 HTML 或 ZIP。
  报告也可仅含指定目标，报告存在不能证明整个工作流完成。
- 证据性质：已实现功能及官方使用示例，不是通用有效性的比较研究。

### O05：RFC 8493，The BagIt File Packaging Format (V1.0)
- 作者：J. Kunze 等，California Digital Library、Stanford Libraries、
  Library of Congress 等机构。Informational RFC，2018-10，BagIt 1.0。
- 原文：[RFC 8493](https://www.rfc-editor.org/rfc/rfc8493.html)。
  已读 §1、§2.1.3、§2.2.3、§3。
- 原始机制：完整性检查文件清单双向覆盖，内容一致性检查每个 checksum。
  允许先传缺件包，但需取齐缺件才可有意义地检查完整性。
- 证据性质：公开格式规范。RFC 自述 Library of Congress、Dryad 等有实际使用，
  本次未独立追查这些部署，不作为实测证明。

### O06：kubectl wait 与版本化状态条件
- 作者：Kubernetes 维护者。wait 页面随主站版本变化，未固定提交。
- 原文：[kubectl wait](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_wait/)、
  [KEP-1623](https://www.kubernetes.dev/resources/keps/1623/)。
  已读 Status 条件、存在/删除、超时、condition 的 observedGeneration 定义。
- 原始机制：等待指定资源实际出现所需状态。
  条件中的 observedGeneration 低于当前 generation 时是旧条件。
- 证据性质：wait 为可用命令文档，KEP 为设计原文。
  不将 KEP 的推荐 schema 当作所有资源均已采用的事实。

### O07：Executing notebooks
- 作者：Jupyter Development Team。读取 nbconvert 7.17.2 文档。
- 原文：[执行 API](https://nbconvert.readthedocs.io/en/latest/execute_api.html)。
  已读执行、工作目录、kernel、异常保存、allow_errors、Widget state。
- 已实现机制：执行输入并另存带实际输出的 notebook，配置工作目录和 kernel。
  可保存失败前的部分输出，`allow_errors=True` 会带错误执行到底。
  Widget 执行未经过浏览器，不能证明浏览器呈现正确。
- 证据性质：官方接口行为和使用示例，未证实重跑成功等于分析结论正确。

### O08：What's in a build environment?
- 作者：Reproducible Builds 项目。页面未显示版本及更新时间。
- 原文：[Environment perimeter](https://reproducible-builds.org/docs/perimeter/)。
  已读环境范围、版本、路径、locale、timezone、环境变量及容器局限。
- 作者做法：先明确复现所需环境范围，至少记录工具与版本。
  容器仍可能隐藏 CPU 类型等假设，环境相同的定义须由项目决定。
- 证据性质：维护者实践指南。迁移到表格、报告生成是本报告推断。

### O09：wxa-skills-validate，新增中文来源
- 作者：Tencent，仓库 `wechat-miniprogram/ai-mode-skills`，Skill version 0.3.0。
- 原文：[SKILL.md](https://github.com/wechat-miniprogram/ai-mode-skills/blob/master/wxa-skills-validate/SKILL.md)、
  [CLI 参考](https://github.com/wechat-miniprogram/ai-mode-skills/blob/master/wxa-skills-validate/references/CLI_AGENT_REFERENCE.md)。
  GitHub 连接器返回 blob SHA 分别为 `67b639121dfa6130d86973dc2bb1b5b6c2d3b0c5`、
  `6c346ef7518be947af799c3ee80b46880b8871e9`。未取得提交日期。
- 已读：分层执行与渲染、旧产物复用条件、空结果、监测基线、跳过状态、交付说明。
- 证据性质：团队发布的工作约定，带脚本接口与产物结构。
  本次未运行其脚本，不能当作独立效果验证。

## 可迁移机制与现有覆盖

1. **用实体标识和关联基数核对转换，而不只看总行数。**
   先从业务确定一对一或多对一关系，再查未匹配键、重复键与空键策略。
   可发现行数恰好相等但实体错配、内连接悄悄丢行、重复键放大的失败。
   [O02](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)。
   成本：几项统计或现有校验参数，不强制引入 pandas。
   当前已覆盖标识、重复缺失及总数不足，可能补的是关联基数、孤儿键和空键语义例子。

2. **分开验证公式存在、公式计算、缓存与最终显示。**
   公式解析通过或读取到缓存数字不能证明本次公式已重算。
   对受影响关键单元格，在适合的计算引擎重算后保存，再核对导出数字和呈现。
   [O03](https://openpyxl.readthedocs.io/en/stable/simple_formulae.html)。
   后半流程是本报告推断，须按任务已有工具选择，不默认安装 Excel 或 LibreOffice。
   当前已覆盖独立重算和最终导出，可能补的是缓存这一容易混淆的证据层。

3. **让证据随数据流走，区分真实上游输出与人工样例。**
   保留输入身份、关键参数、实际返回或中间文件、最终输出之间的最小对应。
   下游用真实上游返回验证，修改返回结构后使旧下游证据失效，仅 UI 变化可复用数据。
   [O09](https://github.com/wechat-miniprogram/ai-mode-skills/blob/master/wxa-skills-validate/SKILL.md)、
   [O04](https://snakemake.readthedocs.io/en/stable/snakefiles/reporting.html)。
   “最小对应”是迁移推断，不要求 DAG 系统。成本随链路长度增长。
   当前已有输入版本、受影响检查重做，可补依赖变更如何使证据过期的具体判断。

4. **交付包分“预期件齐全”“字节一致”“实际可用”三层。**
   对较大多文件交付，按预期入口和附件列清单，检查清单与实际文件双向一致，
   有传输或版本混杂风险时才加 checksum，再从接收者拿到的目录验证入口。
   [O05](https://www.rfc-editor.org/rfc/rfc8493.html#section-3)。
   前两层来自 BagIt，第三层是基于其只处理不透明字节的必要推断。
   checksum 不能证明语义正确，也不能证明预期清单本身无遗漏。
   当前已有实际目录验证，候选补充为包完整性与内容正确性分离，不要求采用 BagIt 格式。

5. **异步操作核对当前请求对应的后置条件，并限制等待。**
   按资源身份读取操作后状态，在合理超时内等待需要的条件，
   如有版本或 generation 信息，核对证据属于本次请求，避免旧 Ready 状态误报。
   [O06](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_wait/)。
   版本新鲜度依据 [KEP-1623](https://www.kubernetes.dev/resources/keps/1623/)。
   不同系统状态字段语义不同，“已观察请求”仍未必表示动作完成。
   当前已覆盖真实生效状态，可能补异步、状态新鲜度和超时后保留未完成状态。

6. **先证明监测器有机会观察，再解释“没有错误”。**
   如依赖溢出日志判定，先确认监听已启用并存在生命周期基线，
   再判断未出现错误事件，防止根本没启用检测却判通过。
   [O09 CLI 参考](https://github.com/wechat-miniprogram/ai-mode-skills/blob/master/wxa-skills-validate/references/CLI_AGENT_REFERENCE.md)。
   推广到空扫描范围、没消费数据等，是本报告推断。
   当前已禁止空目录扫描算通过，此例补充了运行时观测器的正向覆盖信号。

7. **按交接用途选择重跑范围，并保留失败与部分产物身份。**
   从明确 kernel、工作目录及必要环境重跑，可发现依赖交互会话残留的分析。
   保存输出仍可能是部分失败 notebook 或 partial report，不能以文件存在推断全部完成。
   [O07](https://nbconvert.readthedocs.io/en/latest/execute_api.html)、
   [O04](https://snakemake.readthedocs.io/en/stable/snakefiles/reporting.html#partial-reports)。
   环境记录按 [O08](https://reproducible-builds.org/docs/perimeter/) 缩到影响结果的内容。
   当前已覆盖检查缺口和接收者路径，可能补会话残留、部分产物与完整完成的区别。

## 去重、适配边界与未收录

- 九组来源中 O09 为主 agent 补充的中文原始材料，故略超通常 5–8 个来源。
  Snakemake 新旧版本搜索结果、BagIt 信息页与正文不重复计数。
- O01 的质量维度主要帮助选失败模式，现有 Skill 的按需原则已覆盖。
  不迁入政府治理组织、常规监控或固定六维全检，避免扩大一次性任务。
- 不迁入供应链签名、正式发布审批、微信固定环境、固定迭代轮数和不可逆接口审批流程。
- 微信“无图像能力时样式检查退化为字段存在即通过”的规则不宜迁入，
  字段存在无法证明样式一致，应按当前 Skill 保留未执行检查及结论边界。
  其 `skipped_destructive` 可借鉴明确状态名，但跳过执行不能成为业务正确性的证据。
- O08 源自二进制构建，普通文档不默认追求逐字节复现。
  随机结果、时间相关数据应定义任务真正需要的等价关系，属于本报告推断。
- 未将搜索结果中的 Stack Overflow 答案、商业介绍、旧版 openpyxl PDF、
  普通宣传页纳入主要证据，已有更直接维护者材料。
- 本路线没有比较实验或量化收益证据，主要贡献是具体故障机制与已实现的检查手段。
