## User

SKILL.md 帮我评审一下现在你看到的这个 Skill，比如里面有没有哪些内容是表述不清晰或者让人费解的？某些要求其实是有适用范围或者潜在副作用的。或者如果你觉得这些某些要求你搞不懂它为什么要放在这里，显得有些莫名其妙，或者有些东西你觉得不应该这么表述。总之，有任何你觉得不合理的地方，你都可以向我提出。这是一个 Skill 的评审，我只是想知道它里面是否有可以改进的地方。

## Assistant

我会按「Skill 评审」的方式审读当前 `SKILL.md`，重点找表述歧义、触发边界不清、隐含副作用，以及看起来缺少理由或不适合写进 Skill 的要求。只提出建议，不会改动文件。

## Assistant

我会使用 `skill-refiner` 的评审框架，因为你的目标正是检查并改进一个 Skill 的规则质量与可执行性；它会帮助我把“读起来别扭”的感觉落实为可验证的问题和改进方向。

## Assistant

整体判断：这个 Skill 的核心框架是扎实的，尤其是“直接性、层级一致性、避免把测试混入实现树”这些原则很有价值。主要问题不在理念，而在于把不少“有帮助的检查动作”写成了无条件的硬流程，容易让小任务变得沉重，也会在真实工程设计中忽略约束、证据和不确定性。

我认为值得优先讨论的点如下。

1. 适用范围对“改进型设计”排除得过宽  
   [第 36 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:36>)、[第 125 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:125>) 将“降低现有系统延迟”归为不适用。但很多任务恰恰是“重新设计某个子系统，以满足时延上限”，并不只是局部打补丁。  
   问题在于“降低延迟”既可能是局部优化，也可能是新系统的硬目标，单凭措辞无法区分。更好的边界应是：是否允许重新选择关键结构和实现路径，而不是目标是否表现为“改进指标”。

2. 把资源、成本、风险一律后置，会误伤有硬约束的设计  
   [第 128 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:128>)、[第 150 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:150>)、[第 475 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:475>) 的意思是，约束只影响优先级，不能提前排除方案。  
   这适合发散探索，但不适合“必须离线”“法规禁止采集某类数据”“预算上限固定”“只能使用现有硬件”这类不可违反的约束。否则会系统性地产生不合格方案。应区分：

   - 硬约束：从根或上层方案空间就应限制
   - 偏好、预算、资源不足：用于排序或标注代价
   - 尚未确认的约束：先保留分支并标明假设

3. “先列方案，不评估可行性”与“设计新系统”存在张力  
   [第 278 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:278>) 明确说除非用户要求，否则不必证明可行或有效。  
   对论文结构还原，这很合理；对从头设计则风险较大。一个“工作原理不同”的分支可能根本不满足基本物理、接口或法规条件。建议至少要求做低成本的“明显不可行性筛除”，并把未验证可行性标注为假设，而不是把可行性完全留到链外。

4. “And 局部完备性”表述得像可证明的充分性，但很多场景做不到  
   [第 283 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:283>) 要问“子节点全部完成，父目的是否仍可能无法实现”。  
   在数学定义或封闭系统里，这是好检查；但工程系统中，外部环境、模型误差、接口失败等总会使答案为“仍可能”。同时第 278 行又不要求验证效果，形成内在拉扯。建议将其限定为“在已声明假设和分析范围内，是否遗漏了本层应显式表达的关键条件”，避免伪精确。

5. 对可量化节点“必须先写严格公式”太强  
   [第 239 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:239>)。  
   许多量化目标只有操作性定义、经验指标或统计估计，没有合适的直接公式。强行公式化容易制造形式感，甚至把代理指标误当目标。可以改成“若存在且有助于拆分，优先使用定义、公式或可操作判据”。

6. 强制创建文件和 Tab 缩进，不适合全部触发场景  
   [第 69 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:69>)、[第 140 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:140>)。description 也覆盖“解释方法各部分如何服务整体功能”这一类可能只需简短回答的请求。此时立即新建文件，会显得动作过度。  
   另外 Tab 在标准 Markdown 渲染器中兼容性不稳定，常被视为代码缩进。若这是为了某个大纲工具，应写明依赖和替代格式；否则更适合默认空格缩进或由用户选择。

7. 工作流仪式感偏重，缺少按任务规模降级的规则  
   [第 338 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:338>) 到 [第 424 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:424>) 要求结构扫描、重读 Skill 和参考文件、两轮无修改复盘，并在环境允许时独立审查。  
   这些动作单独都合理，组合后对十几个节点的小树也会非常昂贵，且容易让模型优先满足流程，而不是回答用户真正关心的分支。建议定义轻量、中等、复杂三档，按节点数、风险、是否用于决策、是否涉及论文还原来决定检查强度。

8. 独立审查的“超过 5 处问题、最多 3 次”阈值缺少理由  
   [第 422 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:422>)。  
   一处严重的根目的错误，远比六处措辞问题重要；而累计三轮仍有六处实质问题时，流程也会停止。这个数值既不能衡量质量，也会诱导审查者按数量输出。更好的结束条件应看“是否仍有未解决的高严重度问题”，并把审查作为复杂任务的可选质量门。

9. 已知方案还原没有要求区分“材料事实”和“分析者补出的桥接”  
   [第 54 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:54>) 与场景参考中“可补出作者省略的桥接层”共同构成风险。  
   对读者而言，“论文明确做了什么”和“分析者推断它必须隐含什么”是不同证据等级。当前规则允许补桥，却没有要求标记推断、依据或置信度，容易把解释性重构误读成论文原意。尤其用于评审、知识组织时，这是重要问题。

10. 队列、回指和关系语法有些不可恢复或不够明确  
   [第 141 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:141>) 要在记忆中维护队列，但 [第 410 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:410>) 又说可从叶节点恢复队列。若队列未写入文件，跨会话并不能真正恢复。  
   此外“上方已分析”“下方已分析”在移动节点后会失效，[第 184 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:184>)；`：or` 也没有明确规定它绑定的是“该父节点的全部子项”还是局部一组子项。可以考虑稳定节点标识或 Markdown 锚点，并用一个更小的完整例子定义关系标记的作用域。

11. “一直追问最终目的”可能造成不必要的重新框定  
   [第 122 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:122>)。  
   当用户已经明确要解释一个局部模块、一个论文机制或一个子系统时，持续追问“它最终服务什么”可能偏离用户任务，也可能把清晰的局部目的硬抬升。建议增加停止条件：当前目的已足以决定本次树的边界，且用户没有要求做更高层设计时，不必继续上溯。

12. “共享手段独立子树”是好想法，但标题层级和引用方式需要统一  
   [第 193 行](</home/yzh/Documents/projects/agent-skills/skills/purpose-means-analysis/SKILL.md:193>) 的例子在主文中再次使用一级标题 `# 单独分析`，与“一个文件一个分析”的结构不协调。文本引用也不可点击、不可校验。建议明确独立子树应作为二级标题、单独文件，还是带稳定锚点的附录。

如果只先改最关键的，我会优先处理 1、2、4、7、9：它们分别关系到适用范围、现实约束、逻辑严谨性、执行成本和事实可信度。

这些是诊断结论，尚未改动文件。你若认可这批问题，我下一步可以按“保守微调”或“重构流程层级”两种方向，提出具体改写方案和副作用推演。
