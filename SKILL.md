---
name: paper-story-architect
description: Use when a research paper needs a full-manuscript narrative blueprint, cross-section claim-return mapping, story-order audit, or repair-impact analysis before drafting or finalization.
---

# Paper Story Architect

Design or audit one evidence-bounded story across six functional section roles. Treat the paper as a dependency graph: each promise, section, paragraph, and evidence object needs a defined role and downstream consumer.

## Select the operation

- `mode=build`: construct a new whole-paper blueprint before drafting.
- `mode=audit`: inspect an existing blueprint or manuscript. Default to read-only; report findings without editing either artifact.
- `mode=update`: respond to a changed RQ, claim boundary, method object, result, figure, or table. Produce an impact map before proposing any blueprint edit.

Use `depth=standard` for the macro spine, section contracts/order, and claim-return chains. Use `depth=deep` for paragraph dependencies and all eleven semantic gates. Default to `standard`; use `deep` for substantial restructuring or pre-submission audit.

## Establish the evidence base

Resolve files from the current workspace; do not assume directory names. Read available evidence in this order:

1. applicable project instructions and README files;
2. user-confirmed idea, contribution boundary, RQs, and target journal;
3. verified literature reports, citation pools, closest-work set, and bibliography;
4. method-audit outputs, technical materials, figure/table plans, and evidence ledgers;
5. the current manuscript or blueprint;
6. supplied benchmarks or benchmark distillation.

Precedence is: verified evidence/project contract > confirmed RQs/contribution boundary > manuscript > benchmarks > defaults. Expose version conflicts. Benchmarks shape form, never scientific scope.

## Route only what the operation needs

Always read [whole-paper-story.md](references/whole-paper-story.md). Read [section-arcs.md](references/section-arcs.md) for building, order audit, or handoffs.

- For `build`: read both files above. At `deep`, add [paragraph-language-citations.md](references/paragraph-language-citations.md) and [audit-gates.md](references/audit-gates.md). Read [benchmark-lessons.md](references/benchmark-lessons.md) only when benchmarks are available or form is disputed.
- For `audit`: read [audit-gates.md](references/audit-gates.md); add [section-arcs.md](references/section-arcs.md) for order/role failures, [paragraph-language-citations.md](references/paragraph-language-citations.md) for paragraph, transition, scope, or citation failures, and [benchmark-lessons.md](references/benchmark-lessons.md) only for benchmark-based judgments.
- For `update`: read [whole-paper-story.md](references/whole-paper-story.md) and the reference governing each impacted unit. Do not load unrelated references.

## Operate with explicit gates

For `build`, stop at exactly three confirmations:

1. macro story and central proposition;
2. section-role/order map and claim-return map;
3. freeze and matching-depth validation; at `deep`, this confirmation also includes paragraph dependencies and all eleven gate verdicts.

Write or overwrite only after the relevant confirmation. For `audit`, return `BLOCKER`, `MAJOR`, and `MINOR` findings with affected IDs, failed gate, evidence, and repair outcome. Editing requires a separate request. For `update`, first map effects across the six canonical roles and evidence ledger; after confirmation, update only the blueprint.

## Preserve boundaries

This skill produces architecture records, not manuscript prose. It does not run experiments, generate scientific results, judge methodological correctness, discover literature, polish language, compile LaTeX, or authorize changes to RQs, evidence status, contribution boundaries, manuscript text, or external systems. Route prose drafting to the appropriate narrative or technical workflow only after the blueprint is accepted. Route wording revision to a polishing workflow.

Deadline pressure or polished prose does not waive the architecture gate. Record limitations as precise positive scope where possible.

## Finish

Run the package validator against the completed blueprint:

```bash
python3 <skill-directory>/scripts/validate_blueprint.py --depth standard <blueprint.md>
python3 <skill-directory>/scripts/validate_blueprint.py --depth deep <blueprint.md>
```

Run exactly one command with the same depth selected for this operation; never validate a `standard` blueprint as `deep` by default. Repair blueprint failures rather than weakening validator expectations. The validator covers structural invariants; at `deep`, record reasoned verdicts for semantic gates. Report the blueprint path, depth, validation result, unresolved blockers, and whether any manuscript files were changed (normally none).
