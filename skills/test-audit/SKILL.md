---
name: test-audit
description: "Invoke whenever writing, changing, reviewing, or sweeping tests. Authoring gate for new tests plus audit workflow for low-value, implementation-coupled, or duplicative tests and the test-only production seams they demand."
---

# Test Audit

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

Then check the test against every [junk pattern](#junk-patterns); a match fails
the gate unless the [retention bar](#retention-bar) names the contract it
independently guards. A test that would break under behavior-preserving
refactoring is asserting implementation, not behavior; rewrite it at the
owning boundary before landing it.

Bug regression tests must fail on the pre-fix code for the intended reason and
pass after the owner-boundary repair. A regression test that never demonstrably
failed proves the mock, not the fix. One regression at the owner boundary
covers the bug; do not replay the same scenario at every layer it crosses.

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
not automatically deletable; the authoring gate still rejects new ones.

Before judging a candidate, read the complete test and production owner, its
entry point, callers, callees, sibling implementations, overlapping tests, CI
routing, and relevant history. Read root and scoped `AGENTS.md` files first.
When the test claims dependency-backed behavior, inspect the dependency source
or types directly.

## Discovery

Keep discovery read-only and report evidence before editing. For broad scope,
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

Record every field below before editing. A missing field means the candidate is
not ready for deletion:

- exact test name and location;
- what failure it can actually detect;
- non-test callers of the covered production or support seam;
- stronger remaining owner-boundary proof, or why no proof is needed;
- relevant history and the reason the test or seam exists;
- production or test-support deletion unlocked;
- risk and the focused validation command.

## Edit shape

Choose one coherent owner-boundary batch. Delete obsolete test-only exports,
globals, wrappers, and dead production paths instead of preserving aliases.
Move retained regressions to their canonical owners. Consolidate repeated
package or dependency assertions into one generic contract.

Prefer net-negative production LOC. Do not add replacement tests that restate
the same implementation, and do not convert uncertain candidates into cleanup
to increase deletion counts.

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

Report:

- root cause and removed low-value categories;
- production owner simplifications;
- retained false positives and why they remain valuable;
- focused and full proof actually run;
- production versus test LOC;
- PR and merge state;
- named follow-ups.
