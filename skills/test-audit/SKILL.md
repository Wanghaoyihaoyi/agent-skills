---
name: test-audit
description: "有效测试与行为验收。用于编写、修改、审查或清理测试，以及修复回归与业务行为验收；按风险判断是否新增测试，建立独立预期和可复核证据。低风险文案允许零新增测试，不自动扩成全仓治理。"
---

# Test Audit

执行本 skill 时，在开始测试或行为验收前，先发送一条以 `🧪` 开头的简短进度消息，例如：`🧪 开始核对业务预期与验证边界。` 显式调用和自动选用都适用；不要只在最终回复中显示。仅创建、编辑或解释本 skill，不代表执行测试审查。

目标是用与风险相称、能够复核的证据确认业务行为。每项检查都要能说明：保护哪条规则、能发现什么错误、实际验证到哪一层。沿用当前任务的权限；修复任务完成实现与验证，只读审查不修改业务代码，保留他人改动和暂存状态。

先判断是否需要新增测试。需要编写或修改测试时使用 Authoring gate；审查已有测试时使用 Audit 的价值与保留标准。只有用户明确要求清理整个子系统测试面时才读 [CAMPAIGN.md](CAMPAIGN.md)，不因一次验收启动清理。

## 开始前：预期、边界与停止条件

用几句话说明以下三项，然后继续已授权的工作，不为例行计划等待确认：

- **行为与依据**：什么输入或事件应产生什么可观察结果，依据来自哪条用户要求或已确认合同。
- **风险与边界**：可能错在哪一层，哪些依赖真实运行，哪些被替代。
- **验证与停止**：最小充分的检查组合是什么，何时证据已足够。

范围从当前需求、明确故障、本次改动及直接依赖开始。复用已有测试、夹具、隔离环境和工具；只有具体证据缺口才引入依赖，不强制安装 Testcontainers、属性测试框架或 Playwright MCP。纯文案、注释及无行为影响的小改动允许直接检查、局部预览或已有检查，允许零新增测试；保留项目必要的构建、契约和 CI 门禁。

以明确要求和已确认业务合同确定预期，核对需求、日志、调用方、历史测试与当前实现。重要期待值不能取自被测生产函数或同一算法的复制品。预期不明时只能记录当前行为并注明“仅保护行为不变”；关键语义冲突无法自行解决时再追问，继续其他独立工作。

## 选择验证边界

| 风险所在 | 最小有效边界 |
| --- | --- |
| 计算、校验、状态转换 | 稳定函数、模块接口或事件入口的确定性测试。公共 API 不限于 HTTP；复杂内部算法可直接单测。 |
| 数据库、缓存、队列、事务、跨服务序列化 | 真正经过相关依赖的隔离集成测试；存储与恢复问题不能由内存替身证明。 |
| 重复、乱序、取消、重连 | 用受控事件、时钟或调度重现；串行重放不能代替真实并发语义验证。 |
| 页面关键流程 | 核对用户实际得到的页面结果，保留可重复步骤与断言。 |
| 真实模型选择、原生设备、音频与硬件 | 取得相应模型或设备证据；缺条件时完成可执行部分并标明缺口。 |

关键交互保留真实实现。可以替代昂贵外部服务、时钟、超时或难触发错误，但说明替代内容；不能把目标缺陷所在组件模拟成成功，也不绑定私有拆分或无关调用顺序。

断言业务状态与输出、正确的对象和身份、持久化与权限效果、必要副作用及禁止行为。非空、无异常、HTTP 202、工具被调用或日志成功只证明各自事实。仅当次数或顺序是合同的一部分时才断言交互细节，例如禁止重复扣款、确认后才能执行。

等待明确状态或事件并设置合理超时；不固定长等待、不重复直到变绿。隔离数据与身份，保留随机失败输入或种子。测试断言保持简单，不用条件分支跳过核心断言，不吞异常、不写永真断言。测试失败先核对独立业务预期，只有证据证明测试过时或错误才修改并说明依据；不得为通过而删断言、放宽容差或无依据跳过。

## Authoring gate

Before adding any test, answer four questions; a missing answer means do not
add it yet:

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression makes it fail?
3. Why does existing coverage not already catch that failure? Each contract has
   one primary test owner at the strongest boundary; another layer needs its
   own distinct risk, such as a transport or lifecycle failure the owner cannot
   reach. Prefer extending a table-driven case or shared fixture over a
   near-duplicate test; consolidate duplicated setup in the same change.
4. Does it need a production seam (export, flag, wrapper, injection hook) that no
   production caller needs? If yes, move the test to the real boundary instead.

Use the relevant [junk patterns](#junk-patterns) to challenge the test; keep it
when the [retention bar](#retention-bar) names an independent contract. A test
that breaks under behavior-preserving refactoring is suspect, not automatically
invalid: public names, bytes, packaging and architecture may be the contract.
Otherwise move assertions to observable behavior at the owning boundary.

## 修复前后对照

优先在改实现前通过真实处理入口建立最小回归：同一测试在旧实现上因目标业务错误失败，修复后通过。再补充或复用直接受影响的合法行为，防止靠屏蔽所有结果消除错误。缺依赖、导入失败、服务未启动或测试自身出错都不算复现。

代码已改好时，在安全的隔离副本中对照修复前后，保护用户未提交修改；无法核对时明确写“未验证修复前失败”。偶发问题优先利用已捕获轨迹、受控时钟、事件顺序或并发屏障；有限次未复现只说明这些运行中未观察到问题。

## 按需读取专项验收

异步任务、语音、模型或设备验收，以及现有证据确有缺口而需要变异、属性、差分、契约或故障恢复验证时，读取 [专项行为验收](references/behavior-acceptance.md) 的对应部分。确定性回归已经充分时，不追加同义的高级测试；不向生产或共享工作区注入错误，不为对照重复真实扣费、发送或写入。

## CI 稳定性与运行成本

CI 偶发失败和耗时排查由 [hunt 的 CI 指引](../hunt/references/ci-maintenance.md) 承接运行历史、根因与收益分析；本 skill 负责检查修复后的测试是否仍保护真实行为。慢或偶发失败都不是删除测试的依据，不把重跑变绿当成修复；只有已证明无效或被更强证明替代的测试才进入删除审查。

## Junk patterns

The shared checklist for both modes: the authoring gate rejects a new test that
matches one, and audits hunt for existing tests that do.

- assertion-free coverage probes;
- self-comparisons and identity copiers;
- copied fixtures, inventories, manifests, or export lists;
- exact source, import, or string greps;
- private predicate or call-shape tests duplicated at real boundaries;
- duplicate invocations of the same contract;
- provider-local replays of shared helpers;
- tests whose only purpose is preserving test-only exports, globals, or wrappers;
- dead production code whose only callers are tests;
- expected values produced by the helper or renderer under test;
- mocks that implement the asserted behavior, or one identical mock standing in
  for different APIs;
- fixtures that supply the receipt, admission, or callback ordering the owner
  should produce, or persistence asserted against a store the path never writes;
- capability tests that restate declared flags instead of exercising the
  delivery or acknowledgement the flag promises;
- negative controls that pass for an unrelated reason, such as a denial from a
  different guard or a rejection the production path never reaches;
- names or fixtures that promise more than the input exercises, such as a
  "retires the window" test asserting the window was not cleared.

## Value bar

Tests justify their maintenance cost by protecting behavior, a credible
regression, or an independently meaningful contract. In an audit, an existing
test that must change for behavior-preserving source reorganization is suspect,
not automatically deletable. New tests use the same independent-contract bar;
reject implementation coupling, not a meaningful public-contract assertion.

Read applicable project rules, the complete candidate test and its production
owner. Follow callers, sibling coverage, CI and history as needed to establish
the real contract and remaining proof; a small test edit does not require a
whole-system inventory. Check dependency source or types when they decide the
behavior being asserted.

## Discovery

Keep discovery read-only until the candidate is understood; a brief finding is
enough and does not create another approval gate for authorized edits. For broad scope,
group discovery along these boundaries; delegate only when the user or
applicable project instructions authorize it:

- core and packages (`src/`, `packages/`);
- plugins (`extensions/`);
- UI, apps, scripts, and tooling;
- a cross-cutting pattern sweep.

Outside campaign mode, prefer a few high-confidence candidates over a large
speculative inventory. Hunt for the [junk patterns](#junk-patterns).

## Retention bar

Keep a test when it independently enforces a public API, plugin SDK, protocol,
config, migration, storage, security, platform, default, prompt-byte, generated
cross-language, package, release, or architecture contract. Also keep:

- call ordering when order is observable behavior;
- regressions with a credible failure mode;
- source inspection when it is the cheapest independent guard: it fails when
  the contract changes (the user-facing key, byte, or path) and survives an
  identifier-only refactor;
- a retained test that fails on the baseline: treat it as a possible product
  bug, reproduce it, and repair the owner rather than deleting it.

Static or slow is not a deletion reason. A test that resembles implementation
may still be the independent contract; prove otherwise before removing it.

## Candidate evidence

Before deletion, establish the following applicable evidence; a short local
note is sufficient. Missing behavior or remaining-proof evidence blocks deletion:

- exact test name and location;
- what failure it can actually detect;
- non-test callers of the covered production or support seam;
- stronger remaining owner-boundary proof, or why no proof is needed;
- the reason the test or seam exists, using history where needed;
- production or test-support deletion unlocked;
- risk and the focused validation command.

## Edit shape

Choose one coherent owner-boundary batch. Delete obsolete test-only exports,
globals, wrappers, and dead production paths instead of preserving aliases.
Move retained regressions to their canonical owners. Consolidate repeated
package or dependency assertions into one generic contract.

Reduce unnecessary production seams while preserving behavior; line counts are
not a target. Do not replace deleted tests with implementation restatements or
delete uncertain candidates to increase cleanup counts.

## Validation

Do not edit the same source or tests while a verification run is using them.
Derive commands, runtimes, isolation and generated-file rules from the current
project's instructions, manifests and CI. Do not assume a test framework or
another repository's helper scripts. External services and devices follow
the task's existing authorization.

1. Run the smallest relevant owner and sibling tests using the project's
   actual test command. For a bug fix, show failure before and success after
   when reproducible; otherwise name the missing evidence without claiming
   the regression was reproduced.
2. For removed source greps or plan assertions, run the executable script or
   dry-run that owns the real contract.
3. Run the relevant static checks and `git diff --check`; do not format unrelated files.
4. Inspect the final diff for lost behavior coverage and newly orphaned
   production seams. Distinguish baseline failures from introduced failures.
5. Complete any review required by the project. Independent review is useful
   for broad deletions when authorized; no particular external skill is mandatory.

## Landing and continuation

Commit, push, open a PR, or land only under the applicable authorization and
project workflow. A test audit does not automatically start a publishing or
whole-repository cleanup campaign. If an authorized campaign continues,
refresh its actual base branch and changed files before the next batch.

## Handoff

默认运行目标案例与直接受影响的相关检查。扩大范围前说明要解决的具体风险；公共协议、基础设施或广泛共享逻辑变更可以合理扩大。适用的原缺陷、合法行为、关键边界和必需门禁已有充分证据就停止，不为数量或指标继续加测。清理只处理范围内已证明无效、完全重复或错误耦合的测试，先确认没有删除独立业务保护。

最终简洁报告以下事实，小任务可合并成几句话：

1. **结果**：已修复或验证的行为、尚未完成的部分。
2. **关键证据**：业务规则、实际入口、预期与实际结果，以及运行命令或可定位记录。
3. **修复前后**：原缺陷是否被捕获、修复后是否通过；无法核对就直说。
4. **验证边界**：真实依赖、替身、真实模型、Web、模拟器和真机分别验证到哪里；不适用项省略。
5. **停止依据**：为什么证据充分，或缺什么证据及最小下一步。

仅报告实际执行的检查，区分通过、失败、跳过、未执行和建议。清理任务另补删除类别、保留依据、生产简化与交付状态；单次验收不要求清理报告、行数对比或 PR 模板。
