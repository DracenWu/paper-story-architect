# Paper Story Architect

`paper-story-architect` is a Codex skill for designing and auditing the
whole-paper narrative before manuscript drafting. It treats a paper as an
evidence-bounded dependency graph: every research question, section,
paragraph, evidence object, and closing claim must have a defined job and a
traceable downstream consumer.

It is intended for research papers that need a rigorous narrative blueprint,
a cross-section claim-return audit, or a controlled update after an RQ, method,
result, figure, or claim boundary changes.

## What it helps with

- Build a full-manuscript narrative blueprint from Introduction through
  Conclusion.
- Check whether every RQ returns through a method, result, Discussion
  interpretation, and Conclusion closure.
- Audit section order, handoffs, paragraph dependencies, evidence consumers,
  scope discipline, and version consistency.
- Check overall and RQ-level gap/consequence chains, figure and table reading
  order, main-text versus supplement allocation, and Discussion closure.
- For a standard full-length empirical article, plan about 70 unique cited
  references, normally 65--80, and audit their coverage and claim consumers.
- Detect defensive narrative structures, assign each necessary limitation to its
  claim consumer, and create a handoff ledger for sentence-level revision with
  `$anti-defensive-writing`.
- Map the impact of a changed RQ, construct, result, figure, table, or evidence
  boundary before modifying a blueprint.

The skill plans architecture. It does not draft manuscript prose, run
experiments, create results, or expand a paper's scientific claims.

For wording revision, use the accepted claim scopes and defensive-writing
handoff ledger with `$anti-defensive-writing`. Paper Story Architect identifies
where defensive framing breaks the argument; the language skill executes the
sentence-level deletion, consolidation, or positive-scope rewrite while
preserving genuine uncertainty and methodological limits.

## Install

Clone this repository into your local Codex skills directory:

```bash
git clone https://github.com/DracenWu/paper-story-architect.git \
  ~/.codex/skills/paper-story-architect
```

Restart or refresh Codex after installation so it discovers the skill.

## Use it in Codex

Invoke the skill explicitly:

```text
Use $paper-story-architect to build a deep narrative blueprint for this paper.
```

Or make a request that clearly matches one of its three modes:

```text
Audit this manuscript's claim-return chain before language polishing.
```

```text
Update the blueprint because RQ2 and Figure 3 have changed; show the impact map first.
```

### Modes

| Mode | Use when | Output |
|---|---|---|
| `build` | A paper needs a blueprint before drafting. | A whole-paper architecture record after staged confirmation. |
| `audit` | A blueprint or manuscript needs structural review. | Read-only `BLOCKER`, `MAJOR`, and `MINOR` findings with repair outcomes. |
| `update` | An RQ, claim boundary, method, result, table, or figure changes. | An impact map, then confirmed blueprint-only revisions. |

### Depth

| Depth | Use when | Required detail |
|---|---|---|
| `standard` | You need the macro spine and section contracts. | Six functional roles, RQ return chains, and an evidence ledger. |
| `deep` | You are freezing a blueprint, substantially restructuring, or auditing before submission. | Standard records plus paragraph dependencies and eleven semantic-gate verdicts. |

The six functional roles are `introduction`, `related_work`, `methods`,
`results`, `discussion`, and `conclusion`. They are blueprint units rather
than mandatory top-level headings: prior work may sit inside the Introduction
and closure may sit at the end of Discussion when journal practice supports
that presentation. Their functional order remains explicit.

## Build workflow

`build` stops at three confirmation points:

1. Macro story and central proposition.
2. Section-role/order map and RQ claim-return map.
3. Freeze and validation; at `deep`, this also includes paragraph dependencies
   and all eleven semantic gates.

This prevents a polished outline or an early Discussion draft from being
mistaken for an accepted research architecture.

## Validate a blueprint

Completed blueprints use one fenced YAML block. Validate it with the matching
depth:

```bash
python3 scripts/validate_blueprint.py --depth standard path/to/blueprint.md
python3 scripts/validate_blueprint.py --depth deep path/to/blueprint.md
```

The validator checks structural contracts, including role order, RQ return
chains, reference direction, evidence consumers, depth-specific targets, and
the non-empty evidence ledger. At `deep`, it also requires complete paragraph
records and all eleven semantic-gate records. It does not replace scholarly
judgment about methods or evidence validity. Deep builds and manuscript audits
also use the semantic ledgers in `references/manuscript-integrity.md`.

## Repository layout

```text
SKILL.md                         Main routing and operating rules
agents/openai.yaml               Codex display metadata
references/                      Macro-story, section, paragraph, gate, and benchmark guidance
scripts/validate_blueprint.py    Deterministic blueprint validator
tests/                           Validator test suite
```

Run the tests locally with:

```bash
python3 -m unittest discover -s tests -v
```

## Core principle

The paper must make one evidence-bounded story:

```text
phenomenon -> practical tension -> literature gap -> RQ -> method -> evidence
-> interpretation -> knowledge change -> stakeholder action -> bounded closure
```

Section headings, citation density, and polished prose do not establish this
dependency. The blueprint must show it explicitly.
