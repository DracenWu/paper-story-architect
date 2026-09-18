# Section Arcs

Use this reference to test the six canonical functional roles in order: `introduction`, `related_work`, `methods`, `results`, `discussion`, `conclusion`. Role order is mandatory; display titles and paragraph counts are not. RQ return fields follow that order: problem/consequence -> `introduction`, gap -> `related_work`, method -> `methods`, result -> `results`, discussion -> `discussion`, conclusion -> `conclusion`; each target role must list the RQ in `rq_consumers`.

## `introduction`

Order: `phenomenon/significance -> practical tension -> compact prior-work map -> precise limitation -> consequence -> aim/RQs -> method fit -> bounded contribution -> roadmap`.

The Introduction creates promises; it does not discharge them. Each gap unit must connect a prior-work synthesis to an exact unresolved object, explain the consequence, and establish the corresponding aim. Method fit states capability, not implementation detail. Contributions may not exceed the evidence planned later.

Handoff: a finite set of questions and required capabilities that Related Work and Methods must establish.

## `related_work`

Order: `research object/boundary -> problem-oriented solution streams -> necessary mechanisms -> contextual or temporal conditions -> closest work -> unresolved intersection -> design requirements`.

Order streams by cognitive dependency, not chronology, search bins, or method labels. Each subsection receives an `entry_question`, establishes a premise, identifies the residual problem, and hands that exact problem onward. Transition words do not create dependency. If adjacent units can be swapped without loss, clarify their dependency, merge them, or remove one.

Handoff: evidence-backed method requirements, not a scarcity claim.

## `methods`

Order: `design requirement -> unit/setting/temporal order -> constructs and eligibility or measurement -> controlled comparisons -> execution or estimation -> diagnostics -> claim scope`.

Translate every RQ into executable or estimable objects before implementation details. State what changes, what remains fixed, expected outputs, and interpretation rules. Put a genuine scope condition next to the operation it constrains. Methods defines evidence objects; it does not announce findings or repair an unresolved literature gap.

Handoff: predefined evidence objects and rules that Results can report without inventing a new estimand.

## `results`: evidence ladder

Order: `input/descriptive validity -> analytical, model, audit, or conformance credibility -> principal answers in RQ order -> boundary/sensitivity/robustness evidence -> compact synthesis`.

A validity condition must precede any claim that depends on it. Results establishes what happened under defined comparisons, not why it matters theoretically. Figures and tables require named claims and text consumers. A bundled contrast cannot be narrated as an isolated mechanism effect; a controlled fixture cannot silently become external validation.

Handoff: a bounded finding set, with validity and uncertainty attached, that Discussion must consume.

## `discussion`: explanation ladder

For each major RQ, use: `direct answer -> brief evidence reminder -> mechanism -> literature dialogue -> theoretical or methodological implication -> actor-condition-action implication -> boundary`.

Discussion interprets results without repeating tables. Every mechanism must be triggered by a result and grounded in prior literature or labeled as interpretation. Complete RQ-level explanations before synthesizing higher-level implications. Practical implications must name the actor, condition, action, and misuse boundary. Limitations reverse-map to design simplifications, data scope, or evidence class; they do not form a generic disclaimer list.

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

At each handoff, record the unresolved reader question and the downstream unit that answers it. `inherits_from_previous` and paragraph `inherits_from` point only to an earlier section/paragraph or a paper-story root explicitly allowed by `whole-paper-story.md`; RQ IDs and output-side paper-story fields are not inheritance targets. Paragraph `consumed_by` points only downstream, to a declared RQ, or to `paper_story.closure_claim`. A smooth sentence-level transition cannot compensate for a missing logical consumer. At both depths, retain a non-empty evidence ledger and make `principal_evidence` name one of its evidence IDs.
