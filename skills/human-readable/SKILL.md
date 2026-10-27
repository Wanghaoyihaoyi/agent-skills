---
name: human-readable
description: Optimize AI-generated language for human comprehension while preserving facts and intent. Use when drafting or revising conversational replies, technical reports, summaries, explanations, or voice output; not for code formatting or machine-consumed output.
---

# Human Readable

Optimize for successful human communication, not minimum token count.
Reduce unnecessary cognitive load without removing essential meaning.
Based on the psycholinguistic findings in arXiv:2610.29162.

## 1. Identify the communication context

Select the appropriate mode:

- Conversation: Natural, spoken, easy to follow.
- Technical: Precise, structured, technically complete.
- Executive: Conclusion first, followed by evidence and next actions.

## 2. Detect linguistic complexity

Inspect the draft for diagnostic signals (not absolute prohibitions):

- Long-distance grammatical dependencies.
- Excessive nested clauses.
- Stacked noun phrases.
- Unfamiliar or unnatural word combinations.
- Unnecessary nominalization.
- Ambiguous subjects and actions.
- Excessive information packed into a single sentence.

## 3. Reconstruct the expression

Apply where useful:

- Prefer familiar language over unusual phrasing.
- Keep subjects, actions, and objects close together.
- Replace unnecessary abstract nouns with concrete actions.
- Split sentences when doing so improves comprehension.
- Introduce one major idea at a time.
- Explain necessary technical terms rather than deleting them.
- Make causal relationships explicit.
- Place the most important information where users can easily identify it.

Do not force every sentence to be short.

## 4. Preserve semantics

Never silently alter:

- Facts, numbers, identifiers, or timestamps.
- Business states or tool execution results.
- Uncertainty, limitations, or exceptions.
- Technical constraints and causal relationships.
- User intent or requested level of detail.

Do not convert unknown outcomes into successful outcomes.

## 5. Validate the result

Before returning, check:

- Can the intended audience understand it on the first reading or hearing?
- Is the main conclusion clear?
- Are important details preserved?
- Has the rewrite introduced unsupported claims?
- Is any remaining complexity necessary?

If a rewrite loses important information, restore that information.

## Voice-specific rules

For spoken responses:

- Use natural spoken Chinese when responding in Chinese.
- Put the main result early.
- Avoid reading raw error codes unless needed.
- Avoid long enumerations and deeply nested explanations.
- Distinguish completed, in-progress, failed, and unknown states.
- Do not interrupt required confirmations or hide failures.
- Prefer a short immediate response followed by additional details when appropriate.

## Technical-specific rules

For engineering reports:

- Preserve exact error codes, file paths, API names, and commit identifiers.
- Separate observations, hypotheses, and verified conclusions.
- State what passed, what failed, and what remains unverified.
- Do not replace technical precision with vague reassuring language.

## Efficiency

- Do not automatically invoke another model for every response.
- Prefer applying these rules during initial generation.
- Perform an additional rewrite only when complexity or audience mismatch warrants it.
- Avoid recursive rewriting.
- Never delay urgent or time-sensitive responses for stylistic optimization.

## Success Criteria

A successful output is easier to understand without being less accurate, less complete, or less useful.
