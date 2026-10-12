---
name: how
description: Explain how something works in this codebase by exploring the real code and producing a clear architectural explanation; optionally critique the architecture with independent reviewers. Use for "how does X work", "walk me through what happens when…", "X 是怎么运作的", "讲讲这块", "从 A 到 B 经过哪些环节", or when asked to find architectural problems in a subsystem. Read-only; not for fixing bugs or reviewing a diff.
---

# How

Answer "how does X work?" questions. Produce an explanation that lets the reader build a working mental model of a subsystem — enough to reason about it and make decisions, not an annotated source listing.

Adapted from poteto/how for both Claude Code and Codex. Two modes:

1. **Explain** (default) — explore the codebase and produce a clear explanation
2. **Critique** — explain first, then have independent reviewers look for architectural issues

## Audience and language

- Write in the user's language. Follow the user's own communication preferences (global instructions, AGENTS.md / CLAUDE.md) over the defaults here.
- Default reader: a smart owner who is not in the code every day. Lead with the conclusion, use plain words, explain any unavoidable term in half a sentence the first time. File and function references go in "Where Things Live", not scattered through prose.
- If the user is clearly an engineer asking for code-level detail, go deeper.

## Explain Mode

### Step 1 — Understand the question and assess complexity

Parse what is being asked: a subsystem, a feature flow, an architectural overview, or a runtime trace ("what happens when a user says …"). If ambiguous, state your interpretation and proceed — don't ask; the user can redirect.

Read the repo's AGENTS.md / CLAUDE.md and any architecture doc they point to for this area first — they are the map. Then verify against code: docs describe intent, code is the fact. Call out any place where they disagree.

- **Simple** (one module, a narrow question): explore and explain yourself in one pass. Go to Step 4.
- **Complex** (spans several services/files, cross-cutting flow, full overview): go to Step 2. When in doubt, take the simple path first.

### Step 2 — Parallel exploration (complex questions only)

Split a complex question into distinct angles only when that reduces duplication or isolates substantial context (for example entry point, business flow, persistence, external boundary). Use `references/explorer-prompt.md` as a tracing checklist.

Prefer exploring directly for a narrow question. If delegation materially helps and is permitted, use the current environment's actual agent tools and the cheapest capable available model; do not assume named agent types or a particular provider. Without delegation, trace the angles sequentially.

Exploration must read actual code, trace call chains to the relevant effects, and state what could not be verified.

### Step 3 — Synthesize

Reconcile the findings yourself (the orchestrator already holds the context — don't spawn another agent just to write). Follow `references/explainer-prompt.md`. Where explorers contradict each other, re-read the code to settle it.

### Step 4 — Present

Structure (drop sections that add nothing):

- **一句话结论 / Overview** — what it is, what it does, why it exists. Reader can stop here.
- **Key Concepts** — only the pieces needed to follow the rest, each defined in plain words.
- **How It Works** — the longest part. Trigger → steps → decision points → result, in prose. Add a mermaid or ASCII diagram only when several components talk to each other.
- **Where Things Live** — short map of files/directories (as clickable paths when the client supports it).
- **Gotchas** — surprising behavior, historical leftovers, sharp edges, doc-vs-code mismatches.
- **Open Questions** — what you could not verify, stated plainly.

## Critique Mode

Triggered when the user asks for architectural problems, risks, or improvements — not just understanding.

1. **Explain first** (full Explain Mode). You must understand before you critique.
2. **Critique against evidence.** Use `references/critic-prompt.md` and `references/critique-rubric.md` as a checklist. Review locally by default. When an independent review is requested or materially useful and permitted, pass the relevant explanation and files through available read-only review tools. An explicitly requested cross-model review can use `adversarial-review` if installed; otherwise explain what independent review is available. Do not force two vendors, a fixed agent count or an unavailable CLI for every architecture question.

3. **Lead judgment.** You are a pragmatic lead, not an aggregator. Sort findings into **Act on** / **Consider** / **Noted** / **Dismissed** (wrong, missing context, or style preference), each with a one-line reason.

Present the explanation first, then the critique below it — someone who only wants to understand the system should not have to wade through critique.

This explanation and critique are read-only. A bundled, already authorized fix can continue after the explanation under its own implementation workflow; this skill alone grants no edit permission.
