# 测试方法与验证有效性调研

抓取日期：2026-10-26。仅研究，不修改正式 Skill，不安装或运行外部项目。
已读当前 `SKILL.md`、`automated-checks.md`、`behavioral-and-comparative.md`。
这里的“候选”是适配判断，不代表决定采纳。

## 范围、查询和访问限制

关注测试预期来源、测试能否检出缺陷、回归证据、属性和变形关系、
变更影响、未触达分支，以及模拟环境与真实结果之间的缺口。
实际搜索词包括：

- `site.hypothesis.readthedocs.io property based testing test different oracle`
- `site.stryker-mutator.io mutation testing coverage tests quality`
- `site.docs.djangoproject.com writing your first patch regression test fails`
- `site.testing.googleblog.com dont put logic tests expected`
- `site.coverage.readthedocs.io branch coverage measurement missing branches`
- `site.abseil.io resources swe-book test doubles fidelity real implementation`
- `metamorphic testing a review of challenges and opportunities Chen 2018 oracle`
- `site.bazel.build query how-to affected tests rdeps set`
- `Chen metamorphic testing 1998 technical report simple approach pdf`
- 补查 `metamorphic testing site.hypothesis.readthedocs.io` 等作者与框架限定词。

网页来源均打开原文。GitHub 用已发现的 `github_fetch`、`github_fetch_file`
连接器读取 GeMTest README、提交信息及 Hypothesis 自测指南，连接器可用。
PDF 查阅按本机 PDF Skill 处理，但受网页提取、截图可见性和网络限制，
无法可靠通读的论文不作为已读机制证据，详见末尾。

## 来源卡片

### T01：Don't Put Logic in Tests

Erik Kuefler，Google Testing Blog，2014-07-31。
[原文](https://testing.googleblog.com/2014/07/testing-on-toilet-dont-put-logic-in.html)。
已读正文与示例。作者展示测试中的字符串拼接会掩盖双斜杠错误，
建议具体输入输出直接可见，复杂测试辅助函数也应检验。
证据类型：作者工程指导和示例，无受控效果评测。

### T02：Writing your first contribution for Django

Django 官方，固定文档版本 5.2，页面更新日期未标明。
[原文](https://docs.djangoproject.com/en/5.2/intro/contributing/)。
已读编写、运行新测试和修复后复跑部分。
明确要求回归测试在缺陷存在时失败、修复后通过，并实际检查新测试是否被发现。
证据类型：成熟项目贡献流程和可运行教学例，不是通用效果实验。

### T03：Mutation testing / Equivalent mutants

Stryker 官方团队，读取当日在线文档，页面版本和更新时间未标明。
[方法说明](https://stryker-mutator.io/docs/)、
[等价变异限制](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/)。
已读机制、边界比较符示例及等价变异说明。
对生产代码施加小改变后，测试应能失败。存活变异提示检查覆盖或断言缺口，
但语义等价变异无法靠新增测试消除。
证据类型：工具已实现机制，官方示例展示，无本轮独立运行或效果评测。

### T04：Hypothesis introduction / Testing Hypothesis

Hypothesis 团队，在线教程显示 6.170.11。
[教程](https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html)、
[项目自测指南](https://github.com/HypothesisWorks/hypothesis/blob/master/guides/testing-hypothesis.rst)。
已读属性候选、生成样例方式和自测哲学。
教程举出往返、简单参考实现、守恒与不崩溃等属性。
自测指南文件 blob 为 `5c8e45f1ae8c33ded4d598dbcd619e0651c00428`，
声明项目要求分支覆盖，但同时指出满覆盖仍可能缺失关键断言。
证据类型：框架机制及维护团队自述的实际采用，无普遍收益量化结论。

### T05：GeMTest: A General Metamorphic Testing Framework

Simon Speth、Alexander Pretschner，TUM 作者团队官方仓库。
[固定提交 README](https://github.com/tum-i4/gemtest/blob/f13150ebf86ddf5e350dfba351381581beb23ddb/README.md)。
连接器完整读取。提交 `f13150ebf86ddf5e350dfba351381581beb23ddb`，
2025-06-13，提交说明为版本 1.0.1。
将变形关系拆成源输入、输入变换、输出关系与被测系统，
用正弦周期性展示从一组输入生成后续用例并交由 pytest 执行。
证据类型：原作者框架文档、实现与示例运行记录。本轮未运行，
README 的通过例不证明缺陷检出率，也不能据此称框架被广泛采用。

### T06：Branch coverage measurement

Coverage.py 官方，在线文档版本 7.17.0，更新时间未标明。
[原文](https://coverage.readthedocs.io/en/latest/branch.html)。
已读语句覆盖遗漏 false 分支的例子、分支报告与排除规则。
该工具记录实际行间转移，与可能转移比较，指出未执行的分支。
证据类型：测量机制及可复现例，无“满覆盖保证正确”的主张。

### T07：Software Engineering at Google，Chapter 14: Larger Testing

Joseph Graves 撰写、Tom Manshreck 编辑，图书出版于 2020 年，
[作者机构公开原文](https://abseil.io/resources/swe-book/html/ch14.html)。
已读 fidelity、unfaithful doubles、configuration issues 与大型测试成本。
指出手工 mock 可能误述依赖行为并过期，单元测试难以覆盖启动配置，
真实组合测试更贴近系统，但有运行慢、不稳定和维护责任等代价。
证据类型：Google 工程经验及案例叙述，无本轮可复核的跨团队收益统计。

### T08：Bazel Query guide

Bazel 官方，读取当日在线文档，版本与更新时间未标明。
[原文](https://bazel.build/query/guide#reverse-dependencies)。
已读反向依赖、路径查询和测试集合展开。
`rdeps(u, x)` 在指定图范围内查找依赖变更目标的其他目标，
`tests(...)` 展开测试集合。
证据类型：工具可实现的影响分析机制，未评测测试选择安全性。

## 可迁移机制及与现有 Skill 的关系

1. **独立预期还应便于人工核对。**
   对少量关键例子，写出由需求或独立计算得出的具体预期，
   避免在断言里复刻同一套转换、分支或拼接逻辑。
   复杂辅助判定器则核对其自身正确性。[T01](https://testing.googleblog.com/2014/07/testing-on-toilet-dont-put-logic-in.html)
   当前已明确独立预期和新脚本正反例，因此主要是细化共同错误来源，新增价值有限。
   成本低，适合精确输出。不能扩大为所有属性测试都禁止逻辑。

2. **回归应尽可能提供同一用例的失败再通过证据。**
   先确认用例在有缺陷版本失败，再确认修复版本通过。
   已经完成修复时，可在安全的旧版副本运行，避免改动当前工作区。
   [T02](https://docs.djangoproject.com/en/5.2/intro/contributing/#writing-some-tests-for-your-ticket)
   当前已要求保留触发条件及修订后复现，但未明确验证测试对旧缺陷有检出力。
   这是较直接的候选补充。推广判断：还需核实失败原因对应目标缺陷，
   缺少依赖、用例未被发现等问题不能代替该证据。
   无法运行旧版时如实保留限制，不把所有任务改造成从头执行 TDD。

3. **对关键断言做少量定向破坏，检查测试是否敏感。**
   测试已绿但仍怀疑漏检时，在隔离副本反转一项边界、去掉一项必要行为，
   看相关测试能否失败。恢复后验证最终版本。
   机制源于 [T03](https://stryker-mutator.io/docs/)，少量人工变异是本报告的轻量适配，
   不等于必须装框架。当前只明确新增检查脚本用正反例自测，
   此项可延伸到重要回归测试和断言本身。
   成本随变异数量增长，存活结果需排除[等价变异](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/)，
   不追求固定分数，不据存活变异直接要求修改产品。

4. **难以逐例给答案时，选少量领域属性或变形关系。**
   从真实契约选往返、幂等、守恒、对参考实现等价，
   或在明确成立的前提下改变输入并检查输出关系。
   [T04](https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html#when-to-use-hypothesis-and-property-based-testing)、
   [T05](https://github.com/tum-i4/gemtest/blob/f13150ebf86ddf5e350dfba351381581beb23ddb/README.md)
   当前已有不变量与独立重算，新增价值是输入变换及多次运行间的关系验证。
   适合转换、算法与数据处理，不要求引入生成框架。
   本报告推断：关系只约束部分行为，常量输出也可能满足幂等，
   编解码两端也可能共享错误，因此应保留关键已知答案，不能把性质通过等同整体正确。

5. **用影响关系决定检查范围，再用覆盖报告找实际漏跑路径。**
   项目已有依赖图时，由变更向调用方或消费者找受影响测试，
   而非只按改动文件同名选择。用分支报告看关键条件的另一侧是否真正运行。
   [T08](https://bazel.build/query/guide#reverse-dependencies)、
   [T06](https://coverage.readthedocs.io/en/latest/branch.html)
   当前有相邻路径和受影响检查重跑要求，此项补充可操作的范围依据。
   低成本前提是已有项目工具，不为一次检查建设依赖系统。
   本报告推断：图中未建模的配置、动态依赖与环境行为仍需人工判断。
   覆盖率仅说明触达，不能证明断言正确，不推广 Hypothesis 项目的满覆盖门槛。

6. **在结论里保留对结果有影响的保真缺口。**
   对依赖和配置相关改动，识别测试实际替换了哪些依赖、采用何种配置与数据。
   若关键风险就在被替换的交互边界，补一条授权范围内的真实组合路径，
   或明确尚未验证的部分。[T07](https://abseil.io/resources/swe-book/html/ch14.html)
   当前已要求真实组合路径并区分推演和执行，主要补充选择真实测试的具体触发点。
   不要求所有任务连生产系统，也不要求测试报告罗列所有无关环境差异。

## 去重、未收录及证据边界

- 独立预期、正反例、不变量、关键边界、失败分类、最终版本与受影响检查重跑，
  当前已存在。无需以新术语重写一遍，候选价值应落在上述具体缺口。
- Google 同书第 13 章、Stryker 多平台配置、Coverage.py 旧版文档，
  与主来源机制重叠，未另编号或据此增加来源数量。
- Chen 等 2018 综述的 HKU PDF 两次超时，Nottingham 存储库 403。
  1998 原论文 PDF 可打开，但正文编码混乱，网页截图只返回引用文本，
  未得到可读图像。本机下载又被不可达网络代理阻断，因此未以摘要冒充已读原文。
- GeMTest 2025 原论文两条 TUM PDF 地址均返回 429，
  改用作者仓库原文支撑方法，不据搜索摘要声称已核实论文实验结果。
- Hillel Wayne 及其他解释文章仅作检索线索，不作为原始机制证据。
  未将搜索得到的外部 Skill 正文纳入本路线，也未执行其中任何指令。
- 这些资料支持机制及其局限，不能据此估计本 Skill 的收益幅度。
  本轮没有进行框架基准测试、真实缺陷检出率比较或跨项目成本评测。
