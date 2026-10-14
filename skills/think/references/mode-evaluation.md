# Evaluation Mode

Activate when the user wants to judge whether something should exist, be kept, exposed, or removed. Typical triggers: "判断一下", "有没有必要", "值不值得", "should we keep this", "is this worth it", "我不想做", "商业前景", "有没有必要继续".

State the evaluation target and what kind of judgment is needed (value, risk, or tradeoff). Take a current-state snapshot: what it does, who uses it, what depends on it; grep and read before opining.

When the proposal adds or removes lasting product or engineering surface, inventory the relevant delta: settings, flags, environment variables, commands, services, tabs, routes, schemas, dependencies, public APIs, and long-lived helpers. Each addition must name its distinct user need, owner, maintenance and rollback cost, and why changing an existing default or affordance cannot achieve the same result. If that case is weak, remove the entity from the proposal; technical feasibility is not necessity.

For product pivot, commercialization, or business-direction requests, frame the market, user, distribution, willingness-to-pay, and maintenance burden before proposing technology. Do not assume open source, do not assume implementation comes first, and do not hide a business judgment inside a technical plan.

**Commercial readiness gate.** When the judgment is whether a product, paid feature, launch, or version is chargeable, evaluate chargeability before implementation. Check delivery and update path, first-run activation/onboarding, payment/license/trial boundary, privacy and network promises, headline-feature reliability and honest degradation, support/refund triggers, competitor wedge, and solo-maintainer maintenance burden. A product is not ready to charge because the happy path works locally; missing distribution, update, licensing, privacy disclosure, or headline-feature reliability is a Keep-building/Pivot blocker.

**Output:** lead with a clear keep, remove, change-direction, or insufficient-evidence judgment in the user's language, after the skill's invocation marker. Give the decisive evidence, meaningful costs and tradeoffs, and what would change the judgment. Do not force three reasons, entity counts, English verdict labels, or a full plan. Compare alternatives only when a real choice remains.

For removal or major rework, explain affected users, contracts and migration or recovery cost. This judgment alone does not authorize implementation; continue existing authorized work without another approval round, and ask only for an unresolved decision or missing authorization.

Distinction: ordinary design answers how to meet a goal; evaluation answers whether a capability should exist or be retained.
