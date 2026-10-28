# 原书 PDF 定点复核

本轮只补充 OCR 与图示证据，不是全量试解，也不启动任何额外 Agent。
用户尚未批准正式全量分析，原有停止点保持。

PDF：../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf
共224页，无文本层。页码先用PDF物理页序（从1开始），再核对扫描页脚印刷页码，
确认是否与既有 Markdown 的 Page 标签对应。

## 操作

- 先读 当前环境提供的 PDF Skill。
- 仅读分配页段。先用pdftoppm生成约180dpi的缩略页或拼图，
  必要时对关键文字、线条局部提高到300dpi，或裁切，不大量看原始大图。
- 可用 tools.view_image 查看本地渲染。Python有需要优先使用
  python3，或系统标准库。
- 原始PDF、三个OCR文件、Skill、已冻结的before-answer.md、question.md、
  protocols/solver.md、pilot/freeze.json均不修改。
- 只写分配的报告与证据图文件。无Git提交，不删除文件，禁止rm。
- 图像只存直接影响结论的少量页或局部，不复制26MB原PDF进仓库。
  临时渲染存/tmp，提交候选证据存_private/evidence/pdf-check/自己任务子目录。

## 报告

写 reviews/pdf/<assigned-name>.md：

1. 实际读的PDF物理页、印刷页及与OCR页的对应。
2. 哪些细节是直接可见，给出精确字词/图中字母/线条关系。
3. 与OCR及既有判断有何出入，区分OCR错误与原书本身如此。
4. 该出入是否会改变案例题干、原书解法、既有分类或仅改变不确定性。
5. 没有复核的内容及仍不可判的点。不要把示意图自动当作实际可实现性证明。
6. 每项关键发现链接到PDF的#page=N和保存的证据图。

如需JSON修正候选，仅给主Agent易采纳的具体字段建议，不编辑canonical索引。
不要顺便设计新解法，不重写原报告，不把本轮新证据回填到答案前记录。
