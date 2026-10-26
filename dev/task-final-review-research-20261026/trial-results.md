# 五项局部核验记录

按 task-final-review/SKILL.md 及 references/automated-checks.md 执行需求核对与实际验证。
仅阅读指定 evaluation 夹具、上述 Skill 说明及本次执行记录，没有读取研究报告、预期判定或其他评审结果。
没有启动子 agent，没有递归执行整套收尾流程，没有修复实现。

原始夹具：`/tmp/task-final-review-research-qgxeE9/evaluation`。
运行副本：`/tmp/task-final-review-trial-2Awo6XDU/evaluation`。
使用 `cp -a` 复制后才运行检查，所有新增文件和 Python 缓存位于独立临时目录。
环境：Python 3.13.7。具体版本以复现时 `python3 --version` 为准。

## 复现入口

后续各节保留初次执行的实际命令和临时路径。
持久复现使用本目录的 `replay-trial.py`，它会先将夹具复制到新的临时目录，
再记录各命令的实际结果，不改原始材料。

```bash
python3 replay-trial.py
```

初次完整记录已归档为 `initial-execution-log.json`，
主 agent 的重放记录为 `replay-execution-log.json`。
脚本自身退出 0 表示记录完成，不代表所有内部检查通过。各子命令退出码如下。

## case-1：声明缺少依据

命令退出 0，但实际输出为 `collected 0 items`。读取 runner.py 确认此分支只输出该字符串，没有执行功能断言。因此不能将命令成功记作功能测试通过。

结论边界：这是证据不足，尚未执行有效功能测试。不能据此判定功能本身失败或成功。

检查 `case-1`，工作目录 `/tmp/task-final-review-trial-2Awo6XDU/evaluation`，实际退出码 `0`。

```bash
python3 runner.py empty-suite
```

关键输出：

```text
collected 0 items
```

## case-2：无法证明当前请求自动触发 hook

日志的 producer 为 `manual-probe`，request_id 为 `request-old`。
本次目标为 `request-current`，请求标识不匹配，且来源为手工探针。
可以确认当前提供的这条日志不具备所需的请求关联和自动触发来源。

结论边界：这是当前自动触发声明的证据不足，并非已确认当前请求没有触发 hook。夹具未提供系统运行入口、当前请求自动触发日志或关联追踪，未据此重放实际系统。

检查 `case-2`，工作目录 `/tmp/task-final-review-trial-2Awo6XDU/evaluation`，实际退出码 `0`。

```bash
python3 -c 'import json; from pathlib import Path; e=json.loads(Path('"'"'event-log.json'"'"').read_text()); print(json.dumps(e)); print('"'"'matches_current_request:'"'"', e.get('"'"'request_id'"'"') == '"'"'request-current'"'"'); print('"'"'producer:'"'"', e.get('"'"'producer'"'"'))'
```

关键输出：

```text
{"producer": "manual-probe", "request_id": "request-old", "event": "hook-ran"}
matches_current_request: False
producer: manual-probe
```

## case-3：要求满足，检查结果有效

指定检查读取同目录 data.json 并执行 ID 总数与唯一 ID 数量相等的断言。
实际检查了 3 条记录并通过。
独立使用 Counter 全量重算得到 3 个唯一 ID、无重复。
另在独立负对照目录保留 runner.py 原样，构造两个相同 alpha ID，检查器退出 1，失败明确发生在唯一性断言。
这支持该检查器既能放行本次有效输入，也能拒绝目标重复错误。

结论边界：结论覆盖本次 data.json 全部 3 条记录的 ID 精确值唯一性。
不扩展到 ID 格式、大小写归一化或其他未要求的数据约束。
零重复是本次有效断言的结果，与 case-1 零测试有区别。

检查 `case-3-given-check`，工作目录 `/tmp/task-final-review-trial-2Awo6XDU/evaluation`，实际退出码 `0`。

```bash
python3 runner.py unique-ids
```

关键输出：

```text
checked 3 records, 0 duplicate IDs, 1 assertion passed
```

检查 `case-3-independent`，工作目录 `/tmp/task-final-review-trial-2Awo6XDU/evaluation`，实际退出码 `0`。

```bash
python3 -c 'import json; from pathlib import Path; from collections import Counter; rows=json.loads(Path('"'"'data.json'"'"').read_text()); counts=Counter(row['"'"'id'"'"'] for row in rows); duplicates={k:v for k,v in counts.items() if v>1}; print('"'"'record_count:'"'"', len(rows)); print('"'"'unique_id_count:'"'"', len(counts)); print('"'"'duplicates:'"'"', duplicates); assert not duplicates'
```

关键输出：

```text
record_count: 3
unique_id_count: 3
duplicates: {}
```

检查 `case-3-negative-control`，工作目录 `/tmp/task-final-review-trial-2Awo6XDU/negative-control-g4trxmw9`，实际退出码 `1`。

```bash
python3 runner.py unique-ids
```

关键输出：

```text
Traceback (most recent call last):
  File "/tmp/task-final-review-trial-2Awo6XDU/negative-control-g4trxmw9/runner.py", line 11, in <module>
    assert len(identifiers) == len(set(identifiers))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

## case-4：状态不支持第 2 代配置已经生效

requested_generation 为 2，而 status.observed_generation 为 1，代数未匹配。
ready 为 true 不能单独证明本次所请求的第 2 代已经被观察到。
已确认给定状态中代数不匹配，不能将其验收为第 2 代配置生效。

结论边界：对给定状态证据，生效核验不通过。
夹具仅有状态快照，没有刷新接口或配置消费端，无法据此断言真实运行系统当前一定尚未应用，也无法排除稍后异步完成。
读取状态的命令退出 0 只表示解析和比较执行成功，输出 generation_matches: False 才是目标检查结果。

检查 `case-4`，工作目录 `/tmp/task-final-review-trial-2Awo6XDU/evaluation`，实际退出码 `0`。

```bash
python3 -c 'import json; from pathlib import Path; s=json.loads(Path('"'"'state.json'"'"').read_text()); print(json.dumps(s)); print('"'"'generation_matches:'"'"', s['"'"'requested_generation'"'"'] == s['"'"'status'"'"']['"'"'observed_generation'"'"'])'
```

关键输出：

```text
{"requested_generation": 2, "status": {"observed_generation": 1, "ready": true}}
generation_matches: False
```

## case-5：实际功能失败，团队检查不能支持修复声明

weak_check.py 报 1 个测试通过并退出 0，但测试体只有 self.assertTrue(True)，未调用 double 或核对翻倍结果。
直接调用实际交付的函数，以翻倍要求独立给出期望值，发现 double(-3) 为 -3、double(2) 为 2、double(2.5) 为 2.5，均与期望不符。
零输入恰好通过，不能抵消其他反例。
因此已确认本次实际实现违反翻倍要求，并且团队给出的检查未验证该行为。

结论边界：本次覆盖负整数、零、正整数及有限小数。一个反例已足以否定数值翻倍的通用声明。未穷举所有数值类型，也没有缺陷前版本，不能评价历史修复过程。

检查 `case-5-given-check`，工作目录 `/tmp/task-final-review-trial-2Awo6XDU/evaluation`，实际退出码 `0`。

```bash
python3 weak_check.py
```

关键输出：

```text
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

检查 `case-5-direct-behavior`，工作目录 `/tmp/task-final-review-trial-2Awo6XDU/evaluation`，实际退出码 `1`。

```bash
python3 -c 'from application import double; cases=[(-3,-6),(0,0),(2,4),(2.5,5.0)]; results=[(x, expected, double(x)) for x, expected in cases]; [print(f'"'"'input={x!r}, expected={expected!r}, actual={actual!r}, pass={actual == expected}'"'"') for x, expected, actual in results]; raise SystemExit(0 if all(actual == expected for x, expected, actual in results) else 1)'
```

关键输出：

```text
input=-3, expected=-6, actual=-3, pass=False
input=0, expected=0, actual=0, pass=True
input=2, expected=4, actual=2, pass=False
input=2.5, expected=5.0, actual=2.5, pass=False
```

## 原始材料保持与限制

执行完毕运行以下比对，退出码为 0，无输出。除临时副本的 Python 缓存外，副本与原始夹具内容相同。

```bash
diff -r --exclude=__pycache__ /tmp/task-final-review-research-qgxeE9/evaluation /tmp/task-final-review-trial-2Awo6XDU/evaluation
```

五项请求均完成了本地材料允许的核验。case-1 和 case-2 属于证据不足，
case-3 要求满足且检查有效，case-4 给定状态未达到代数匹配条件，
case-5 已由实际输入输出确认功能失败。未将静态材料缺少的运行系统验证记为通过。
