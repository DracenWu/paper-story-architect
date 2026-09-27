# Manuscript Integrity Records

Use these records for `depth=deep` builds and manuscript-level audits. They turn recurring review failures into explicit evidence for the semantic gates. They are architecture records, not manuscript prose.

## RQ motivation ledger

Record the overall gap, overall consequence, and the bridge to a finite set of problems. Then record for every RQ:

| Field | Required content |
|---|---|
| `central_relation` | How the RQ advances the paper's central proposition |
| `local_gap` | The exact unresolved object supported by closest work |
| `consequence` | The inference, decision, or use that remains unreliable |
| `question` | A genuine unknown, stated without embedding the solution |
| `response_preview` | The broad evidence capability used by this study |
| `method_consumer` | The later Methods unit that operationalizes the response |

The response preview may follow the RQ. Keep it concise and postpone implementation details. Verify that the three local chains form one cumulative argument rather than parallel topics joined only by numbering.

## Figure and table ledger

For every visual, record:

`id | claim_consumer | first_substantive_citation | explanatory_unit | intended_section | destination | evidence_source | rendered_page | placement_verdict`

`destination` is `main`, `supplement`, or `internal`. The main paper retains the minimum display needed to judge a principal claim. The supplement carries detail required for scrutiny but not for following the argument. Internal material includes maintenance records and orphan outputs. When no rendered PDF exists, mark the page and placement verdict as pending rather than guessing.

Check whether dense prose contains a latent table: repeated comparable values, scenarios, model families, sample flows, or decision states. A new table needs a named claim consumer and verified source; compression alone is not a reason to add one.

## Main text and supplement allocation ledger

For every analysis or supporting object, record:

`object | RQ | claim_supported | validity_status | main_summary | supplement_detail | destination_reason | downstream_consumer`

Keep scientifically relevant null, negative, and boundary evidence when it answers an RQ or constrains a claim. Remove or reclassify material that is invalid, unrelated, duplicative, or lacks a downstream consumer. Do not treat an inconvenient result as unrelated. The supplement follows the same evidence rules as the article.

## Terminology and version ledger

Record canonical RQ labels, construct names, state labels, sample names and denominators, evidence classes, and internal aliases. For each item capture:

`canonical_term | aliases_retired | first_use | definition_location | dependent_text_or_visuals | current_source`

Before release, compare the canonical manuscript, supplement, translated reading version, rendered PDFs, README or completion report, checksum list, and anonymous review package. Every artifact must identify the same scientific version. A current PDF paired with stale documentation is a version-consistency failure.

## Defensive-writing handoff ledger

For every passage whose main function is caveat, exclusion, hedge, rebuttal, or scope control, record:

`location | claim_consumer | category | strongest_supported_claim | necessary_boundary | current_function | action | target_workflow`

Use only these categories: `unnecessary_disclaimer`, `necessary_scope`, `methodological_limitation`, `conceptual_contrast`, `evidence_qualification`, and `redundant_clarification`. The action is `delete`, `convert_to_positive_scope`, `consolidate`, `retain`, or `relocate`.

Pass requires all of the following:

1. every retained limitation has a named claim consumer;
2. each boundary appears once at the earliest location needed for valid interpretation, unless a later concise reminder prevents a genuine ambiguity;
3. title, abstract, contribution statements, Results answers, Discussion contributions, and Conclusion lead with supported content rather than disclaimers;
4. narrowing is expressed through an exact subject, predicate, estimand, population, setting, comparison, or evidence class;
5. the accepted ledger is handed to `$anti-defensive-writing` for sentence-level execution after the architecture is approved.

Do not convert a broad claim into an acceptable one by appending a caveat. Narrow the claim itself. Do not delete uncertainty, adverse evidence, or a limitation that changes scientific interpretation.

## Benchmark structure check

Use comparable papers to test section functions and order, preferably from the target journal or the same study type. Verify journal identity and article content before treating a paper as a positive exemplar. Compare:

1. how the Introduction moves from prior work to overall gap, consequence, and RQs;
2. whether literature is integrated into the Introduction or separated as Related Work;
3. how Methods orders data, comparison design, estimands, and diagnostics;
4. whether Results follow research questions, analytical stages, or evidence dependencies;
5. how Discussion returns to prior work, contributions, applications, and boundaries;
6. where summary and detailed tables are placed.

Adopt a pattern only when it improves the present paper's dependency chain. Journal quartile, publication status, or frequent use of a structure does not override the study's evidence order.
