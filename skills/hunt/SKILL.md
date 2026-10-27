---
name: hunt
description: "Finds root cause before any fix. Use when something errors, crashes, regresses, or used to work. 也用于关键路径、尾延迟、排队积压、跨服务卡点、CI 负载优化和偶发失败的证据诊断。不用于代码审查或新功能设计。"
---

# Hunt: Diagnose Before You Fix

> 来源：基于 [Tw93 / Waza 的 hunt 技能](https://github.com/tw93/Waza/tree/main/skills/hunt) 改编。保留 Tw93 的 [MIT 版权声明](LICENSE)。

Prefix your first line with 🥷 inline, not as its own paragraph.

A patch applied to a symptom creates a new bug somewhere else.

## Outcome Contract

- Outcome: the root cause is identified before any fix is applied.
- Done when: evidence explains the cause and affected symptoms, separate or unresolved symptoms are identified, and the repair or handoff has a meaningful verification check.
- Evidence: source trace, repro command or UI path, logs or state, targeted test/build output, and runtime evidence for UI or native defects.
- Output: root cause, fix or handoff, verification result, and any unswept sibling risks.
- Authorization: "diagnose", "investigate", "why", "look into", "排查", "看看", or equivalent is report-only. Apply a fix only when the current request explicitly asks to fix, change, implement, or optimize, or when an authorization to do so is still in force for this same unfinished task with the action, scope, and goal unchanged; root-cause proof is still required first. Commit, push, publish and destructive actions follow the current task and project authorization separately; honor existing authorization without asking again.

**Before changing product behavior, state the cause and supporting evidence:**
> "I believe the root cause is [X] because [evidence]."

Name a specific file, function, line, or condition. "A state management issue" is not testable. "Stale cache in `useUser` at `src/hooks/user.ts:42` because the dependency array is missing `userId`" is testable. If the cause is not specific enough to test, gather more evidence first. Minimal diagnostics may be added within authorization to discriminate hypotheses; they are not a behavioral fix.

## Diagnosis Signals

Account for each reported symptom with evidence, including evidence that it has a separate cause; do not force unrelated failures into one hypothesis. For intermittent or timing-dependent issues, use logs, controlled ordering, replay or reproduction to discriminate causes. Failure to reproduce once is not proof of absence, and deterministic reproduction is not the only possible evidence.

Rationalization smells: "I'll just try this" = no hypothesis, write it first. "I'm confident" = run the instrument that proves it. "Probably the same issue" = re-read the execution path from scratch. "It works on my machine" = enumerate env differences before dismissing. "One more restart" = inspect the last error and current state; do not repeat restarts without new evidence or a concrete test.

Memory and prior notes are hypothesis fuel only: current code, logs, and repro evidence override them, and they never replace a fresh root-cause sentence or symptom list.

## Bisect Mode

Activate when: "以前是好的", "之前是好的", "used to work", "上一次提交还是对的", "broke after update", or the user remembers a specific good commit or version.

- Protect the user's worktree first: `git status --short --branch -uall`. Any modified, staged, or untracked files mean no bisect in the current checkout: run it in a temporary detached worktree and remove that worktree when done. If a temporary worktree is impossible, continue read-only comparison or use an isolated copy; ask only if a necessary state-changing alternative lacks authorization.
- If the last-good version is only a few releases back, `git diff <last-good>..HEAD -- <suspect path>` and read the delta first. The regression is usually visible there at a fraction of a bisect's cost; fall through to bisect only when the diff is too large or the culprit is not obvious.
- Bisect only with a non-interactive pass/fail command defined up front, and keep the bookkeeping in git (`git bisect good/bad`), including when you test a suspect commit directly. When it names the culprit, read only that diff down to the specific line, then run `git bisect reset` before removing the temporary worktree.

## 最小化失败场景（Delta Debugging）

输入、配置或事件序列太复杂，难以判断原因时，先定义可复验的失败判据，再在隔离副本中逐步去掉输入片段、事件或条件；每一步都确认仍是同一种失败，而非语法错误、其他拒绝或未到达原路径。保留必要前置状态和能触发失败的样例，不修改共享工作区来试错。

间歇故障需固定可控时序、随机种子或记录重放，并说明重复运行的结果；无法可靠区分通过与失败时，先补观测，不从一次未复现推断某条件无用。缩减结果用于发现致因条件，不直接证明根因，也不要求证明全局最小；修复后仍回到原始完整场景验证。

## Repeated Regression / Screenshot Reference Mode

Activate when the user says the same issue is still wrong after a fix, provides a "good" screenshot/version/file, or describes a visual result as previously correct.

Treat the reference as evidence, not decoration: list every reported and visible symptom in the user's concrete words; identify the reference oracle (last-good commit, old build, fixture, screenshot, described expected state); define the pass/fail check before editing; then name the exact current-vs-reference delta. Do not generalize a visual defect into "style polish" when the evidence points to a broken render, race, font pipeline, or state path.

If the issue is purely subjective UI taste, route to `/ui`. If it is rendering, state, timing, build output, font generation, or a regression from a known-good version, stay in `/hunt`.

## Scope Blast Mode

Activate after fixing a root-cause pattern, before declaring the bug done; also when the user says "举一反三", "举一反三深入看看", or "其他地方有没有同样问题". The same shape often hides in N other places; one local fix that ignores the blast leaves N - 1 bugs in the tree.

Extract the pattern signature (the specific function, regex, API call, CSS selector, lock acquisition, validation skip, or input boundary that produced the bug) and search the affected call chains and sibling modules with available repository search tools, preferring `rg` and excluding generated dirs, build output, and vendored deps; for class-of-bug patterns ("any handler missing the lock"), grep the surrounding shape, not just the literal text. Classify relevant matches as same bug, safe with a reason, or unresolved evidence. Investigate factual unknowns yourself and ask only for a necessary decision or resource. Summarize the sibling scope and gaps before claiming the affected class is fixed; no per-match report template is required. Unrelated bugs the sweep surfaces get listed, not fixed in this PR, unless the user agrees.

## Confirm or Discard

Run the one probe that would fail if the hypothesis were wrong, then read it. If the evidence contradicts the hypothesis, discard it completely and re-orient on what the probe just showed. Do not stack a fix onto a disproven hypothesis, and do not keep one just because the code "looks like" the cause.

## Runtime Evidence Ladder

修复验收沿用 [test-audit](../test-audit/SKILL.md) 的独立业务预期、验证边界与停止条件；复用已有检查，不因排查自动新增测试或清理整个测试面。优先通过真实入口捕获目标业务失败，修复后用同一案例与直接受影响的合法行为核对；无法核对旧实现时明确写“未验证修复前失败”。涉及异步结果、模型选择、语音或设备时，再读 [专项行为验收](../test-audit/references/behavior-acceptance.md) 的对应部分，区分受理、完成、存储、展示与实际播放。

Use this ladder before claiming a bug is fixed:

1. Source trace: name the exact function, state transition, file, line, or condition that can produce the symptom.
2. Deterministic repro: run or write the smallest command, fixture, UI path, or scenario that produces it.
3. Running version: before reading a deployed service's or device's behavior, read the version identity from the running target itself (container image digest and start time, served build id, installed app version or commit) and match it to the code under test. A deploy reported as done can still be running old code after a silent failure; until identity matches, every later rung measures the old build.
4. Logs/state/cache: inspect the runtime state that proves the path was reached, including queues, DB rows, caches, temp files, generated outputs, device logs, or external tool logs. Capture them before a redeploy, reinstall, or restart replaces them.
5. Build/test: run the narrow test or build that exercises the fix.
6. Real runtime check: for UI, native app, browser, rendering, or visual bugs, open the app/page/artifact and verify the visible result with a screenshot or concrete checklist.

Compile-only is not enough for UI, native-app, visual, rendering, or generated-artifact bugs. If the runtime check is impossible in the environment, say why and hand off the exact screen, command, or artifact to verify.

When the reporter's environment is the missing rung and it cannot be reproduced locally, the next artifact is a read-only probe they can paste and run, not another hypothesis. Have it print the environment, the disputed measurement, and the state of whatever the hypothesis turns on, and nothing that could carry a secret or a private path. Assume none of your own layout: their install method, directory conventions, locale, shell, and version all differ, so discover rather than hardcode. Ship it as plain copyable text with one command to run and one block to paste back.

For recurring classes of failures, load `references/failure-patterns.md` before adding a second fix.

## Native App Freeze Mode

For beachballs, not responding, tab-switch freezes, first-open lag, idle wake stalls, overlay lockups, or frozen-app screenshots, load `references/logging-techniques.md` (Native App Freeze Mode) before changing code.

## 性能与跨服务诊断

遇到慢、延迟波动、排队积压、调用成本过高，或无法确定多服务链路卡点时，读取 [关键路径与可观测性](references/performance-diagnosis.md)。先测真实用户结果，再定位；不把先回复“处理中”当任务更快完成，也不凭单段耗时归咎模型。

## 跨端会话与时序

故障跨客户端、网关、后端或外部服务，表现为事件先后错乱、断线重连后状态丢失、取消后迟到结果生效，或接口成功但用户体验不对时，先在这里定位：拿到事件先后、请求或会话标识和状态归属的证据，写出根因句。常见形态见 [故障模式](references/failure-patterns.md) 中的会话重连、先占后查和迟到结果条目。

项目提供跨端行为技能（如 `cross-layer-behavior`）时，根因明确后，由它确定目标行为、必须阻止的副作用以及跨层修复和验收；沿用这里已有的证据和根因，不重新调查一遍。只涉及单层的小问题直接在这里修复。

## CI 负载与偶发失败

用户要求减少 CI 时间或成本、排查不稳定测试时，读取 [CI 历史、收益与稳定性](references/ci-maintenance.md)。按历史运行记录量化收益，区分机器运行时间和合并等待时间；偶发失败先按证据分类，再修复明确原因。建议或审计请求保持只读，修复与交付沿用当前授权。

## Targeted Logging

Each log must answer a yes/no question about a hypothesis; see `references/logging-techniques.md` for what to log and how to trace runner-only failures. Remove temporary logs before finishing; gate persistent diagnostics behind the project's debug flag.

## Rendering Bug Mode

For PDF output, page breaks, font rendering, or print layout defects, load `references/rendering-debug.md`; it carries the activation triggers and the diagnosis checklist (WeasyPrint quirks, font loading, page overflow, browser print CSS).

## IME / Unicode Issues

For input method, character rendering, or text encoding bugs (IME state, cursor drift, emoji splitting, composition events), check `references/ime-unicode.md` first before forming a hypothesis.

## Hard Rules

- **Same symptom after a fix is a hard stop; so is "let me just try this."** Both mean the hypothesis is unfinished. Re-read the execution path from scratch before touching code again.
- **Stop repeating attempts without new evidence.** Reassess disproven hypotheses and choose a discriminating probe. Continue authorized investigation when new evidence gives a concrete next step; hand off only when a missing resource, decision, permission or agreed budget blocks it. State what was checked, ruled out and still unknown rather than requiring approval after an arbitrary attempt count.
- **External tool failure: inspect before retrying.** Check the error and actual terminal state; use an equivalent authorized alternative when it can obtain the needed evidence safely. Do not blindly retry, duplicate side effects or reset credentials.
- **System/tooling symptoms need a lower-layer baseline.** Before blaming the visible app, generated file, or top-level feature, measure the raw lower layer first: OS capture versus post-processing, runtime service versus UI, compiler/toolchain versus test assertion, network/API versus client handling. Retire hypotheses that the baseline disproves instead of circling them.
- **Visual/rendering bugs: static analysis first.** Trace paint layers, stacking contexts, and layer order in DevTools before adding console.log or visual debug overlays. Logs cannot capture what the compositor does. Only add instrumentation after static analysis fails.
- **Behavioral / lifecycle / async bugs need ordering evidence.** Reuse logs, traces, tests or a controlled reproduction. Add minimal diagnostics only when they are missing; static code can prove some pure-logic or ownership failures, but cannot prove unobserved runtime order. Do not add logs mechanically or fix from guesses.
- **Repeated numeric tuning needs a structural check.** Inspect constraints, units and ownership before changing another constant. Share a token only when values represent the same rule; do not force legitimate asymmetry into one value or infer a cause from an attempt count.
- **Performance complaints need numbers.** For "slow", "laggy", or memory-growth reports outside Native App Freeze Mode, measure the baseline first (wall-clock time, profile sample, memory footprint), fix, then re-measure and report before/after numbers. "Feels faster" is not evidence.
- **Fix the cause within the authorized scope.** Continue necessary fixes, including a prerequisite refactor such as a shared interface change once you state why it is needed; ask only when the fix expands that scope or needs an unresolved behavior tradeoff, and file count alone is not an approval boundary. Keep unrelated refactors separate, and route an explicitly requested feature to its own workflow under the same completion ledger after diagnosis; a bug-fix authorization alone does not authorize an unrequested feature.

## Gotchas

| What happened | Rule |
|---------------|------|
| Patched the wrong copy of a duplicated surface | Trace the execution path backward to the instance that actually renders before touching any file |
| Orchestrator reported RUNNING while a downstream stage was misconfigured | In multi-stage pipelines, test each stage in isolation |
| Race condition diagnosed as a stale-state bug | For timing-sensitive issues, inspect event timestamps and ordering before state |
| Reproduced locally but failed in CI | Align the environment first (runtime version, env vars, timezone), then chase the code |
| Worked when launched from app, broke when opened via file association / drag-drop / deep link / external proxy | Reproduce using the exact entry point the user described. App-internal init differs from cold-launch-with-file init; state may not be ready when the document arrives. |
| Fix matched the reporter's setup but changed nothing for everyone else, or regressed the default | A defect report is evidence, not the full scope. State whether the fix changes the default experience for all users or only the reporter's configuration, and prefer fixing the default path. |
| Broke after toggling theme / mode / locale, fine after restart | State not re-applied on the toggle path. Trace the toggle's recompute or invalidation route first; do not tune styles pixel by pixel while the state path is broken. |
| Changed the algorithm but the output stayed wrong | The reader may be hitting persisted output written by the old code (scan results, analysis cache, snapshot with a TTL). Changing generated-then-persisted data requires invalidating or version-bumping the old cache in the same change; before re-diagnosing, confirm the runtime is not reading stale data. |
| Fixed the one cause that reproduced, shipped, and the same gate blocked the next user for a different reason | A guard that refuses has a set of causes, not one. Enumerate every branch that can refuse before shipping, and give each a distinguishable code, a one-line reason, and a next command. |
| The user's observation and the log disagreed, and the log won | Trust the observation and treat the gap as an un-instrumented path. A probe that passes on the happy path says nothing about the failing one; a probe that cannot reproduce is an invalid probe, not an absent defect. |
| Patched a capability-gated feature on a surface that never offered the capability | Confirm the run surface (simulator, device, sandbox, restricted entitlement) supports it before writing a fix. If it does not, say so and stop; no source change makes it appear. |

## Output

Lead with outcome and delivery state, then briefly explain the cause, actual repair, affected sibling scope, evidence and unverified limits. Use project-specific format only when required; a small diagnosis does not need a fixed report block.

For recurring bugs, retain a meaningful automated regression at the real boundary when feasible, following `test-audit`'s value and red-green rules. If automation cannot exercise the failure, explain why and retain a reproducible diagnostic or concrete device acceptance check; do not claim automated regression proof. Verify that negative assertions and the runner can actually detect the intended failure, using a discriminating control when needed, not a mandatory duplicate positive case for every assertion.
