# OCR 与原书排印定点核验

本轮只核验指定疑点，不作全书扫描或新增试解。
按 `protocols/pdf-check.md` 和 PDF Skill 操作，先看180 dpi接触表，
关键字和数字再看300 dpi局部。未修改原PDF、OCR、canonical索引或冻结试点文件。

## 页码与证据范围

所核PDF为
[原书扫描PDF](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf)。
下列物理页与现有OCR的 `Page N` 标签相同，印刷页均为物理页减7。
补看77页用于定位T27，补看106页仅查主Agent追加的容器回提号。

| PDF物理页 / OCR Page | 印刷页 | 实际读取范围 |
| --- | --- | --- |
| 27、28 | 20、21 | T04题干、冰与磨料解法 |
| 75、76 | 68、69 | T26物质名及温度 |
| 77 | 70 | 仅T27题干术语，未分析同页其他题 |
| 78 | 71 | T31题干 |
| 79、80、81 | 72、73、74 | T31回提号及连续文字分析 |
| 106 | 99 | 仅“喷雾器”“容器”回提号局部 |
| 137 | 130 | 仅荧光粉、易熔垫回提号 |
| 181、182、183、184、185 | 174、175、176、177、178 | 题号、章标题及中间无编号段落的连续性 |

## 1. T04：冰与磨料解法可确认

[物理27页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=27)
清楚印“课题4”，题干要求向抛光器下供给冷却液，
并对比表面“有窟窿”与“无窟窿”的工作效果。
[物理28页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=28)
明确写抛光器由“冰及冻结在冰里的磨料颗粒”组成，
抛光时冰融化，使抛光表面保持刚性，又能让大量冷却水全面通过。

这与OCR Page28第997–1000行的主要内容一致。
Page28开头的损坏没有遮掉解法关键句，可关闭“冰与磨料是否为OCR拼接或猜补”的疑点。
题干自身没有冰、相变或材料替换提示，现有题干和解法边界可保持。
本次未核验该解法的工程参数或实际抛光性能。

证据：[题干与解法局部](../../_private/evidence/pdf-check/ocr/p027-028-t04.png)。

## 2. T26：原词与温度均可读，温度逻辑疑点仍保留

[物理75页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=75)
可逐字读到“阿利芙干性油”六字，整句开头为“在水化阿利芙干性油时”。
本次只确认原书词形，不据此认定其对应的现代化学名称。
“课题26”题号也正常，OCR的“课显26”属于误识别。

该页温度确实印为“在加热高于25°C时”，数字25后没有可见的尾0。
不能把它静默改为250°C。
[物理76页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=76)
直接可见的温度为：

- 建议在700～1100°C下加热以跃过温度危险区。
- 催化剂在350°C时失去活性。
- 加热到500°C时更糟。
- “谁能想到从300°C起会出现安全区呢？”
- 另提可试验把物质加热到1000°C。

因此，25°C、350°C与“从300°C起”之间的既有疑点来自原书现有排印，
本次不能归为OCR误识别，也没有证据判断哪一个数字应改。
可关闭精确字形读取问题，但仍保留阈值逻辑及化学名称解释的不确定性。
这不会改变“高温快速处理”的原书解法方向，不能据此认定所有给定温度均已自洽。

证据：[物质名与温度局部](../../_private/evidence/pdf-check/ocr/p075-076-t26.png)。

## 3. T27：“光谱射线”为原书用词

T27实际在
[物理77页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=77)，
不在75–76页。题号清楚为“课题27”，OCR的“瀑®27”为误识别。
禁用条件确实印作“又不允许采用反光镜和光谱射线的设计结构”。
“光谱射线”四字可以辨认，不宜为了术语自然程度而改写成其他词。

可关闭“准确词形待核原图”的OCR疑点，仍可保留原术语含义需解释的限制。
本次未读其后文答案，未判断这一禁用条件的技术含义。

证据：[T27题干局部](../../_private/evidence/pdf-check/ocr/p077-t27.png)。

## 4. T31：79页是OCR错号，题干确有气密、高温、高压

[物理78页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=78)
题号是“课题31”。以下条件均直接可见：

- “坚固的气密的金属容器”。
- 放置30～40块不同合金，灌满侵蚀性液体。
- 试验液体“在高温以及高压条件下对合金表面的作用”。
- 液体也侵蚀容器壁，导致使用贵重金属、造价太高。

[物理79页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=79)
清楚印“以课题31为例”。
OCR part2第25行的“以课题3的为例”是OCR误识别，
不是此处原书错引。可关闭这个配题疑点，恢复为T31的直接回提。

[物理80页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=80)
至
[物理81页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=81)
的连续分析归于同一容器题。
81页明确说不能在时间上分开，因为液体应不断作用于制品，
继而提出在空间上分开：“有合金块的地方有液体，有容器的地方无液体”。
该局部文字没有同时交代如何在高温、高压、气密条件下实现完整试验装置。
因此，本次确认了题干约束的真实性，但不以这段文字直接证明这些约束已经全部满足。

证据：
[题干和31回提号](../../_private/evidence/pdf-check/ocr/p078-079-t31-number.png)，
[80–81页空间分离文字](../../_private/evidence/pdf-check/ocr/p080-081-t31-separation.png)。

## 5. 106页：“课题29的容器”是原书错引

按主Agent追加要求，仅定点核验
[物理106页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=106)
对应OCR part2第1003行附近。
原书清楚印：
“电极不在其列（像课题53的喷雾器和课题29的容器一样）”。

这里“29”与现有OCR一致，因此是原书现有排印，不能像79页一样归为OCR错误。
结合已核T31题干与79页直接回提，不能因这个29而把容器解法改归真正的T29。
同一行的前一个题号实际为53，OCR误作3。
本次未读T53题干，不以此额外作喷雾器机制配题。

证据：[106页回提号局部](../../_private/evidence/pdf-check/ocr/p106-container-reference.png)。

## 6. 137页：5与8均为原书现有排印

[物理137页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=137)
明确印“在课题5中预先加入荧光粉保证了反馈性”，
随后是“而在课题8中是预先用易熔垫来实现反馈性的”。
数字5、8及“荧光粉”“易熔垫”均可直接辨认。

所以OCR part2第2214–2215行没有错认这两个回提号。
应将这两处标作原书现有错引，不能以修复OCR为由改写原始转写。
既有按机制把荧光检漏归T09、易熔垫归T12的处理不因这两个印刷号而推翻。
本次没有重读T09、T12前部题干，只关闭“137页是否被OCR错成5或8”的疑点，
不新增独立配题证明。

证据：[137页回提号局部](../../_private/evidence/pdf-check/ocr/p137-references.png)。

## 7. T60：指定相邻页确实没有课题60标签

[物理181页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=181)
印刷174页，清楚列“课题58”“课题59”。
59是装有罐头制品的瓶子检验瓶盖严密性，其后注释结束本页。

[物理182页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=182)
印刷175页，以“第八章 发明的科学”“第一节 靠机遇发现”开始新章，
随后是无编号的转炉内衬实例。
[物理183页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=183)
印刷176页，接着是无编号的双液体液压实例。
[物理184页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=184)
印刷177页，继续前段并转到无编号的玻璃熔炉修理实例，
页末明写“还有一个有趣的例子，请看课题61”。
[物理185页](../../_private/references/altshuller/Altshuller-creativity-as-an-exact-science.pdf#page=185)
印刷178页，页首清楚为“课题61”，内容为金属电镀润滑油。

这些连续页的印刷页码没有跳页，且中间段落没有课题60题号。
可关闭“181–185页的OCR吞掉了一个可见课题60标签”的疑点。
这只证明所核页段原书本身从59过渡到61，
不证明全书其他位置一定没有60，也无法确定作者或排印时为何跳号。
不把无编号实例猜补为T60。

证据：[181–185页连续接触表](../../_private/evidence/pdf-check/ocr/p181-185-numbering.jpg)。

## 供主Agent采纳的字段建议

本报告不直接改索引，建议在后续统一修订时：

- T04：保留现有冰与磨料解法及其答案引用，关闭Page28开头乱码影响关键解法的疑点。
- T26：可把 `original_label` 的OCR异形与规范题号分开。
  保留原词“阿利芙干性油”和原温度，
  将不确定性改为“原书词形已核，名称解释及温度逻辑未解”。
- T27：记录原书正常题号与“光谱射线”原词，关闭词形待核项。
- T31：79页 `original_label` 候选为“以课题31为例”，
  说明现有OCR误识别；106页的“课题29的容器”保留为原书错引。
  题干气密、高温、高压条件应保留。
- T08、T09、T12相关137页不确定性：
  将“可能是OCR错号”收窄为“原书印5和8，配题依机制核对”。
- coverage中的T60：继续记未找到可归属编号题，
  可补充“物理181–185已查原书，59到61之间无60标签”。

## 未复核与保留限制

未核全书T60其他可能位置，未核这些题的外文原版、专利或现代技术资料，
未对T26温度作化学推断，未检验各解法在完整题干条件下的工程可行性。
除所列物理页及106页指定局部外，未扩读其他章节。
本报告只提供排印与OCR证据，不改变原有正式分析停止点。
