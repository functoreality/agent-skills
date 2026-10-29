# 参考材料与本地设置

本项目用《创造是一门精密的科学》的案例检验因果链分析和目的手段分析。
公开仓库保留题答摘要、必要短摘录、分析报告、页码和校验指纹。
完整扫描PDF、完整OCR、书页截图及原始长段揭答材料不随仓库发布。
仓库自身的许可证不代表这些未分发参考材料已获相同许可。

## 原书

- 《创造是一门精密的科学》，吴光威、刘树兰编译，北京航空航天大学出版社。
- 本次使用的扫描PDF共224个物理页。
- 索引的Page N指PDF物理页序；所核页段的印刷页码为N−7。
- 引用还保留OCR文件内的行号，方便本地精确定位。
- 未公开的材料链接注明“本地材料”，在GitHub上不能直接打开是预期行为。

## 本地目录

以下路径均相对于当前案例目录：

```text
_private/
  references/altshuller/
    Altshuller-creativity-as-an-exact-science.pdf
    Altshuller-creativity-as-an-exact-science.pages-1-78.md
    Altshuller-creativity-as-an-exact-science.pages-79-151.md
    Altshuller-creativity-as-an-exact-science.pages-152-219.md
  evidence/pdf-check/           # 书页截图，按需在本地生成
  frozen-inputs/                # 原始揭答归档、旧冻结协议
  history/                     # 公开整理前的本地提交备份
  input-audit/                 # 全量资料审核与定点核字原始记录
  question-packets-v2/          # 按审核原文构建的基础/增补题干包
  work/                        # 临时文件
```

整个`_private/`被本目录的`.gitignore`忽略。
请把自己合法取得的资料副本放到这些路径，不要提交或上传整个目录。
文件名固定，使不同电脑上的引用保持一致，个人文件系统路径不进入公开文档。
其他仓库目录的图片和追踪规则不受影响。

可手动复制四份参考文件，或执行：

```bash
python3 scripts/copy_references.py --pdf /path/to/book.pdf --ocr-dir /path/to/ocr-folder
```

命令行路径只在本地使用，不会写进公开清单。
脚本会核对预期指纹，既有内容不同则停止，不覆盖用户已有材料。
原书与OCR的预期SHA256见[输入清单](manifest.json)和[PDF清单](pdf-manifest.json)。
OCR版本或分段不同会使行号与指纹不一致，不应静默替换成同一个实验输入。

## 没有参考材料也能做什么

直接阅读[题目摘要](../inventory/questions.md)、[答案摘要](../inventory/answers.md)、
[试点报告](../pilot/summary.md)和方法观察，不需要完整PDF或OCR。
运行公开检查：

```bash
python3 scripts/check_artifacts.py
```

该模式检查公开文件、可公开验证的链接与候选指纹，
明确跳过未公开原文、截图和原始协议验证，不把跳过写成已核验通过。
清单可从公开的分段摘要重建，材料缺失时会报告原文可用性：

```bash
python3 scripts/build_inventory.py
```

有完整本地材料时，运行：

```bash
python3 scripts/check_artifacts.py --with-private
```

该模式额外核验原文页码、行号、参考文件指纹及已登记的私有实验输入。
书页截图与最初归档输入并非普通新克隆自动拥有，缺失会如实报出。
首次整理保存的旧协议包含当时的安装路径，只在私有目录留存。
现行公开协议使用仓库相对路径，不能拿新协议冒充旧协议的哈希原件。
三个答案前候选及题干未因目录迁移改写。

初始清单与已完成轮次的Skill输入按清单对应的Git提交读取并核验，
不要求活动Skill永远保持旧版本。进行中的轮次及冻结脚本仍检查当前输入，
防止轮中变更。历史提交缺失时会报告无法核验，不更新旧哈希掩盖缺口。
轮次的`baseline_commit`及各文件SHA256是复验入口。

## 日常维护与发布

- 新摘录只保留解题需要的题干、答案或短句，不连续搬运全章论述。
- 原文或截图补查写清来源页码，原文件留在`_private/`。
- 公开材料使用相对路径，不写个人主目录或本机安装位置。
- 题解索引与报告只引用本地副本，不依赖原来放在下载或笔记目录的文件。
- 当前目录仅追踪UTF-8纯文本，不提交PDF、图片或其他二进制附件。
- 提交前运行公开检查，发布前再运行历史检查：

```bash
python3 scripts/check_artifacts.py --history
```

[Git的gitignore文档](https://git-scm.com/docs/gitignore)说明忽略规则不影响已追踪文件。
历史中的截图需另行处理，不能只靠添加忽略规则。
历史处理与备份范围见[公开目录整理记录](../reviews/publication-review.md)。

## 全量题干复核后的输入

全部205条的[保真审核](../input-audit/README.md)另列状态和任务类型。
完整题干私有保存，公开只保留原文范围、字符边界、PDF校正与哈希。
prepare_case_input.py可用自有OCR重新准备就绪条目，不依赖个人机器路径。
后文补充条件和首次题干分别生成，旧10题的冻结输入不覆盖。
