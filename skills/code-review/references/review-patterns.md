# Conditional Review Patterns

Load only the sections whose trigger appears in the diff. These are hard stops when the described failure can reach users; otherwise report them as advisory.

## Recurring or hard-to-observe bugs

For a recurring visual, layout, timing, or stateful-UI bug, inspect the responsible decision and violated behavior rather than accepting another tuned constant. Verify the actual decision and event order at its owning boundary; extracting a pure function is useful only when it clarifies a real responsibility, not merely to make testing convenient.

Do not demand test-only seams, exports or an extra enforcement framework. For costly operations such as deletion or privilege changes, check that safeguards are reached by real callers. Source inspection is appropriate only when it independently protects a meaningful contract and survives harmless refactoring; apply the same evidence bar as `test-audit`.

## Captured output and asynchronous completion

When code branches on an error message or captured command output, probe what the string contains at runtime. A subprocess using inherited stdio may show diagnostics in the terminal while `error.message` contains only the command line. Prefer structured facts such as exit codes or known targets over reparsing prose.

Flag fixed `sleep`, `asyncAfter`, `setTimeout`, frame counts, or guessed timeouts that stand in for an observable completion signal. They vary across CPU speed, display refresh rate, and networks. Drive the next step from callbacks, navigation completion, frame changes, state flags, or wall-clock state as appropriate.

## 并发、队列与可靠提交

改动涉及后台工作、共享状态、重试、队列或事件提交时，检查实际所有者和产生副作用的路径，不凭使用了某个模式就判安全，也不因没用某个框架就判缺陷：

- 任务结束、失败和取消是否有人接收？越过请求生命周期后谁负责资源与结果，旧结果能否污染替换后的用户或会话？
- 乐观版本检查是否与写入原子结合？并发重试、同键不同请求、结果未知时，服务端幂等能否阻止重复业务效果？
- 并发、等待队列和重试是否都有界？满载策略是否使任务静默丢失或一直显示处理中？
- 数据提交与事件发送之间失败会不会丢事件，重投会不会重复副作用？Outbox 不免除消费去重，Saga 补偿失败不等于已回滚；检查最终恢复与用户状态。

按相关风险构造发生顺序和失败位置，再寻找已有保护证伪；性能结论须含排队及端到端结果。不要把这份清单变成所有 diff 都需要的架构改造。

## Simplification and deletion

For prose, rule, skill, or guidance consolidation, read the deletions back and classify every removed behavior as `folded into X`, `redundant with Y`, or `behavior removed`. List behavior-removed entries explicitly. Deletion volume is not evidence of a good pass.

For dead-code or YAGNI claims, search the whole repository: entrypoints, docs, tests, generated dispatch tables, scripts, CI, packaging allowlists, manifests, and dynamic lookup patterns. Separate test-only from production references and chase data written but only read indirectly. If a dev tool is merely exposed by the wrong package or mirror, tighten distribution rather than deleting the tool. Partial search scope cannot justify deletion.

## History-sensitive normalization

When a diff restores a recently removed symbol, string, asset, enum case, localization entry, or config field, confirm the current review target and actual integration branch still consume it. A parity test or stale rule is not proof of life.

Before making an outlier match its siblings, inspect the change or comment that introduced the divergence. The asymmetry may deliberately avoid a known defect; normalization must preserve that protection.

## Non-atomic replacement of user files

When a diff writes to a path the user already has (`curl -o`, `>`, `tee`, open-truncate-write), ask what survives a failure partway through. Truncating the destination first means a dropped connection, timeout, or non-zero exit leaves a corrupt file and no original. Require staging into a sibling temp file, swapped in only once the content is complete.

Staging covers the paths the code tests for. It does not cover signals: with no trap, an interrupt mid-write can both strand the temp file and let the shell run past the interrupt to install partial content. A fetch running with `-fsSL`, `2>/dev/null`, or a swallowed exit code compounds this by telling the user nothing about what broke or what was left intact.

## Destructive matcher breadth

For recursion, mass deletion, traversal, ID-prefix wildcards, or fallback regex branches feeding a destructive sink, inspect:

- matcher breadth in every primary and fallback branch;
- protected-path coverage at the new entry point;
- user-confirmation paths; and
- whether the guard lives inside the deletion primitive rather than only at one caller.

Ask for the narrowest evidence authorizing deletion. Exact identifiers and exact paths can pass. Display names, vendor prefixes, common tokens, and user labels cannot safely authorize neighboring deletion.

## Duplicated derivations

Check classification, ordering, thresholds and eligibility rules computed in multiple places for inconsistent ownership. Summary/list or preview/executor pairs may drift after a one-sided change. Share the rule when the business meaning and boundary are the same; do not merge distinct responsibilities solely because their code looks similar. When one side changes, inspect its actual sibling consumers.

## Test surface fidelity

A test is not coverage when it pins a helper that production never reaches or asserts the literal source form of a command/config string instead of the shipped entry point. Ask whether it fails on the unfixed code and whether users execute the asserted path. If either answer is no, the test is a finding. Then ask the two questions a red-green run cannot answer. What can the assertion not see: a matcher scoped to tagged instances reads an untagged one as exempt rather than as a blind spot, an input set built before the producer's own transformation never contains what production emits, and a parity check comparing two copies to each other is blind to what both are missing. What benign change turns it red: an anchor on exact wording, on a positional slice, or on one spelling of a rule usually written another way survives the removal it exists to catch and fails on a rewrite. Anchor on the fact, the identifier, or the enclosing structure.

## Never-shipped migrations

Check whether compatibility logic protects a real supported consumer or persisted state. A missing public release tag is not proof that a database migration was never executed or an internal client never used the schema. Follow project migration rules and execution evidence; never rewrite or delete executed migrations. Remove compatibility scaffolding only after proving its triggering state cannot exist within the supported contract.

## Unknown identifiers

Search every new function, type, variable, asset, command target, and config key that the diff assumes already exists. No result outside the new diff means the dependency is unproven. Dynamic registries require checking their generation or lookup path rather than trusting a name match.

## Dependency changes

Verify lockfile consistency in the project's declared environment. Check the full manifest, overrides, resolver configuration, and dependency diff, then run the project's frozen/locked verification. Regenerate in an isolated checkout only to investigate a concrete discrepancy, using the complete proposed inputs and declared toolchain. Equal bytes do not prove provenance; differences require explanation, not an assumption of hand-editing. Confirm that the resolved dependency graph implements the requested change.

Automated security PRs get two extra checks their scanner does not do. First, whole-file reserialization: bots that rewrite a manifest can silently escape non-ASCII (emoji, CJK) or reorder keys, so diff the manifest against base in full rather than only the version line. Second, reachability: confirm the package is actually built into the shipped artifact (`cargo tree -i <pkg> --target all`, or the equivalent import/feature check) before repeating the advisory's severity, since an inert lockfile entry is not a live vulnerability in this project.

When a version pin exists, find out why before moving anything near it: `git log -S'<pinned-name>' -- <manifest>` usually names the bug it was added for. A bump that satisfies the advisory but leaves a companion pin at its old version can be worse than not bumping at all.
