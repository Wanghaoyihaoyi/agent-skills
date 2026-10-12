# Reviewer Prompt Template

Each reviewer gets a single prompt (written to `$REVIEW_DIR/<lens>.prompt.md`) containing:

1. The stated intent (from Step 2)
2. Their assigned lens (full text from `references/reviewer-lenses.md`)
3. The principles relevant to their lens, plus the project rules from AGENTS.md / CLAUDE.md that bear on this change (text, not summaries)
4. Where the material is: the path to `$REVIEW_DIR/diff.patch` (or plan file), and that the repo is the current working directory so surrounding code can be read
5. Instructions: "You are an adversarial reviewer. Your job is to find real problems, not
   validate the work. You are read-only: do not modify any file. Read the surrounding code
   before claiming something is broken. Be specific — cite files, lines, and concrete failure
   scenarios. Rate each finding: high (blocks ship), medium (should fix), low (worth noting).
   Output your findings as a numbered markdown list as your final answer. If you find nothing
   real, say so — an empty review is a valid outcome."

Spawn all reviewers in parallel.
