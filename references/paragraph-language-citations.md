# Paragraph, Language, and Citation Records

Use this reference at `depth=deep` or when auditing paragraph roles, transitions, citation obligations, or scope language. It plans functions; it does not draft or polish manuscript prose.

## Paragraph dependency record

Create one record per planned or audited paragraph:

```yaml
paragraph:
  id: "DISC-P2"
  section_id: "SEC-DISC"
  reader_question_received: "Why did the RQ1 pattern occur?"
  inherits_from: ["RESULTS-P3", "DISC-P1"]
  single_job: "Explain the bounded mechanism behind RQ1"
  evidence_form: "Result-triggered interpretation plus literature dialogue"
  citation_obligation: "Cite prior mechanism evidence; point to the internal result"
  claim_scope: "The observed setting and defined comparison"
  closure_claim: "The mechanism explains the pattern within the tested boundary"
  handoff_question: "How does this revise prior knowledge?"
  consumed_by: ["DISC-P3", "CONC-P1"]
```

`single_job` must be unique in the local sequence. At `deep`, `inherits_from` and `consumed_by` must each be non-empty lists of existing accepted references. `inherits_from` names premises or evidence already established. `closure_claim` states what this paragraph earns; `handoff_question` makes the next unit necessary; `consumed_by` proves the paragraph is not decorative.

## Sentence-function citation obligations

Plan citations by what a sentence does:

| Sentence function | Obligation |
|:--|:--|
| External fact, prevalence, definition, or institutional rule | External citation required |
| Field-level synthesis | Multiple representative sources normally required |
| A specific prior method or finding | Cite the originating work; author-driven form may be useful |
| Gap or missing-capability claim | Cite the closest-work set or verified search evidence |
| Transition between already supported points | Usually no citation |
| This paper's aim, RQ, design choice, contribution, or organization | Usually no external citation |
| Interpretation of this paper's result | Point to the internal result; use external sources only for dialogue |

Reject blanket citation-density targets, including an 85% rule. Such thresholds reward stuffing and distort Introduction and Methods. Literature synthesis should be citation-rich because of its functions, not because it must reach a percentage. Every planned citation needs a role such as definition, synthesis, contrast, method, finding, or closest-work positioning.

## Positive and precise scope

Record the strongest affirmative claim supported by the evidence, then record its real boundary once where that boundary controls interpretation.

- Prefer `scope = population, setting, comparison, time, estimand, or evidence class actually examined`.
- Narrow an overbroad claim by changing its subject or predicate, not by surrounding it with vague hedges.
- Distinguish uncertainty from limitation: uncertainty concerns an estimate or inference; limitation concerns what the design can establish.
- Do not scatter “does not claim,” “cannot prove,” or anticipatory rebuttals across high-impact positions.
- Keep necessary causal, external-validity, novelty, ethical, and methodological limits explicit.

This is an architecture constraint, not authorization to rewrite sentences. When prose needs revision, pass the accepted claim scope to the relevant drafting or language workflow.

## Transition as logical handoff

A transition is valid only if it carries at least one of:

1. an unresolved question;
2. a change of analytical level;
3. a newly necessary construct;
4. a validity condition required by the next claim;
5. a completed claim whose consequence motivates the next unit.

Connector words such as “however” and “therefore” are not evidence of a handoff. Test the record by deleting the transition wording: the dependency should remain visible in the inherited premise and outgoing question.
