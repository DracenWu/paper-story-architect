# Section Arcs

Use this reference to test the six canonical functional roles in order: `introduction`, `related_work`, `methods`, `results`, `discussion`, `conclusion`. Role order is mandatory; top-level heading count, display titles, and paragraph counts are not. Related-work functions may be integrated into the Introduction and conclusion functions may be integrated into the end of Discussion when target-journal practice supports that presentation. Keep them as distinct blueprint units so their jobs and RQ returns remain auditable. RQ return fields follow the canonical order: problem/consequence -> `introduction`, gap -> `related_work`, method -> `methods`, result -> `results`, discussion -> `discussion`, conclusion -> `conclusion`; each target role must list the RQ in `rq_consumers`.

## `introduction`

Order: `phenomenon/significance -> practical tension -> compact prior-work map -> precise limitation -> consequence -> aim/RQs -> method fit -> bounded contribution -> roadmap`.

The Introduction creates promises; it does not discharge them. Its compact prior-work map must close with an overall gap and a concrete consequence: what decision, inference, or use remains unreliable if the gap persists. It must then announce the finite set of linked problems before presenting them. Each problem unit connects a prior-work synthesis to an exact local gap, explains its consequence, states the RQ, and may close with a concise account of how this study responds. Method fit states capability, not implementation detail. Contributions may not exceed the evidence planned later.

Keep local gap, consequence, RQ, and study response in that order. State an RQ as an unknown about the research object. A response preview may name the comparison or evidence capability used to answer it; put chosen fields, thresholds, model variants, test settings, and detailed expected outputs in Methods. Connect problem units through their logical dependency rather than mechanical “first question/second question” labels. Check demonstratives such as “this representation” against an antecedent already available to the reader.

Handoff: a finite set of questions and required capabilities that Related Work and Methods must establish.

## `related_work`

Order: `research object/boundary -> problem-oriented solution streams -> necessary mechanisms -> contextual or temporal conditions -> closest work -> unresolved intersection -> design requirements`.

Order streams by cognitive dependency, not chronology, search bins, or method labels. Each subsection receives an `entry_question`, establishes a premise, identifies the residual problem, and hands that exact problem onward. Transition words do not create dependency. If adjacent units can be swapped without loss, clarify their dependency, merge them, or remove one.

For each stream, distinguish the question studied, actual method, reported finding, and remaining question. A literature-to-RQ handoff states the unresolved question; it does not prescribe the authors' chosen workflow immediately after an RQ label. Reserve exact expected outputs, implementation fields, and settings for Methods. A review can explain why a capability is needed without presenting this study's solution as prior knowledge. Verify categorical novelty claims against the closest work.

Close each substantial subsection by synthesizing what the stream establishes, the specific issue it leaves open for this paper, and, where useful, the broad capability this study uses to address it. This closure should advance the paper's logic rather than repeat a generic claim that prior work is limited. The Introduction gives the compact map; Related Work supplies the deeper evidence and should preserve the same problem order.

When a literature landscape table helps, use it to synthesize streams and the unresolved intersection. Verify each row's source and analytical role. Repeating RQ labels in every row is no substitute for explaining the connection. Plan its first citation at the synthesis paragraph in Related Work and keep it near that paragraph in the rendered paper.

Handoff: evidence-backed method requirements, not a scarcity claim.

## `methods`

Order: `design requirement -> unit/setting/temporal order -> constructs and eligibility or measurement -> controlled comparisons -> execution or estimation -> diagnostics -> claim scope`.

Translate every RQ into executable or estimable objects before implementation details. State what changes, what remains fixed, expected outputs, and interpretation rules. Put a genuine scope condition next to the operation it constrains. Methods defines evidence objects; it does not announce findings or repair an unresolved literature gap.

Separate the evidence classes the study actually uses before naming results. Source construction, annotation reliability, generated conformance, descriptive comparison, model sensitivity, and external validation establish different things. Explain consequential inherited choices as study-specific definitions, without treating a loosely related citation as proof of optimality. Keep hashes, paths, and maintenance logs out of narrative prose unless a detail is necessary to interpret or reproduce a scientific quantity.

Handoff: predefined evidence objects and rules that Results can report without inventing a new estimand.

## `results`: evidence ladder

Order: `input/descriptive validity -> analytical, model, audit, or conformance credibility -> principal answers in RQ order -> boundary/sensitivity/robustness evidence -> compact synthesis`.

A validity condition must precede any claim that depends on it. Results establishes what happened under defined comparisons, not why it matters theoretically. Figures and tables require named claims and text consumers. A bundled contrast cannot be narrated as an isolated mechanism effect; a controlled fixture cannot silently become external validation.

Show the decision-bearing observation rather than repeating output cells that hide it. Keep relevant null and boundary findings. If evidence contradicts an intended claim, narrow or withdraw the claim. Check denominators, estimands, labels, and evidence status against current result artifacts.

Organize principal findings in the promised RQ order. Open each RQ subsection with its direct evidence-based answer, then present the quantities and displays that earn it. When prose carries several comparable estimates, states, scenarios, or model families, test whether a compact table would expose the pattern more clearly. Put the summary needed to evaluate the main claim in the article; place exhaustive grids, cell-level outputs, and audit detail in the supplement with an explicit main-text consumer.

Handoff: a bounded finding set, with validity and uncertainty attached, that Discussion must consume.

## `discussion`: explanation ladder

For each major RQ, use: `direct answer -> brief evidence reminder -> literature dialogue -> knowledge change -> boundary`. After completing the RQ-level interpretations, synthesize the theoretical or methodological contribution and then the practical implications. For papers with several RQs or a dense evidence base, separate these functions with descriptive subsections; do not force headings when a shorter discussion remains unmistakably ordered.

Discussion interprets results without repeating tables. Every mechanism must be triggered by a result and grounded in prior literature or labeled as interpretation. For each RQ, identify which prior finding is extended, qualified, or placed in a new setting, and show whether the gap promised in the Introduction was actually closed. Complete RQ-level explanations before synthesizing higher-level implications. Theoretical or methodological contributions state the change in knowledge; practical implications name the actor, condition, and action. Limitations reverse-map to design simplifications, data scope, or evidence class; they do not form a generic disclaimer list.

Handoff: stable interpretations at the same strength that Conclusion may compress.

## `conclusion`: closure

Order: `opening problem -> answers in original RQ order -> unifying contribution -> evidence boundary -> tightly matched extension`.

Conclusion is compression, not escalation. It adds no new data, result, mechanism, stakeholder, citation, novelty branch, or stronger causal/generalization language. It returns the same conceptual vocabulary and ordering promised by the Introduction.

## Cross-section prohibitions and handoffs

- Introduction must not contain result claims that later evidence has not established.
- Related Work must not become an annotated bibliography or supply method implementation prose.
- Methods must not interpret outcomes.
- Results must not create a new literature gap or theoretical mechanism.
- Discussion must not introduce primary evidence.
- Conclusion must not expand scope or novelty.

For every figure and table, record its first substantive citation, explanatory paragraph, and intended section. When a rendered manuscript exists, inspect its actual page and reading order: explanation should precede or accompany the visual, and a float should not interrupt an unrelated section. Check that captions, grouped headers, notes, and arrow meanings match the prose and implemented objects. Visual proximity alone does not validate numerical content.

At each handoff, record the unresolved reader question and the downstream unit that answers it. `inherits_from_previous` and paragraph `inherits_from` point only to an earlier section/paragraph or a paper-story root explicitly allowed by `whole-paper-story.md`; RQ IDs and output-side paper-story fields are not inheritance targets. Paragraph `consumed_by` points only downstream, to a declared RQ, or to `paper_story.closure_claim`. A smooth sentence-level transition cannot compensate for a missing logical consumer. At both depths, retain a non-empty evidence ledger and make `principal_evidence` name one of its evidence IDs.
