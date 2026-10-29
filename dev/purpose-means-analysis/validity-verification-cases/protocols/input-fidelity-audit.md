# 全量题干保真与盲试边界复核

本次只复核资料，不试解、不修改Skill、不重跑案例。
按用户最新要求覆盖全部205条记录，包括既有10题和未来可能试的记录。
资料审核者可以读题解及原书，但以后不能承担这些题的独立盲解。
完整题干片段只写_private，公开报告仅写差异、引用和状态。

## 逐条检查

1. 读取分配记录的全部question_refs及相邻完整段落，沿跨页和指代补足上下文。
   也检查同题后文重述，不能把解法推理冒充原题条件。
   现有摘要和行范围只是定位起点，不预设它们完整或不泄答。
2. 核对目标、对象及结构关系、数值/单位、时间顺序、材料/能量/信息、
   允许与禁止、精度、已有失败尝试、原题自带提示、问题原本要求。
   必要时查看答案段以确定题干在哪里结束，勿把答案并入题干。
3. 区分独立题干、依赖上下文的叙述、问题与答案交织的实例、仅有回指。
   如果没有完整独立的问题，明确标缺失，不能根据答案反造题干后称原题。
4. 检查标题或摘要是否提前给出解法。未来输入用中性编号标题，
   不用可能泄答的旧标题、关键词、方法归因或复盘提示。
5. 原题提示单列hint，同题后文新增条件标later_constraint。
   仅因答案用了某材料或几何条件，不能把它补成题干事实。
6. 图示被题干依赖、OCR关键字模糊或公式缺失时标记待核，不猜补。
   本阶段不批量渲染PDF，必要页及原因登记后由主Agent安排定点复核。

## 私有输出格式

写分配的_private/input-audit/part-N.json，数组，每条：

- id，input_form：standalone/contextual/solution_embedded/reference_only。
- status：ready_text/needs_figure/needs_ocr/insufficient_statement。
  ready_text仅表示可构造无答案的完整原文文本输入，不表示已验证题解或所有PDF页。
- reviewed_refs：实际核对的来源范围，逐项file/line_start/line_end/page。
- segments：无答案的原文题干片段。
  每片段包含file/line_start/line_end/page、role、text。
  role为statement/context/hint/later_constraint。
  text从对应原文逐字取得，可仅取同行中的题干部分，不能含答案。
  text去空白后必须是相应原文范围去空白后的连续子串。
  如有跨段跳过理论或答案，使用多个片段，不用自写桥接句。
- findings：数组，type（omission/addition/meaning_shift/answer_leak/
  missing_context/figure_dependency/ocr_uncertainty/no_material_difference），
  detail（中文摘要）、impact（none/possible/material）、source_refs。
  必须具体说明现有摘要少了什么、添了什么或为何不能直接用于盲解。
- packet_notes：只描述必要指代或OCR疑点，不能补入方案思路。
- figure_requests：必要PDF页和原因，数组，没有则空。
- summary：一句审核结论，不能仅写“通过”。

对needs_figure/needs_ocr/insufficient_statement仍可保留已确认的题干片段，
但不得冒充可直接试解。整条几乎只有解法的记录允许segments为空。
不要因旧摘要很短就自动判缺失，也不要因有题号就默认ready。
已有后文提示不是全部自动加入，先分清其是任务重述还是解题展开。

文件名英文，正文中文，引用仅使用本目录相对路径。
不得改既有question、冻结稿、manifest、公开索引或其他Agent输出。
完成后报告条数、状态统计、关键差异及必须核图的页，停止等待。
