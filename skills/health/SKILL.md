---
name: health
description: "Audits agent config, instruction drift, hooks or MCP, and AI maintainability. Use when Claude, Codex, or Pi setup looks wrong. Not for application bugs or PR review."
---

# Health: Agent-Assisted Engineering Health

> 来源：基于 [Tw93 / Waza 的 health 技能](https://github.com/tw93/Waza/tree/main/skills/health) 改编。保留 Tw93 的 [MIT 版权声明](LICENSE)。

Prefix your first line with 🥷 inline, not as its own paragraph.

Audit the current project's agent setup and AI coding maintainability against this framework:
`agent config → instruction surfaces → tools/runtime → verifiers → maintainability`

Find violations. Identify the misaligned layer. Calibrate to evidence and risk, not repository size.

## Outcome Contract

- Outcome: a budget-aware health report that separates agent configuration risk from AI maintainability risk.
- Done when: each finding names the misaligned layer, the concrete evidence, and a copy-pasteable action or diagnostic command.
- Evidence: collected health script output, tracked project instructions, runtime config summaries, verifier logs, hooks/MCP surfaces, and read-only live probes when needed.
- Output: prioritized findings with status, impact, and next action, or a clear clean bill with residual risk.

Two lanes share one report:

- **Agent config health**: Codex/Claude/Pi instruction drift, permissions, hooks, MCP, skills, and memory supply chain.
- **AI maintainability health**: non-obvious constraint reachability, risk-backed hotspot ownership, verifier coverage, generated-artifact checks, and stale or misleading durable docs.

**Output language:** Check in order: (1) project agent instructions (`AGENTS.md` before runtime-specific files); (2) global agent instructions; (3) user's recent language; (4) English.

**Budget posture:** Start with the summary audit. Escalate automatically when the user asks for a deep, full, complete, thorough, "深入", "完整", "彻底", or "继续跑完" audit, when the user explicitly mentions AI coding code rot, Codex/Claude config drift, unclear context, missing verification, verifier output that points at stale paths, or "代码变烂", when current project instructions or remembered user preference says to run deep health checks by default, or when the summary pass exposes a critical ambiguity that cannot be resolved locally. Inventory counts never trigger escalation on their own. Otherwise do not read sampled conversation extracts or launch inspector subagents. Tell the user before escalating because deep health audits can consume significant token quota.

**Conversation scope:** When the request names only static material (`AGENTS.md`, skills, rules, settings, "只审查指令和配置"), pass `instructions` as the first argument to `collect-data.sh` and the run skips session history, reporting it as out of scope rather than as a coverage gap. This is chosen from the request, not a switch the user has to know about. Otherwise: Summary scans up to three recent previous sessions for the current project across Claude and Codex from a bounded candidate window when those local histories exist. Deep streams every previous current-project session across both runtimes for signals while printing only bounded extracts and a coverage receipt. Other projects remain out of scope by default. Only when the user explicitly asks for all conversations or cross-project capability distillation, run `python3 <skill-base-dir>/scripts/conversation_audit.py <claude-projects-root> deep --all-projects --codex-root <codex-sessions-root>` (the first argument holds every per-project log folder; the parser rejects other flag combinations), or hand off to a cross-project retro if one is installed. Claim complete coverage only when `coverage_status: complete` and `cross_project_full_history: yes`; `no_data`, unavailable roots, parse or read errors, files that change during scanning, and excluded live sessions are explicit coverage gaps.

## Durable Context Preflight

See [references/durable-context.md](references/durable-context.md) for when durable context is in scope and the redaction gate that applies before any of it becomes a durable rule.

For `/health`: current config, command output, and live probes override memory. Also flag durable memory problems when they affect behavior: oversized injected summaries, stale or contradictory entries, missing project entrypoint references, or private paths copied into public instructions. Keep these as context findings, not code-review findings.

## Hard Rules

- Summary and deep audits are report-only. Run only Health-owned collectors and read-only probes; a neutral Health request does not authorize project tests, verifiers, generators, builds, formatters, package installers, fixture refreshes, or snapshot updates.
- **A bundled debugging or code-review ask uses its own workflow.** Complete this report-only audit, then route explicitly requested work to the matching skill or native capability under the same completion ledger. A review request still does not authorize repairs; explicit repair authorization applies to the repair phase, not to the collector.
- A documented command alone does not authorize every possible use of it. Read-only probes may run when they fit the current request and effective authorization. For verification that writes files, accesses restricted resources or changes external state, honor the current task and valid standing permissions; request only missing authorization after preparing the concrete scope and expected effects.

## Step 0: Establish the evidence basis

Record four evidence classes:

| Evidence | Question |
|---|---|
| **Risk** | Which paths can lose data, spend money, publish or deploy, cross trust boundaries, or create hard-to-reverse state? |
| **Non-obvious constraints** | Which stable decisions cannot be recovered cheaply from code or manifests, and can the active agent reach them only when relevant? |
| **Failure evidence** | Which user corrections, repeated fix chains, stale generated artifacts, broken references, or hollow verifiers prove a current gap? |
| **Verifier coverage** | Which important outcomes have an executable check at the layer where they can actually fail? |

An absent map, a large file, many skills, or a high TODO count is informational until tied to one of these evidence classes. Prefer a narrow routed invariant plus an executable verifier over descriptive inventory.

## Step 1: Collect data

Run the collection script in summary mode for the requested scope. `<skill-base-dir>` is the directory containing this installed Health `SKILL.md`. Resolve only its adjacent `scripts/`; do not guess a former dispatcher's layout. If a helper or runtime is unavailable, inspect the relevant static evidence with available tools and report the missing coverage instead of prescribing a different skill bundle.

On Windows with the required PowerShell and Git Bash runtime, use the included launcher. Its process-local execution policy must not change account or machine policy:

```powershell
$HEALTH_LAUNCHER = "<skill-base-dir>/scripts/run-health.ps1"
$POWERSHELL = Join-Path ([Environment]::SystemDirectory) "WindowsPowerShell\v1.0\powershell.exe"
& "$POWERSHELL" -NoLogo -NoProfile -ExecutionPolicy Bypass -File "$HEALTH_LAUNCHER" collect instructions summary
```

On Linux or macOS with Bash available:

```bash
HEALTH_SCRIPT="<skill-base-dir>/scripts/collect-data.sh"
BASH_ENV= ENV= /bin/bash -p "$HEALTH_SCRIPT" instructions summary
```

These examples select static instructions. Use `auto summary` only when the request includes runtime/history diagnosis as described in Conversation scope; retain the selected scope if escalating to deep mode.

Sections may show `(unavailable)` when tools are missing:

- trusted `python3` missing: conversation, MCP/hooks/allowedTools, and skill-security sections unavailable
- A runtime-specific config file absent: check whether that runtime is in use and whether global config supplies it; absence of another runtime's file is not a defect

Treat `(unavailable)` as insufficient data, not a finding. Do not flag those areas.

The collector includes both runtime-specific and agent-agnostic surfaces:

- `AGENT CONFIG SUMMARY` / `AGENT CONFIG DETAIL` for Codex, Claude, Pi, and project instruction files; its sections start at `=== AGENT INSTRUCTION SURFACE ===`.
- `AI MAINTAINABILITY SUMMARY` / `AI MAINTAINABILITY DETAIL` for project signals, verification surface, generated mirrors, wrappers, and doc links; its sections start at `=== PROJECT SHAPE ===`.

## Step 1b: MCP Live Check

For a static instructions/config audit, skip live probes and report that scope. For a runtime connectivity question, probe only the relevant enabled integrations with a verified read-only, non-mutating operation that fits the user's authorization. Do not infer a safe ping from a tool name or contact every configured external service. Record actual success, failure or untested status. Disabled or unrelated servers are not failures. Check credential presence without printing values.

## Step 1c: Safety and security checks

These run after collection and before the Step 2 analysis. The first two apply to every audit; the third only to projects with long-running or autonomous agents.

### Security Baseline Checks

Run these on every audit. They are the floor, not the ceiling.

**Deny-list floor.** Apply this only when the runtime actually enforces the rule shape being recommended: agent permission settings, hook settings, MCP settings, allowed/denied tools, or a documented autonomous-agent launcher. In that case, the settings should deny, at minimum: credential and key directories (SSH, cloud providers, GPG, gh CLI), credential-bearing files (`credentials*`, `secrets*`), and pipe-to-shell installers. Treat `.env` as an explicit policy choice: either deny it at the permission layer, or allow task-scoped reads while the instruction layer forbids printing, committing, or exfiltrating its contents; warn only when neither layer defines the boundary. Report missing categories as one concise WARN; let the reviewer fill in exact local paths. Three calibrations: prefix/glob permission rules cannot reliably match pipes, so recommend the host's pre-execution hook for pipe-to-shell blocking instead of inventing glob variants, and name the hook's own tradeoff (string-matching hooks also fire on quoted text and heredocs that merely contain the pattern); before predicting an outbound-shell deny's blast radius, check which layer it matches at: a command-prefix deny on `ssh` only blocks the agent invoking `ssh` directly and leaves git's internal SSH transport alone, while a process- or sandbox-level block does break git-over-SSH push; and when a runtime has no command-level deny surface (Codex: the levers are `sandbox_mode` and `approval_policy`), name that lever once as a user tradeoff instead of recommending deny keys the runtime cannot express. If no agent settings surface exists at all, report the deny-list as not applicable rather than a failure.

**Permission-layer vs instruction-layer gating.** An allowlist entry for a git write action (`git push`) next to an instruction-layer rule ("push only when the user says so") is not automatically a contradiction: instructions decide when the action happens, permissions decide whether it re-prompts, and a user who explicitly authorizes pushes every session may keep push in allow deliberately to avoid double confirmation. Calibrate by reversibility and the user's own rules: actions the instructions forbid outright (`git reset --hard`, `git stash`, force-push) belong in deny or ask; routine explicitly-authorized actions stay where the user put them, reported at most as a note. Escalate only when auto mode plus skipped prompts plus broad allow lets a write action run with zero user input in a session, and even then present the friction tradeoff for the user to choose instead of silently moving entries.

**Environment override surface.** Treat the following as attack surface, report when set in tracked files or shipped settings without a justification comment: API base-URL overrides (redirect all traffic to a third party), auto-trust flags for project-local MCP servers, wildcard tool allowlists (`allowedTools: ["*"]`), and permission-skip flags (`--dangerously-skip-permissions` or equivalents). Print file:line and the key name only; never print secrets.

### Memory and Skill Supply Chain

Treat agent memory and third-party skills as supply-chain artifacts. They run with the user's privileges.

**Memory hygiene.** Audit the project's long-term agent memory store for secrets, tokens, or credentials (Critical), and for entries written by untrusted runs (subagent invoked on attacker-controlled input, /loop iteration over external content); recommend rotation after such runs. For high-risk one-off runs (untrusted PDFs, uncontrolled scraping, third-party scripts), recommend disabling memory persistence for that session entirely.

**Skill supply chain.** Third-party skills, plugins, and MCP servers run with the user's privileges. For each one not authored in this repo, check: source pinned to a release tag or revision (not `main`, a branch, or a remote git marketplace left tracking its latest head), hook handlers do not write to credential directories, MCP servers have explicit user consent (not auto-trusted by wildcard). Report unpinned sources or unreviewed hook handlers as Structural, not Critical, unless an active exploit signal is present.

### Long-Running Agent Stop Conditions

For projects that use `/loop`, autonomous agents, or any long-running agent flow, load `references/long-running-agents.md` and audit the four hard stop signals it lists. Projects without such a flow skip this check.

## Step 2: Analyze

Analyze locally from the summary output by default. When Budget posture escalates, re-run collection with the same scope argument (`instructions` or `auto`) and mode `deep`, using the applicable launcher from Step 1. Analyze the relevant inspector checklists locally, or delegate independent substantial scopes when available and permitted. Do not require parallel agents or a particular agent API. Redact credentials to `[REDACTED]`.

- **Deep inspector routing:**
  - **Agent 1** (Context + Security): Read `agents/inspector-context.md`. Feed `CONVERSATION SIGNALS` section.
  - **Agent 2** (Control + Behavior): Read `agents/inspector-control.md`. Feed the relevant runtime, hook, MCP, and permission evidence.
  - **Agent 3** (AI Maintainability): Read `agents/inspector-maintainability.md`. Feed only `PROJECT SIGNALS`, `AI MAINTAINABILITY SUMMARY` or `AI MAINTAINABILITY DETAIL`, and concrete verifier/drift receipts. Launch this agent only for deep health audits or explicit code-rot/AI-maintainability requests.
- **Fallback:** If a subagent fails, analyze that layer locally and note "(analyzed locally)".

Before reporting a deep audit as complete, wait for every launched inspector and reconcile its assigned scope. If one remains pending or fails without a local replacement pass, list that scope as unreviewed instead of issuing a whole-scope clean bill.

## Gotchas

| What happened | Rule |
|---|---|
| Missed the local override | Identify the active runtime's supported config locations and precedence; inspect relevant local overrides, not only tracked files |
| Subagent timeout reported as MCP failure | MCP failures come from the live probe, not data collection |
| Flagged intentionally noisy hook as broken | Ask before calling a hook "broken" |
| Hook seemed not to fire, but it did -- a later UI element rendered above it | Hook firing order is not visual order. Before re-editing the hook config: (a) confirm with `--debug` or by piping output, (b) check whether a diff dialog, permission prompt, or other UI element rendered on top and pushed the hook output offscreen, (c) only then suspect the hook itself. |
| Treated missing specs/docs as a failure | Decision artifacts are optional by default. Escalate missing docs/specs only when active handoff risk, failure evidence, or the user request makes them necessary. |

## Output

**Health Report: {project} ({summary|deep}, evidence-based)**

**Global findings report once.** Findings in machine-global config (`~/.claude`, `~/.codex`, global rules, skills, memory) are not project findings: label them `global`, report each once with its fix, and recommend one dedicated session for global cleanup instead of re-fixing per project. Before editing any global file, re-read its current state: when health runs across several projects in one day, another session may already have fixed or be mid-fix on the same file, and re-applying a variant of the same rule creates duplicate entries. Never edit the same global file from two concurrent sessions.

### [PASS] Passing checks (table, max 5 rows)

### Finding format

```
- [severity] <symptom> ({file}:{line} if known)
  Why: <one-line reason>
  Action: <exact command or edit to fix>
```

`Action:` must be copy-pasteable. Never write "investigate X" or "consider Y". If the fix is unknown, name the diagnostic command.

A finding refuted in the same breath (a TODO count that turns out to be vendored code or false positives) is not a finding; drop it or fold it into the passing table.

### [!] Critical -- fix now

Confirmed dangerous permissions, consequential rule violations, security findings, and leaked credentials. Server counts and estimated context percentages never establish Critical severity.

Example:

- [!] `settings.local.json` committed to git (exposes MCP tokens)
Why: leaked token enables remote code execution via installed MCP servers
Action: `git rm --cached .claude/settings.local.json && echo '.claude/settings.local.json' >> .gitignore`

### [~] Structural -- fix soon

Agent instructions in the wrong layer, missing hooks, oversized descriptions, verifier gaps.

**Instruction drift.** Use the agent-config summary as leads, then verify the active runtime's actual instruction loading and configuration rules. Runtime adapters in the collector cover particular formats and versions; they do not prove current precedence for every installed agent. Flag a rule only when it is unreachable, contradictory or unsupported in the actual environment. Missing files for an unused runtime, an intentional trust policy, or a different supported project layout are not defects. Important shared constraints should be reachable through the project's authoritative instructions; private local preferences need not be copied into public files. Report key names and redacted evidence, never credentials.

Quick check from the project root, reusing `$HEALTH_SCRIPT` resolved in Step 1 (standalone output has no `AGENT CONFIG SUMMARY` wrapper):

```powershell
& "$POWERSHELL" -NoLogo -NoProfile -ExecutionPolicy Bypass -File "$HEALTH_LAUNCHER" agent-context . summary
```

On Linux and macOS:

```bash
BASH_ENV= ENV= /bin/bash -p "${HEALTH_SCRIPT%/*}/check-agent-context.sh" . summary
```

**AI-maintainability findings.** For the maintainability lane (verification surface, conversation-derived guidance, concentrated fix chains, risk-backed hotspot ownership, non-obvious constraint reachability, verifier wrapper, broken doc and Markdown references, stale verifier cache output), load `references/maintainability-findings.md` and work its checks with `AI MAINTAINABILITY SUMMARY` / `DETAIL`.

### [-] Incremental -- nice to have

Outdated items, global vs local placement, context hygiene, stale allowedTools entries.

If no issues: `All relevant checks passed. Nothing to fix.`

A report-only request does not authorize fixes. Already explicit repair authorization can be handled after the audit without repeated confirmation. The audit is not a substitute for code review, project verification or architecture work; it reports configuration and maintainability findings with concrete next actions.
