# Triage Mode

Activate when the user forwards a bundle of asks: an issue with multiple requests, a batch of screenshots, a user saying "看看这几个需求", or several distinct items that need independent acceptance or rejection.

For an evaluation request, do not silently turn the bundle into implementation.
For already requested implementation, preserve that authorized scope, including
explicitly requested styling; classify only genuine gaps or unresolved choices.
Use these categories as needed:

| Bucket | Meaning | Action |
|--------|---------|--------|
| **Bug** | Broken behavior with evidence | Fix |
| **Already works** | The feature exists but the reporter missed it | Point to the existing affordance |
| **Accepted improvement** | Genuine gap, low-risk, aligns with product direction | Implement |
| **Cosmetic / preference** | Subjective, no functional impact | Note it, do not implement unless the maintainer agrees |
| **Out of scope** | Conflicts with product boundary or adds unjustified complexity | Decline with one sentence |

Use a compact table when it helps independent decisions; place it after the invocation marker and a brief conclusion. Implement the subset already covered by explicit authorization; a read-only triage request needs approval before implementation. Ask only for an unresolved choice or scope expansion. "Already works" misidentified as missing is the most common waste; grep for the existing affordance before classifying an item as a gap.

**Negative-user feedback is not automatic scope.** Refund, churn, and "competitor X is more intuitive" complaints often land on deliberate product differentiation, not an oversight. Before converting the complaint into a rework plan, read the project's own docs for the criticized behavior named as a deliberate choice; if it is, state the original reason and compare it with current evidence. Preserve the boundary pending any necessary business decision, but do not automatically treat old differentiation as proof the design should stay. Do not write a "fix the friction" plan that quietly removes the differentiator.
