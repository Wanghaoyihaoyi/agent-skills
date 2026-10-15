---
name: test-audit
description: "Invoke whenever writing, changing, reviewing, or sweeping tests. Authoring gate for new tests plus audit workflow for low-value, implementation-coupled, or duplicative tests and the test-only production seams they demand."
---

# Test Audit

执行本 skill 时，在开始测试编写、检查或修改前，先发送一条以 `🧪` 开头的简短进度消息，例如：`🧪 开始检查测试的有效性。` 显式调用和自动选用、三种模式都适用；不要只在最终回复中显示。仅创建、编辑或解释本 skill，不代表执行测试审查。

Three modes, one value bar. Follow the current project's instructions and
authorization. A review-only request does not authorize edits. Keep changes
scoped to this task and preserve other work and index state.

Authoring mode gates every new or changed test at
write time. Audit mode runs focused sweeps of tests that re-assert source,
duplicate stronger proof, couple behavior to implementation, or keep test-only
production seams alive. Continue only within the authorized scope; optimize
for confidence, not deletion count. Campaign mode prunes one
whole subsystem's test surface (every test file a plugin or core area owns);
before starting one, read [CAMPAIGN.md](CAMPAIGN.md).

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

For reproducible bugs, observe the regression failing for the intended reason
on the pre-fix code in isolation and passing after repair. If the old failure
cannot be run, name the missing evidence; a passing test alone does not prove
the original bug was reproduced. Add cases for distinct risks, not duplicate
replays of the same contract at every layer.

## 按风险选择验证方法

只在现有验证有关键缺口时选用以下方法，不为术语齐全引入新框架。每种方法仍须通过上面的新增测试门槛；优先复用现有测试工具和真实边界。

| 场景 | 方法与证据边界 |
| --- | --- |
| 不熟悉的旧实现将被替换 | 表征测试记录真实输入、输出、错误和副作用；已知错误单独标记，不能把现状固化为正确业务规则。 |
| 新旧实现迁移或多套逻辑合并 | 差分测试使用相同输入、初始状态和受控事件序列。只归一化合同允许变化的字段；每个差异都须解释为预期修复或回归。新旧一致仍可能共同出错，补独立业务断言。 |
| 权限、数据规则或复杂状态转换 | 属性测试从独立业务规则提出始终成立的性质，例如未经授权不能跨用户写入、重复请求不重复产生副作用。覆盖合法与非法输入、事件顺序和边界；保留随机种子并缩减失败样例，不能由实现反推性质。 |
| 模块或服务接口发生变化 | 契约测试验证真实生产方和消费方的输入、输出、错误语义及适用版本。消费方的自制 mock 不能单独证明生产方兼容；合同有主责任方，其他层仅补独立风险。 |
| 怀疑测试能通过却发现不了错误 | 小范围变异测试：在隔离副本中故意改变关键判断或副作用，观察测试是否因目标行为失败。存活变异先区分等价变化、未执行路径与断言缺口；不追求统一变异分数。 |
| 可靠性依赖故障或时序保障 | 故障注入实际触发相关超时、断连、重复或迟到事件，再检查资源和业务副作用；正常路径通过不能证明故障保障有效。 |

以上方法的副作用都须隔离，不向生产或共享工作区注入错误，不为对照重复真实扣费、发送或写入。状态与异步行为要验证完成后的状态及副作用，不能只检查返回值。有限样本、差分一致或高变异分数都不等于完全正确；报告实际覆盖及未验证边界。

### 受控故障与恢复验证

混沌工程只用于有明确恢复假设的场景，不随机制造故障：指定注入位置、故障或事件顺序、影响范围、观察指标、停止条件和清理办法。先用隔离测试、重放或已有工具，覆盖相关断连重连、重复乱序、下游超时、队列饱和或部分提交，验证最终业务状态、资源回收及副作用次数，而非只看异常被捕获。

真实服务、共享资源和流量上的注入或压测须有适用授权；测试授权不自动包含这些操作。停止注入后确认环境恢复，保留能解释失败的种子和事件记录。未执行恢复检查就报告未验证，不由一次恢复宣称系统能承受所有故障。

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

Report the actual change or review outcome, protected behavior, evidence and
remaining limits. Include removed low-value categories, retained candidates,
production simplifications and delivery state when applicable; authoring one
test does not require a cleanup report, LOC comparison or PR template.
