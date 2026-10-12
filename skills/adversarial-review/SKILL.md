---
name: adversarial-review
description: Cross-model adversarial review of a change. Claude sends reviewers to Codex (`codex exec`), Codex sends them to Claude (`claude -p`), each attacking from a distinct lens (Skeptic / Architect / Minimalist), then a synthesized verdict with lead judgment. Read-only — produces a verdict, makes no changes. Use when asked for "adversarial review", "对手审查", "让 Codex/Claude 审一下", "交叉审查", or after a large diff, a finished plan phase, or a planning session when a second model's scrutiny is worth the cost.
---

# Adversarial Review

Adapted from poteto/noodle for Claude Code and Codex. Spawn reviewers on the **opposite model** to challenge the work. The deliverable is a synthesized verdict — do NOT make changes.

**Hard constraint:** reviewers MUST run through the opposite vendor's CLI (`codex exec` or `claude -p`). Do not use your own subagents as reviewers — they run on your own model, which defeats the purpose. If the opposite CLI is missing or fails, stop and report that; do not quietly fall back to same-model review.

## Step 1 — Load principles

Read the repo's AGENTS.md / CLAUDE.md (and AGENTS.override.md if present). Project rules there — architecture boundaries, contracts, migrations, authorization — are part of what reviewers judge against. Combine them with the principles below and pass the relevant ones to each reviewer.

- **prove-it-works** — "it compiles" or "tests pass" is not proof the goal works end to end. Claims need evidence.
- **fix-root-causes** — fixes belong at the source, not a special case, retry, guard, or fallback where the symptom showed up. The same bug elsewhere should be fixed too.
- **serialize-shared-state-mutations** — concurrent writers to shared state need an explicit ordering or ownership rule; late or stale callbacks must be rejected, not applied.
- **boundary-discipline** — validation at entry points; each component owns its responsibility; no business decisions leaking into transport/adapter layers.
- **foundational-thinking** — design serves the real goal and the actual data/access pattern, not an assumed one.
- **redesign-from-first-principles** — when a replacement lands, everything that belonged only to the old approach (code, config, env vars, docs, tests) is deleted in the same change.
- **subtract-before-you-add** — prefer deleting and simplifying over adding layers, flags, or options without a second concrete use.
- **outcome-oriented-execution** — the change should do what the user needs, no more; scope follows the problem, not the file list.
- **cost-aware-delegation** — watch token/context size, duplicate calls, startup latency, and expensive model use.

## Step 2 — Determine scope and intent

Identify what to review from context (uncommitted diff, a branch vs its base, a commit range, a plan). State the **intent** — what the author is trying to achieve — explicitly before proceeding. Reviewers challenge whether the work *achieves the intent well*, not whether the intent is right.

Collect the confirmed review scope in a per-run directory under the operating system's temporary directory. Include staged, unstaged and relevant untracked content when the target is current work; a plain `git diff` can miss parts of it. Record the base and current revision, the intent, constraints and relevant surrounding files. Do not include unrelated work or credentials.

Choose the smallest set of independent lenses that can cover the actual risk: Skeptic for correctness, Architect for cross-boundary decisions, Minimalist for compensating complexity. File or line counts alone do not require more reviewers. Bound parallelism to available tools and resources.

Lens definitions: `references/reviewer-lenses.md`. Prompt template: `references/reviewer-prompt.md`. Write each prompt to `$REVIEW_DIR/<lens>.prompt.md`.

## Step 3 — Spawn reviewers on the opposite model

Run from the repo root so reviewers can read surrounding code. All reviewers are read-only. Resolve `REVIEW_DIR` to the per-run directory above. Check that the opposite CLI is installed and its current help supports the intended flags. The commands below are POSIX-shell examples, not a requirement for a particular operating system or tool API. Use the environment's supported process/background execution and polling; do not assume a tool parameter named `run_in_background` exists.

**If you are Claude** — reviewers run on Codex:

```sh
codex exec -s read-only --skip-git-repo-check -o "$REVIEW_DIR/skeptic.md" - < "$REVIEW_DIR/skeptic.prompt.md" > "$REVIEW_DIR/skeptic.log" 2>&1
```

Launch only the chosen lenses. Keep each process identifier, exit status and output path; use supported background execution when available, otherwise run sequentially.

**If you are Codex** — reviewers run on Claude:

```sh
claude -p --permission-mode plan --add-dir "$REVIEW_DIR" \
  --allowedTools "Read Grep Glob Bash(git diff:*) Bash(git log:*) Bash(git show:*)" \
  < "$REVIEW_DIR/skeptic.prompt.md" > "$REVIEW_DIR/skeptic.md" 2> "$REVIEW_DIR/skeptic.log"
```

Use bounded waits so the user can receive progress. Parallel runs are optional; avoid one blocking shell wait for all reviewers. Missing CLI support or a failed process is missing review evidence, not a successful verdict.

Name outputs after the lens: `skeptic.md`, `architect.md`, `minimalist.md`.

## Step 4 — Verify and synthesize

Record the actual CLI and model when available, process result and review scope. Confirm each requested output exists and has substantive content. Keep the final verdict or artifacts the user requested; clean up only this run's disposable prompts and logs.

If an output is missing or empty, read its `.log` and state the failure in the verdict — never silently skip a reviewer.

Read each reviewer's output. **Check every high/medium finding against the actual code before accepting it** — reviewers are adversarial by design and do hallucinate. Deduplicate overlapping findings and produce one verdict in the format in `references/verdict-format.md`.

## Step 5 — Lead judgment

Apply your own judgment, using the stated intent, project rules, and principles above. For each finding, accept or reject with a one-line reason. Call out false positives, overreach, and style-as-substance.

Present the verdict in the user's language, following their communication preferences (conclusion first). The review itself makes no changes. If the same task already authorizes fixing accepted findings, continue that work after delivering the review result under the existing scope; otherwise stop at the verdict.
