# Audit Gates

Use this reference for `mode=audit`, all `depth=deep` builds, and final blueprint freezing. Semantic PASS requires identified artifact evidence and a short reason; the deterministic validator cannot substitute for judgment.

## Severity

- `BLOCKER`: the paper's central proposition, RQ/evidence chain, research version, or drafting authorization is unresolved; architecture cannot be frozen.
- `MAJOR`: a section order, handoff, consumer, or claim scope is materially wrong but repair does not require redefining the entire study.
- `MINOR`: a local dependency or record is ambiguous while the global chain remains valid.

Each finding reports severity, affected IDs/sections, failed gate, concrete evidence, required repair outcome, and whether the blueprint or manuscript is affected. Audit is read-only unless separately authorized.

## Eleven gates and PASS evidence

1. **Reverse-outline** — Every paragraph has one distinct job. PASS evidence: complete paragraph-ID-to-job map with no duplicates or mixed jobs.
2. **Adjacent-swap** — Neighboring units are ordered by dependency. PASS evidence: for each non-obvious adjacency, state which premise would disappear or arrive late if swapped.
3. **Deletion** — Every unit is necessary. PASS evidence: each paragraph/stream has a named later claim or consumer; dispensable material is removed or reclassified.
4. **Reader-question** — Each unit answers an inherited question and creates the next necessary question. PASS evidence: populated receive/handoff fields with matching adjacent IDs.
5. **Claim-return** — Every RQ returns through the canonical role mapping: problem/consequence -> `introduction`, gap -> `related_work`, method -> `methods`, result -> `results`, discussion -> `discussion`, conclusion -> `conclusion`. PASS evidence: every target exists at the selected depth, and its containing section lists that RQ in `rq_consumers`.
6. **Forward-reference** — Methods and Results introduce no central construct, comparison, or claim without earlier motivation/definition. PASS evidence: every inheritance reference points only to an earlier section/paragraph or a root in the allowlist defined by `whole-paper-story.md`; it never points to an RQ ID or an output-side paper-story field. Every paragraph consumer points only downstream, to a declared RQ, or to `paper_story.closure_claim`.
7. **Backward-justification** — Every Discussion mechanism is triggered by a result and grounded in prior work or labeled interpretation. PASS evidence: mechanism-to-result and mechanism-to-literature/status links.
8. **Order-preservation** — The six section roles occur once in canonical order, and problem units retain a stable cross-section order unless analysis requires otherwise. PASS evidence: role/order matrix, acyclic forward-only `must_precede` links, and reasons for every content-order exception.
9. **No-new-branch** — Discussion and Conclusion add no unsupported mechanism, stakeholder, result, citation-dependent novelty, or contribution branch. PASS evidence: each terminal claim traces to an earlier promise and evidence object.
10. **Version-consistency** — Idea, terms, RQs, methods, result labels, and answers belong to the same research version. PASS evidence: version/source record and resolved difference log.
11. **Evidence-consumer** — Every substantive literature stream, table, figure, diagnostic, and output has a named claim or interpretive consumer. PASS evidence: a non-empty evidence ledger at either depth, valid non-empty consumers, and `principal_evidence` equal to an existing ledger ID.

## Common rationalizations to reject

- “The sections are individually polished, so architecture can wait.” Polished prose does not repair a missing RQ return.
- “The topics are all covered.” Coverage does not establish order; apply swap, deletion, and reader-question tests.
- “The figure is useful or visually strong.” Evidence without a named claim consumer is orphaned.
- “The labels imply a factorial comparison.” Naming cannot isolate a mechanism when multiple components change together.
- “Discussion can propose an attractive mechanism.” It may interpret a result, but it cannot create unsupported primary evidence or causal identification.
- “A synthetic or constructed test is external validation.” Classify evidence by what the design actually tests.
- “The manuscript uses the latest idea.” Verify Methods, Results, Discussion, and Conclusion rather than trusting one section.
- “Caveats make an overclaim safe.” Narrow the positive claim to the supported estimand.
- “The user is under deadline, so draft prose while auditing.” Deadline never authorizes manuscript prose before the blueprint confirmation gate. Deliver the architecture, blockers, and next decision only.
- “The user asked for both blueprint and Discussion.” This skill completes the blueprint and hands it off; a separate drafting request is executed only after the architecture is accepted through the appropriate writing workflow.

## Gate outcome

At `depth=deep`, freeze only when all eleven gates are reasoned PASS and deep validation succeeds. A `standard` blueprint does not require stored paragraph records or semantic-gate records and must be validated as `standard`. Any gate assessed during an audit that fails remains visible with repair impact; do not convert uncertainty into PASS to meet a deadline. A BLOCKER prevents blueprint approval. MAJOR and MINOR findings may be reported without edits in audit mode.
