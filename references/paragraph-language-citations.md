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

Reject blanket sentence-level citation-density targets, including an 85% rule. Such thresholds reward stuffing and distort Introduction and Methods. Literature synthesis should be citation-rich because of its functions, not because every sentence must contain a citation. Every planned citation needs a role such as definition, synthesis, contrast, method, finding, or closest-work positioning.

In literature synthesis, separate an originating study's finding from the author's cross-study inference. A citation supports what its source actually reports, not an adjacent new interpretation. Count references cited in the final text, not unused bibliography entries, and remove sources included only to reach a numerical target. Verify each review-table row's study object, method, and finding against its sources.

## Reference portfolio size and coverage

For a standard full-length empirical article, target approximately 70 unique references cited in the manuscript. Treat 65--80 as the normal planning band. A user-specified target, a different article type, or a verified journal limit takes precedence and must be recorded in the project contract. Review articles, short communications, registered reports, and theory papers require an explicit format-specific target rather than automatic use of the empirical-article band.

Build a reference-portfolio ledger with:

`source_id | verified_identity | literature_stream | rq_or_claim_consumer | citation_function | intended_section | main_or_supplement | retained_or_removed`

The portfolio must cover the research phenomenon and context, theoretical or conceptual foundations, each RQ's literature stream, measurement or method foundations, the closest-work set supporting the gap, sources needed to interpret the results, and relevant recent work from the target journal. Count unique works actually cited in the canonical manuscript; report supplement-only sources separately when the supplement has a separate bibliography.

The blueprint cannot freeze when a standard empirical article contains fewer than 65 cited works unless the user or verified journal format supplies an explicit exception. More than 80 is a pruning trigger, not an automatic failure: remove redundant or weakly connected sources, while retaining additional works that perform distinct necessary functions. Never add a source solely to enter the band. If relevance screening leaves the portfolio below target, report the uncovered literature streams and continue literature discovery rather than padding the bibliography.

## Positive and precise scope

Record the strongest affirmative claim supported by the evidence, then record its real boundary once where that boundary controls interpretation.

- Prefer `scope = population, setting, comparison, time, estimand, or evidence class actually examined`.
- Narrow an overbroad claim by changing its subject or predicate, not by surrounding it with vague hedges.
- Distinguish uncertainty from limitation: uncertainty concerns an estimate or inference; limitation concerns what the design can establish.
- Do not scatter “does not claim,” “cannot prove,” or anticipatory rebuttals across high-impact positions.
- Keep necessary causal, external-validity, novelty, ethical, and methodological limits explicit.

This is an architecture constraint, not authorization to rewrite sentences. When prose needs revision, pass the accepted claim scope to the relevant drafting or language workflow.

## Defensive-writing planning record

At manuscript level, inspect high-impact positions first: title, abstract, Introduction openings and contributions, RQ statements, Results answers, Discussion contribution claims, and Conclusion. Each should lead with the supported scientific content rather than an exclusion, apology, anticipatory rebuttal, or list of what the study does not do.

Classify each flagged passage before proposing a repair:

| Category | Architecture action |
|:--|:--|
| `unnecessary_disclaimer` | Delete; verify that no evidence boundary is lost |
| `necessary_scope` | Express once as the exact population, setting, comparison, estimand, or evidence class |
| `methodological_limitation` | Place after the affected interpretation or in the consolidated limitations unit |
| `conceptual_contrast` | Retain only when the contrast advances the argument; prefer an affirmative distinction |
| `evidence_qualification` | Keep next to the estimate or inference it qualifies |
| `redundant_clarification` | Consolidate at the first location where the reader needs it |

Record the strongest supported claim before routing prose to `$anti-defensive-writing`. The language pass may delete, consolidate, or convert the flagged wording, but it must not erase genuine uncertainty, adverse evidence, or a design boundary required for valid interpretation.

## Transition as logical handoff

A transition is valid only if it carries at least one of:

1. an unresolved question;
2. a change of analytical level;
3. a newly necessary construct;
4. a validity condition required by the next claim;
5. a completed claim whose consequence motivates the next unit.

Connector words such as “however” and “therefore” are not evidence of a handoff. Test the record by deleting the transition wording: the dependency should remain visible in the inherited premise and outgoing question.

Check each paragraph's opening and ending in context. The opening names a known object or supplies the needed bridge; the remaining sentences complete one job; the ending creates the next reader question without announcing the solution too early. Replace vague “this,” “these,” or “that” with an explicit antecedent when a reference crosses a paragraph or section boundary.

Use explicit logical relations instead of ordinal scaffolding when the argument is cumulative. “First,” “second,” and “third” are acceptable for a true list; they are weak substitutes for explaining why one research problem creates the next. A section title, paragraph opening, or transition must name the domain object precisely enough that a broad term such as “AI,” “validation,” or “performance” cannot refer to several different things.

Keep manuscript prose at the scientific level. Local paths, hashes, run dates, processing receipts, historical work-package codes, and maintenance status belong in internal or reproducibility records unless they change scientific interpretation. Necessary scope belongs once near the claim it governs; repeated statements of what the paper does not do are not structural transitions.
