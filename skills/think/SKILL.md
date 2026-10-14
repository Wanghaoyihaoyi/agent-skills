---
name: think
description: "Turns rough ideas into approved, decision-complete plans before coding. Use when planning architecture, judging whether to build, or writing a handoff. 也用于第一性原理推导、并发与 Agent 架构设计、产品实验和多目标取舍。不用于缺陷排查或小修改。"
---

# Think: Design and Validate Before You Build

> 来源：基于 [Tw93 / Waza 的 think 技能](https://github.com/tw93/Waza/tree/main/skills/think) 改编。保留 Tw93 的 [MIT 版权声明](LICENSE)。

Prefix your first line with 🥷 inline, not as its own paragraph.

Turn a rough idea into a decision-complete recommendation or plan. A planning-only request does not authorize implementation. Small sketches or read-only experiments may clarify a mechanism; continue already authorized implementation under Implementation Handoff without another approval round.

Give opinions directly. Take a position and state what evidence would change it. Avoid "That's interesting," "There are many ways to think about this," "You might want to consider."

## Outcome Contract

- Outcome: a rough idea becomes a decision-complete recommendation or implementation plan.
- Done when: the goal, success criteria, constraints, chosen approach, rejected tradeoffs, tests, and handoff steps are concrete enough to execute without re-deciding.
- Evidence: current repo state, project docs, live external docs when relevant, prior decisions, constraints, and explicit user preferences.
- Output: one recommended direction or a handoff plan with assumptions and verification steps.

## Durable Context Preflight

See [references/durable-context.md](references/durable-context.md) for when durable context is in scope and the redaction gate that applies before any of it becomes a durable rule.

For `/think`: current repo state and live docs override memory. Lock durable decisions and preferences before asking questions, and do not ask the user to restate an intent that the durable context already establishes unless it is risky, stale, or contradicted by current state.

Before outputting any plan, read the project guide index (`AGENTS.md` or `CLAUDE.md`) and only the domain rule that matches the problem. Do not load the entire `.claude/rules/` tree. If the user pointed at a local agent-memory summary, read that too. If the proposed plan contradicts a "hard rule", "never X", "must Y", or "prefer Z" in those files, surface the contradiction in the plan output (one sentence: which rule, which step contradicts it, recommended resolution). Do not silently override the rule. If the rule blocks the plan, stop and ask before continuing.

## Lightweight Mode

Activate when the user asks for a plan for a defined problem and the only open question is "how to fix it." An explicit repair request follows `/hunt`; file count alone does not create another planning approval.

Give one recommended approach: what changes, where when known, why, and the meaningful risk. Prefer the smallest approach that meets the goal. Detail and approval depend on unresolved decisions and existing authorization, not a fixed file count. Use a fuller plan only when interacting constraints or meaningful alternatives require it.

## Evaluation Mode

For value, viability, commercialization, or keep/remove judgments about a single target, load `references/mode-evaluation.md`.

## Triage Mode

For a bundle of independently accepted or rejected asks or screenshots, including "are these worth doing", load `references/mode-triage.md`; use its per-item table rather than Evaluation Mode's single verdict.

## 按问题选择工程视角

用户要求第一性原理推导，或方案涉及职责拆分、异步与实时链路、跨服务一致性、Agent 编排时，按需读取 [系统与 Agent 设计](references/system-design.md) 的相关章节。判断功能收益、比较多目标方案或设计 A/B 实验时，读取 [产品实验与取舍](references/product-experiments.md)。不是术语检查表，不因触及一个概念就运行全部方法或预建框架。

先给当前证据，再说明结论、取舍和什么新证据会改变判断。分析、方案和实验设计本身不授权代码修改、真实流量实验或外部操作；已获授权的同任务实施继续按下文交接规则完成。

## Before Reading Any Code

- If the project tracks prior decisions (ADRs, design docs, issue threads), skim the ones matching the problem before proposing.
- If the plan involves a default value, env var, or config field, open the project's actual config file (e.g. `app.config.json`, `tauri.conf.json`, `package.json`, `.env`) and lift the live value. Never quote a default from memory or docs.

## Check for Official Solutions First

Before proposing custom implementations, check framework built-ins, official patterns, and ecosystem standards against live docs (use the environment's doc-lookup tools when available). An existing official solution is the default recommendation unless you can articulate why it falls short for this specific case.

For an unfamiliar or repeatedly failing mechanism, inspect relevant mature implementations when this can resolve a concrete uncertainty. Explain what transfers and what does not; do not require a competitor survey or source-count quota for every difficult task.

## Propose Approaches

Give one recommended approach with rationale. Include effort, risk, and what existing code it builds on. Mention one alternative only if the tradeoff is genuinely close (>40% chance the user would prefer it). Always include one minimal option.

Anything that asks a person to install or configure something (hook, MCP server, editor plugin, config key, pricing tier, per-day limit) is a setup cost paid by every user. Default to the zero-setup form: a built-in command plus a skill, a fixed sensible default, a doc line. Offer the setup-requiring form only after naming why the zero-setup one cannot do the job.

A plan to distill one project's lessons into reusable skills or shared rules splits into **promote** (reusable workflow constraints only) and **do not promote** (project-specific commands, paths, release checklists, safety boundaries, private local context), unless the user asks to update that project itself.

For the recommendation, identify the most fragile assumption (premise collapse) and state it explicitly: "This plan assumes X. If X does not hold, Y happens." If the assumption is load-bearing and fragile, deform the design to survive its failure.

**Blocking ambiguities**: if requirements have a conflict the user must resolve (two contradicting sources, two valid interpretations with different cost), name the specific conflict in one sentence and ask which takes precedence. Do not silently pick.

**Additional attack angles** (run only when the plan involves external dependencies, high concurrency, or data migration):

| Attack angle | Question |
|---|---|
| Dependency failure | If an external API, service, or tool goes down, can the plan degrade gracefully? |
| Scale explosion | At 10x data volume or user load, which step breaks first? |
| Rollback cost | If the direction is wrong after launch, what state can we return to and how hard is it? |

If an attack holds, deform the design to survive it. If it shatters the approach entirely, discard it and tell the user why. Do not present a plan that failed an attack without disclosing the failure.

Get approval before proceeding.

## Validate Before Handing Off

- Make the affected responsibilities, interfaces and acceptance behavior concrete. Use a diagram when their relationships are difficult to follow.
- Cover meaningful success, failure and boundary scenarios; derive verification commands from the actual project.
- Identify new dependencies, setup cost and any irreversible data or external effects. State the needed authorization and rollback or recovery constraints.
- Check local capabilities and authoritative API contracts. Use a live read-only probe only when it answers a relevant uncertainty and fits current authorization; do not require every external service or credential before a design discussion can finish.
- A missing fact that changes the design must be resolved before calling the design ready. A later execution prerequisite can remain explicit with its owner and verification point; do not claim it was tested.

## Simplicity Gate

Skip for one-file bug fixes or when the user explicitly chose the minimal option.

When the plan adds files, abstractions, error layers, config knobs, or retries the user did not ask for:

- **Minimal path:** the brute-force version in one line; the chosen plan must beat it on risk, rollback, or latency, not elegance.
- **Defensive layers:** every try/catch, retry, fallback, or flag maps to one named failure mode; delete layers that only "might" fail.
- **Surface delta:** list new commands, env vars, flags, or services; prefer +0 unless a user split needs a knob.
- **Compensating complexity:** if the plan is mostly workaround machinery around a misbehaving API, stop and name a route change: when the workaround is larger than the feature it supports, the premise is wrong.

If the gate fails, shrink the plan or switch to the minimal option before asking for approval.

## Implementation Handoff

A finished plan must be executable by another engineer or agent without re-deciding the direction. Include:

- Scope and non-scope.
- The chosen approach and the one rejected alternative, if the tradeoff was close.
- Public API, schema, command, config, or file-interface changes, if any.
- Verification commands and manual acceptance checks.
- Release, publish, migration, or issue/PR follow-through steps, if the task naturally continues there.
- Rollback or failure handling for any step that can leave external state changed.

When the user asks to export a handoff, or when the environment prevents further execution, make the handoff execution-ready instead of explaining the limitation. Include file targets, key constants or selectors, exact commands, runtime or visual checklist, and risk boundaries. If the work depends on a screenshot or artifact, name the artifact and the pass/fail delta.

When the user says "Implement the plan", "just do it", "可以干", "直接改", "直接做", "按你说的来", "不用确认", "整", or otherwise explicitly authorizes implementation, execute the authorized direction without another approval round. With implementation authorization still in force for the same task, skip this skill's planning approval gates (including Lightweight Mode's wait) when the user or project rules already settle the choice. State which plan is being executed and check for repo drift; stop if specific drift makes it unsafe or a material choice remains unresolved. A settled design alone does not authorize implementation or public actions.

## Hard Rules

- **No placeholders in approved plans.** Every step must be concrete before approval. Forbidden patterns: TBD, TODO, "implement later," "similar to step N," "details to be determined." A plan with placeholders is a promise to plan later.
- **Phase independence.** Each phase must be independently mergeable: after Phase N ships, the system is usable even if N+1 never lands, because a plan that needs every phase before anything works lets one stuck phase block the release. If the work cannot be cut that way, ship it as one phase instead of pretending it is staged. A "Phase 0: investigate / spike" is the same red flag: investigation belongs before the plan, not inside it.
- **An error or bug report routes out before anything else.** "判断一下" plus error or bug context is debugging, not a value judgment: say it belongs to `/hunt` in one line, then route. Evaluation Mode is for value and existence judgments only.

## Gotchas

| What happened | Rule |
|---------------|------|
| Rejected design restarted from scratch | Ask what specifically failed, re-enter with narrowed constraints |
| Picked a regional or locale-specific API variant without checking | List all regional or locale differences before writing integration code |
| Introduced a second language or runtime into a single-stack project | Never add a new language or runtime without explicit approval |

## Output

**Approved design summary:**
- **Building**: what this is (1 paragraph)
- **Not building**: explicit out-of-scope list
- **Approach**: chosen option with rationale
- **Key decisions**: 3-5 with reasoning
- **Unknowns**: only items that are explicitly deferred with a stated reason and a clear owner. Not vague gaps. If an unknown blocks a decision, loop back before approval.

If the user only approves the design, end with the plan. If implementation is requested, follow Implementation Handoff instead of asking them to repeat the request.
