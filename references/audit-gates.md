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
6. **Forward-reference** — Methods and Results introduce no central construct, comparison, claim, study-specific symbol, acronym, configuration code, scenario identifier, metric shorthand, or indexed quantity without an available meaning at first use. PASS evidence: every inheritance reference points only to an earlier section/paragraph or a root in the allowlist defined by `whole-paper-story.md`; it never points to an RQ ID or an output-side paper-story field. Every paragraph consumer points only downstream, to a declared RQ, or to `paper_story.closure_claim`. For notation, provide a first-use ledger covering abstract, prose, equations, captions, tables, and figure labels; each entry points to a preceding or same-location definition, an immediate equation `where` clause, or an explicit citation to the original source defining borrowed notation. A later definition or an unrelated citation is not PASS evidence.
7. **Backward-justification** — Every Discussion mechanism is triggered by a result and grounded in prior work or labeled interpretation. PASS evidence: mechanism-to-result and mechanism-to-literature/status links.
8. **Order-preservation** — The six section roles occur once in canonical order, and problem units retain a stable cross-section order unless analysis requires otherwise. PASS evidence: role/order matrix, acyclic forward-only `must_precede` links, and reasons for every content-order exception.
9. **No-new-branch** — Discussion and Conclusion add no unsupported mechanism, stakeholder, result, citation-dependent novelty, or contribution branch. PASS evidence: each terminal claim traces to an earlier promise and evidence object.
10. **Version-consistency** — Idea, terms, RQs, methods, result labels, and answers belong to the same research version. PASS evidence: version/source record and resolved difference log.
11. **Evidence-consumer** — Every substantive literature stream, table, figure, diagnostic, and output has a named claim or interpretive consumer. PASS evidence: a non-empty evidence ledger at either depth, valid non-empty consumers, and `principal_evidence` equal to an existing ledger ID.

Apply these probes within the eleven gates; fluent prose is not PASS evidence:

- **RQ versus implementation (claim-return, reader-question):** read each gap-to-RQ handoff without its following response sentence. The RQ must still state an unknown. The response may preview a broad comparison or evidence capability; exact operations, fields, settings, and expected outputs first appear where their method role is justified. A sequence of RQ labels does not establish a computational pipeline.
- **Overall and local motivation (reader-question, claim-return):** identify the Introduction's overall gap, its consequence, and the sentence that announces the finite problem set. For every RQ, identify its relation to the central proposition, local gap, local consequence, question, and concise study response. Missing “so what” logic or a sudden list of RQs is a failure even when the questions are individually clear.
- **Literature attribution (backward-justification, evidence-consumer):** verify closest-work findings and review-table rows against their cited sources. Separate reported findings from the author's synthesis; locate the unresolved intersection before prescribing an operation.
- **Reference portfolio adequacy (evidence-consumer, deletion, version-consistency):** for a standard full-length empirical article, verify approximately 70 unique cited works, normally 65--80, unless the project contract records another applicable target. Every retained source needs a verified identity, literature stream, citation function, and RQ or claim consumer. Below-band portfolios fail freeze unless an explicit exception applies; above-band portfolios trigger a redundancy review. Irrelevant padding never satisfies the target.
- **Literature subsection closure (reader-question, backward-justification):** each substantial stream must state what it establishes, what remains open for this paper, and which later requirement consumes that open issue. Repeating the Introduction or appending a generic “we study” sentence is not a closure.
- **Visual reading order (order-preservation, reader-question, evidence-consumer):** record first citation, explanatory paragraph, intended section, and, when a PDF exists, actual page and section for each figure and table. A float arriving several pages after its only explanation or entering an unrelated subsection requires a placement repair unless a documented layout constraint prevents it. Compare captions, headers, notes, and arrow semantics with the prose and current implementation.
- **Main text versus supplement (deletion, evidence-consumer):** keep the compact evidence needed to judge each principal answer in the article. Send exhaustive scenario grids, row-level registries, and audit detail to the supplement only when the article contains a clear summary and points to the supporting object. Material with no named claim consumer belongs in neither location.
- **Answer-first Results and returned Discussion (claim-return, order-preservation):** each Results subsection opens with or quickly reaches the direct answer promised for its RQ. Discussion returns to every RQ in the same order, places each answer in literature dialogue, and separates RQ interpretation from higher-level contribution and practical implication when density requires it.
- **Defensive framing and positive scope (reverse-outline, deletion, no-new-branch):** inspect high-impact positions and every caveat-bearing paragraph. A principal claim must remain intelligible after unnecessary disclaimers are removed; each retained limitation must have one named claim consumer and one proper location. Repeated exclusions, anticipatory rebuttals, or statements of what the paper does not do fail when they substitute for narrowing the claim. Record repairs in the defensive-writing handoff ledger and route sentence-level execution to `$anti-defensive-writing` after architecture approval.
- **Terminology and release consistency (forward-reference, version-consistency):** one canonical label represents each RQ, state, construct, sample, and evidence class throughout text, tables, figures, supplement, and translated versions. After manuscript changes, generated PDFs, documentation, checksums, and review packages must describe the same version before release.
- **Evidence class and version (version-consistency, no-new-branch):** compare review notes with the latest schema and results. State what each output establishes. Generated conformance, descriptive comparison, and fitted-model sensitivity cannot become another evidence class through wording. Valid null or contradictory results constrain claims.

## Common rationalizations to reject

- “The sections are individually polished, so architecture can wait.” Polished prose does not repair a missing RQ return.
- “The topics are all covered.” Coverage does not establish order; apply swap, deletion, and reader-question tests.
- “The figure is useful or visually strong.” Evidence without a named claim consumer is orphaned.
- “The labels imply a factorial comparison.” Naming cannot isolate a mechanism when multiple components change together.
- “The RQ names the operation.” A procedure following an RQ does not show why the question matters or whether it remains open.
- “The table is cited somewhere.” A visual can still arrive too late, interrupt the wrong section, or depict a different process than the implemented study.
- “Discussion can propose an attractive mechanism.” It may interpret a result, but it cannot create unsupported primary evidence or causal identification.
- “A synthetic or constructed test is external validation.” Classify evidence by what the design actually tests.
- “The manuscript uses the latest idea.” Verify Methods, Results, Discussion, and Conclusion rather than trusting one section.
- “Caveats make an overclaim safe.” Narrow the positive claim to the supported estimand.
- “Every possible misunderstanding needs its own disclaimer.” State the exact scope once and place real limitations with the claim they govern.
- “The user is under deadline, so draft prose while auditing.” Deadline never authorizes manuscript prose before the blueprint confirmation gate. Deliver the architecture, blockers, and next decision only.
- “The user asked for both blueprint and Discussion.” This skill completes the blueprint and hands it off; a separate drafting request is executed only after the architecture is accepted through the appropriate writing workflow.

## Gate outcome

At `depth=deep`, freeze only when all eleven gates are reasoned PASS and deep validation succeeds. A `standard` blueprint does not require stored paragraph records or semantic-gate records and must be validated as `standard`. Any gate assessed during an audit that fails remains visible with repair impact; do not convert uncertainty into PASS to meet a deadline. A BLOCKER prevents blueprint approval. MAJOR and MINOR findings may be reported without edits in audit mode.
