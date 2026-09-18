# Whole-Paper Story

Use this reference for the macro spine, cross-section returns, section contracts, version control, and blueprint schemas. It defines what must connect; `section-arcs.md` defines the internal order of each section.

## Macro spine

Build one dependency chain:

`phenomenon -> practical tension -> literature's partial answer -> unresolved mechanism or intersection -> RQ -> method response -> evidence validity -> principal evidence -> boundary evidence -> interpretation -> knowledge change -> stakeholder action -> bounded closure`

The central proposition is the shortest evidence-bounded statement that makes this chain one paper. Each link must create a reader question answered by the next link. Do not use conventional headings as evidence that the dependency exists.

## Claim-return mapping

Create one chain for every RQ or primary claim:

`problem -> gap -> consequence -> RQ -> method capability -> result -> Discussion interpretation -> Conclusion closure`

Each RQ return-chain field targets the indicated canonical role: `problem` and `consequence` -> `introduction`; `gap` -> `related_work`; `method` -> `methods`; `result` -> `results`; `discussion` -> `discussion`; `conclusion` -> `conclusion`. At `standard`, every field must target the corresponding section ID. At `deep`, every field must target a paragraph ID contained by that role. In either case, the target section's `rq_consumers` must contain the chain's RQ ID.

Require exact IDs at each link. A chain is broken when an RQ lacks a method object or result, when Discussion answers more than Results establish, or when Conclusion strengthens the interpretation. Preserve the RQ/claim order across sections unless a documented analytical dependency requires a different order.

Map every substantive literature stream, method component, table, figure, diagnostic, and audit output to at least one named downstream claim or interpretation. Remove or explicitly reclassify orphan evidence; visual polish is not a consumer.

## Section contracts

Each section contract records the question it receives, its unique job, what it may use, what it may not do, and the question it hands onward. A locally coherent section fails when it silently performs another section's job or has no downstream consumer.

Use stable identifiers for all sections and, at `deep`, all paragraphs. Every section has one canonical `role` in this order: `introduction`, `related_work`, `methods`, `results`, `discussion`, `conclusion`. All six roles occur exactly once. `name` is a free display title and may follow journal conventions; never infer function from the title.

`must_precede` lists only existing later section IDs that this section actually precedes, normally its immediate dependency successor. It cannot contain the section itself, point to an earlier canonical role, or create a cycle. `rq_consumers` is a non-empty list of one or more declared RQ IDs served by the section; it is not a general claim registry.

Dependency references are directional. A section's `inherits_from_previous` and a paragraph's `inherits_from` may reference only an allowed upstream paper-story root or an earlier section/paragraph in canonical and local order. The paper-story root allowlist is exactly: `paper_story.central_proposition`, `paper_story.phenomenon`, `paper_story.practical_tension`, `paper_story.literature_default_or_partial_answer`, `paper_story.unresolved_mechanism_or_intersection`, and `paper_story.research_questions`. An RQ ID is not a valid inheritance target. Neither are `paper_story.method_response`, `paper_story.principal_evidence`, `paper_story.boundary_evidence`, `paper_story.theoretical_or_methodological_reframing`, `paper_story.stakeholder_actions`, or `paper_story.closure_claim`.

A paragraph's `consumed_by` may reference only downstream sections/paragraphs, a declared RQ, or `paper_story.closure_claim`. No inheritance edge may point forward, and no consumption edge may point backward or sideways.

## Version consistency

Record an authoritative version identifier or dated source for the idea, RQs, constructs, method objects, result labels, and evidence status. Compare them before freezing:

- identical terms must denote identical constructs across sections;
- changed RQs must propagate through method, result, interpretation, and closure records;
- retired claims cannot survive in Discussion or Conclusion;
- renamed evidence must keep traceable aliases or be updated everywhere;
- conflicting versions remain visible until the user identifies the authority.

Do not merge two plausible versions into a synthetic compromise. In `update`, produce an impact map first: changed source -> directly affected IDs -> downstream consumers -> invalidated gate verdicts -> proposed blueprint-only edits.

## Depth contracts

A `standard` blueprint contains the complete top-level `paper_story`, one contract for each canonical role in canonical order, the RQ return chains, and a non-empty evidence ledger. It may omit `paragraphs` and `semantic_gates`. Every RQ-chain field and every evidence consumer must target an existing section ID.

A `deep` blueprint contains the same macro and section contracts, a non-empty evidence ledger, at least one complete paragraph record per section, and all eleven semantic gates. Every RQ-chain field and every evidence consumer must target an existing paragraph ID in the required canonical role.

For both depths:

- section, paragraph, evidence, and RQ IDs are unique within their respective validated namespaces; section and paragraph IDs are also unique across the story graph;
- every evidence consumer and every RQ-chain target names an ID that exists in that blueprint;
- `principal_evidence` names an evidence ID that exists in the non-empty `evidence_ledger`;
- the set of RQ IDs and the set of RQ-chain IDs are identical;
- every section's `rq_consumers` is non-empty and contains only declared RQ IDs;
- every paragraph's `section_id` equals the ID of its containing section;
- at `deep`, every paragraph's `inherits_from` and `consumed_by` lists are non-empty; inheritance uses only the root allowlist or existing upstream section/paragraph IDs, while consumption uses only existing downstream section/paragraph IDs, declared RQs, or `paper_story.closure_claim`.

## Canonical blueprint schema

The completed Markdown must contain one fenced YAML block compatible with the validator. Use non-empty, project-specific values rather than scaffold text.

```yaml
paper_story:
  central_proposition: "Evidence-bounded unifying proposition"
  phenomenon: "Observed or consequential phenomenon"
  practical_tension: "Actor, decision, or failure tension"
  literature_default_or_partial_answer: "What existing work establishes"
  unresolved_mechanism_or_intersection: "Exact unresolved object"
  research_questions:
    - id: "RQ-1"
      question: "Answerable question"
  method_response: "Capabilities matched to the RQs"
  principal_evidence: "EVID-1"
  boundary_evidence: "Diagnostics, robustness, or scope evidence"
  theoretical_or_methodological_reframing: "Knowledge change supported by evidence"
  stakeholder_actions: "Actor-condition-action consequences"
  closure_claim: "Strongest supported closing claim"
  sections:
    - id: "SEC-INTRO"
      role: "introduction"
      name: "Problem framing and research questions"
      entry_question: "Why should the reader care?"
      inherits_from_previous: "paper_story.phenomenon"
      establishes: "Problem, gap, consequence, RQs, and design promise"
      evidence_inputs: []
      prohibited_jobs: ["Report new results"]
      must_precede: ["SEC-LR"]
      handoff_to_next: "What is known, and where does it stop?"
      rq_consumers: ["RQ-1"]
      paragraphs:
        - id: "INTRO-P1"
          section_id: "SEC-INTRO"
          reader_question_received: "Why does the phenomenon matter?"
          inherits_from: ["paper_story.phenomenon"]
          single_job: "Establish the practical tension"
          evidence_form: "Field evidence"
          citation_obligation: "External factual claims require sources"
          claim_scope: "Defined setting and decision"
          closure_claim: "The tension requires an auditable answer"
          handoff_question: "What has prior work resolved?"
          consumed_by: ["INTRO-P2"]
  evidence_ledger:
    - id: "EVID-1"
      source: "Verified result artifact"
      finding: "Evidence-bounded finding"
      consumers: ["RESULTS-P1", "DISC-P1"]
  rq_return_chains:
    - id: "RQ-1"
      problem: "INTRO-P1"
      gap: "LR-P3"
      consequence: "INTRO-P4"
      method: "METHOD-P2"
      result: "RESULTS-P3"
      discussion: "DISC-P1"
      conclusion: "CONC-P1"
  semantic_gates:
    - id: "reverse-outline"
      verdict: "PASS"
      reason: "Each paragraph has one distinct job"
```

The block above shows the additional paragraph and gate structure used at `deep`. Repeat section records for all six canonical roles in canonical order; choose display titles appropriate to the journal. Include all eleven semantic-gate records defined in `audit-gates.md`. A PASS without concrete blueprint evidence is not a semantic pass.

For `standard`, omit every `paragraphs` block and omit `semantic_gates`; change every RQ-chain target and evidence consumer in this example to the appropriate existing `SEC-*` ID. Validate with the matching `--depth` rather than relying on the validator's default.
