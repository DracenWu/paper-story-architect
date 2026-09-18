#!/usr/bin/env python3
"""Validate the structural contract of a paper-story blueprint."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any


REQUIRED_PAPER_STORY_FIELDS = (
    "central_proposition",
    "phenomenon",
    "practical_tension",
    "literature_default_or_partial_answer",
    "unresolved_mechanism_or_intersection",
    "research_questions",
    "method_response",
    "principal_evidence",
    "boundary_evidence",
    "theoretical_or_methodological_reframing",
    "stakeholder_actions",
    "closure_claim",
)
REQUIRED_SECTION_ROLES = (
    "introduction",
    "related_work",
    "methods",
    "results",
    "discussion",
    "conclusion",
)
ROLE_TITLES = dict(zip(REQUIRED_SECTION_ROLES, ("Introduction", "Related Work", "Methods", "Results", "Discussion", "Conclusion")))
SECTION_REQUIRED_FIELDS = (
    "id",
    "name",
    "role",
    "entry_question",
    "inherits_from_previous",
    "establishes",
    "evidence_inputs",
    "prohibited_jobs",
    "must_precede",
    "handoff_to_next",
    "rq_consumers",
)
SECTION_LIST_FIELDS = {"evidence_inputs", "prohibited_jobs", "must_precede", "rq_consumers"}
PARAGRAPH_REQUIRED_FIELDS = (
    "id",
    "section_id",
    "reader_question_received",
    "inherits_from",
    "single_job",
    "evidence_form",
    "citation_obligation",
    "claim_scope",
    "closure_claim",
    "handoff_question",
    "consumed_by",
)
PARAGRAPH_LIST_FIELDS = {"inherits_from", "consumed_by"}
RQ_CHAIN_FIELDS = (
    "problem",
    "gap",
    "consequence",
    "method",
    "result",
    "discussion",
    "conclusion",
)
RQ_CHAIN_ROLE_MAP = {
    "problem": "introduction",
    "consequence": "introduction",
    "gap": "related_work",
    "method": "methods",
    "result": "results",
    "discussion": "discussion",
    "conclusion": "conclusion",
}
REQUIRED_GATES = (
    "reverse-outline",
    "adjacent-swap",
    "deletion",
    "reader-question",
    "claim-return",
    "forward-reference",
    "backward-justification",
    "order-preservation",
    "no-new-branch",
    "version-consistency",
    "evidence-consumer",
)
PLACEHOLDER_RE = re.compile(r"\b(?:TBD|TODO|FIXME|XXX)\b|\(ref\)", re.IGNORECASE)
INHERITANCE_STORY_FIELDS = {
    "central_proposition",
    "phenomenon",
    "practical_tension",
    "literature_default_or_partial_answer",
    "unresolved_mechanism_or_intersection",
    "research_questions",
}


def _value(text: str) -> Any:
    text = text.strip()
    if not text:
        return None
    if text.startswith("[") and text.endswith("]"):
        inside = text[1:-1].strip()
        return [] if not inside else [_value(part) for part in inside.split(",")]
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


def _yaml_lines(source: str) -> list[tuple[int, str]]:
    match = re.search(r"^```ya?ml\s*$\n(.*?)^```\s*$", source, re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError("no fenced YAML block found")
    lines: list[tuple[int, str]] = []
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        lines.append((len(raw) - len(raw.lstrip(" ")), raw.strip()))
    return lines


def _parse_block(lines: list[tuple[int, str]], start: int, indent: int) -> tuple[Any, int]:
    if lines[start][1].startswith("- "):
        return _parse_list(lines, start, indent)
    return _parse_mapping(lines, start, indent)


def _parse_mapping(
    lines: list[tuple[int, str]], start: int, indent: int
) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    index = start
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent < indent or line_indent != indent or content.startswith("- "):
            break
        if ":" not in content:
            raise ValueError(f"invalid mapping entry: {content}")
        key, raw_value = content.split(":", 1)
        index += 1
        if raw_value.strip():
            result[key.strip()] = _value(raw_value)
        elif index < len(lines) and lines[index][0] > line_indent:
            result[key.strip()], index = _parse_block(lines, index, lines[index][0])
        else:
            result[key.strip()] = None
    return result, index


def _parse_list(
    lines: list[tuple[int, str]], start: int, indent: int
) -> tuple[list[Any], int]:
    result: list[Any] = []
    index = start
    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent != indent or not content.startswith("- "):
            break
        item_text = content[2:].strip()
        index += 1
        if ":" in item_text:
            key, raw_value = item_text.split(":", 1)
            item: dict[str, Any] = {key.strip(): _value(raw_value)}
            if index < len(lines) and lines[index][0] > line_indent:
                continuation, index = _parse_mapping(lines, index, lines[index][0])
                item.update(continuation)
            result.append(item)
        else:
            result.append(_value(item_text))
    return result, index


def _is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _is_name(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _error(code: str, message: str) -> str:
    return f"FAIL {code}: {message}"


def validate_blueprint(path: str | Path, depth: str = "deep") -> list[str]:
    """Return structural validation errors for the blueprint at *path*."""
    if depth not in ("standard", "deep"):
        return [_error("INVALID_DEPTH", f"unsupported validation depth {depth}")]
    blueprint_path = Path(path)
    try:
        source = blueprint_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return [_error("READ_ERROR", f"cannot read {blueprint_path}")]
    errors: list[str] = []

    placeholder = PLACEHOLDER_RE.search(source)
    if placeholder:
        errors.append(_error("PLACEHOLDER", f"unresolved placeholder {placeholder.group(0)}"))

    try:
        lines = _yaml_lines(source)
        document, end = _parse_block(lines, 0, lines[0][0])
        if end != len(lines) or not isinstance(document, dict):
            raise ValueError("incomplete YAML parse")
    except (IndexError, ValueError) as exc:
        errors.append(_error("INVALID_YAML", str(exc)))
        return errors

    story = document.get("paper_story")
    if not isinstance(story, dict):
        errors.append(_error("MISSING_PAPER_STORY", "paper_story mapping is required"))
        return errors

    for field in REQUIRED_PAPER_STORY_FIELDS:
        if _is_empty(story.get(field)):
            errors.append(_error("MISSING_FIELD", f"paper_story.{field} is required"))

    sections = story.get("sections")
    if not isinstance(sections, list):
        errors.append(_error("INVALID_SECTION", "sections must be a list"))
        sections = []
    section_roles: list[str] = []
    seen_roles: set[str] = set()
    story_ids: set[str] = set()
    section_ids: set[str] = set()
    section_positions: dict[str, int] = {}
    story_order: dict[str, tuple[int, int]] = {}
    section_role_by_id: dict[str, str] = {}
    section_by_id: dict[str, dict[str, Any]] = {}
    paragraph_owner_by_id: dict[str, str] = {}
    paragraph_ids: set[str] = set()
    paragraph_records: list[tuple[dict[str, Any], str]] = []
    section_records: list[dict[str, Any]] = []
    for index, section in enumerate(sections):
        if not isinstance(section, dict):
            errors.append(_error("INVALID_SECTION", f"section[{index}] must be a mapping"))
            continue
        section_records.append(section)
        section_name = section.get("name")
        if not _is_name(section_name):
            errors.append(_error("INVALID_SECTION", f"section[{index}] name must be a non-empty string"))
        role = section.get("role")
        if _is_name(role) and role in REQUIRED_SECTION_ROLES:
            section_roles.append(role)
            if role in seen_roles:
                errors.append(_error("DUPLICATE_ROLE", f"duplicate section role {role}"))
            else:
                seen_roles.add(role)
        elif "role" in section:
            errors.append(_error("INVALID_SECTION_ROLE", f"section[{index}] has invalid role {role}"))
        section_id = section.get("id")
        if not _is_name(section_id):
            errors.append(_error("INVALID_SECTION", f"section[{index}] id must be a non-empty string"))
        elif section_id in story_ids:
            errors.append(_error("DUPLICATE_ID", f"duplicate id {section_id}"))
        else:
            story_ids.add(section_id)
            section_ids.add(section_id)
            section_positions[section_id] = index
            story_order[section_id] = (index, -1)
            section_by_id[section_id] = section
            if _is_name(role) and role in REQUIRED_SECTION_ROLES:
                section_role_by_id[section_id] = role
        label = section_id if _is_name(section_id) else f"section[{index}]"
        for field in SECTION_REQUIRED_FIELDS:
            if field in SECTION_LIST_FIELDS:
                valid = field in section and isinstance(section[field], list)
                if field == "rq_consumers":
                    valid = valid and bool(section[field])
            else:
                valid = _is_name(section.get(field))
            if not valid:
                errors.append(_error("MISSING_SECTION_FIELD", f"{label}.{field} is required"))
        paragraphs = section.get("paragraphs")
        if paragraphs is None:
            if depth == "deep":
                errors.append(_error("EMPTY_SECTION", f"section {section_name or label} has no paragraphs"))
            continue
        if not isinstance(paragraphs, list):
            errors.append(_error("INVALID_PARAGRAPH", f"section {section_name or label} paragraphs must be a list"))
            continue
        valid_paragraphs = 0
        for paragraph_index, paragraph in enumerate(paragraphs):
            if not isinstance(paragraph, dict):
                errors.append(_error("INVALID_PARAGRAPH", f"section {section_name or label} has invalid paragraph at index {paragraph_index}"))
                continue
            paragraph_id = paragraph.get("id")
            if not _is_name(paragraph_id):
                errors.append(_error("INVALID_PARAGRAPH", f"section {section_name or label} has paragraph with invalid id"))
            else:
                valid_paragraphs += 1
                if paragraph_id in story_ids:
                    errors.append(_error("DUPLICATE_ID", f"duplicate id {paragraph_id}"))
                else:
                    story_ids.add(paragraph_id)
                    paragraph_ids.add(paragraph_id)
                    story_order[paragraph_id] = (index, paragraph_index)
                    if _is_name(section_id):
                        paragraph_owner_by_id[paragraph_id] = section_id
                paragraph_records.append((paragraph, label))
            if depth == "deep":
                paragraph_label = paragraph_id if _is_name(paragraph_id) else f"{label}.paragraph[{paragraph_index}]"
                for field in PARAGRAPH_REQUIRED_FIELDS:
                    if field in PARAGRAPH_LIST_FIELDS:
                        valid = (
                            field in paragraph
                            and isinstance(paragraph[field], list)
                            and bool(paragraph[field])
                        )
                    else:
                        valid = _is_name(paragraph.get(field))
                    if not valid:
                        errors.append(_error("MISSING_PARAGRAPH_FIELD", f"{paragraph_label}.{field} is required"))
            if _is_name(section_id) and paragraph.get("section_id") != section_id:
                errors.append(_error("BROKEN_REFERENCE", f"paragraph {paragraph_id or '<unnamed>'} section_id must equal {section_id}"))
        if depth == "deep" and not valid_paragraphs:
            errors.append(_error("EMPTY_SECTION", f"section {section_name or label} has no valid paragraphs"))
    for role in REQUIRED_SECTION_ROLES:
        if role not in seen_roles:
            errors.append(
                _error(
                    "MISSING_SECTION_ROLE",
                    f"required section role {role} ({ROLE_TITLES[role]}) is missing",
                )
            )
            errors.append(
                _error("MISSING_SECTION", f"required section {ROLE_TITLES[role]} is missing")
            )
    if (
        len(section_roles) == len(REQUIRED_SECTION_ROLES)
        and set(section_roles) == set(REQUIRED_SECTION_ROLES)
        and tuple(section_roles) != REQUIRED_SECTION_ROLES
    ):
        errors.append(_error("BROKEN_ORDER", "section roles are not in canonical order"))

    questions = story.get("research_questions")
    if not isinstance(questions, list):
        errors.append(_error("INVALID_RQ", "research_questions must be a list of mappings"))
        questions = []
    rq_ids: set[str] = set()
    for index, question in enumerate(questions):
        if not isinstance(question, dict):
            errors.append(_error("INVALID_RQ", f"research_questions[{index}] must be a mapping"))
            continue
        rq_id = question.get("id")
        if not _is_name(rq_id):
            errors.append(_error("INVALID_RQ", f"research_questions[{index}] id must be a non-empty string (missing id)"))
        elif rq_id in rq_ids:
            errors.append(_error("DUPLICATE_ID", f"duplicate id {rq_id} in research_questions"))
        else:
            rq_ids.add(rq_id)
        if not _is_name(question.get("question")):
            label = rq_id if _is_name(rq_id) else f"research_questions[{index}]"
            errors.append(_error("MISSING_RQ_FIELD", f"{label}.question is required"))

    chains = story.get("rq_return_chains")
    if not isinstance(chains, list):
        errors.append(_error("BROKEN_RQ_CHAIN", "rq_return_chains must be a list"))
        chains = []
    chain_by_id: dict[str, dict[str, Any]] = {}
    for index, chain in enumerate(chains):
        if not isinstance(chain, dict) or not _is_name(chain.get("id")):
            errors.append(_error("BROKEN_RQ_CHAIN", f"rq_return_chains[{index}] needs a non-empty string id"))
            continue
        chain_id = chain["id"]
        if chain_id in chain_by_id:
            errors.append(_error("DUPLICATE_ID", f"duplicate id {chain_id} chain"))
            continue
        chain_by_id[chain_id] = chain
        missing = tuple(field for field in RQ_CHAIN_FIELDS if not _is_name(chain.get(field)))
        if missing:
            errors.append(_error("BROKEN_RQ_CHAIN", f"{chain_id} is missing {', '.join(missing)}"))
    chain_ids = set(chain_by_id)
    missing_chains = rq_ids - chain_ids
    extra_chains = chain_ids - rq_ids
    if missing_chains or extra_chains:
        details = []
        if missing_chains:
            details.append("missing chains for " + ", ".join(sorted(missing_chains)))
        if extra_chains:
            details.append("chains without questions " + ", ".join(sorted(extra_chains)))
        errors.append(_error("RQ_CHAIN_MISMATCH", "; ".join(details)))

    evidence = story.get("evidence_ledger")
    if not isinstance(evidence, list):
        errors.append(_error("INVALID_EVIDENCE_LEDGER", "evidence_ledger must be a list of mappings"))
        evidence = []
    evidence_ids: set[str] = set()
    evidence_records: list[dict[str, Any]] = []
    if not evidence:
        errors.append(_error("EMPTY_EVIDENCE_LEDGER", "evidence_ledger must not be empty"))
    for index, record in enumerate(evidence):
        if not isinstance(record, dict):
            errors.append(_error("INVALID_EVIDENCE", f"evidence_ledger[{index}] must be a mapping"))
            continue
        evidence_records.append(record)
        record_id = record.get("id")
        if not _is_name(record_id):
            errors.append(_error("INVALID_EVIDENCE", f"evidence_ledger[{index}] id must be a non-empty string"))
        elif record_id in evidence_ids:
            errors.append(_error("DUPLICATE_ID", f"duplicate id {record_id} in evidence_ledger"))
        else:
            evidence_ids.add(record_id)
        label = record_id if _is_name(record_id) else f"evidence_ledger[{index}]"
        for field in ("source", "finding"):
            if not _is_name(record.get(field)):
                errors.append(
                    _error("MISSING_EVIDENCE_FIELD", f"{label}.{field} is required")
                )
        consumers = record.get("consumers")
        if not isinstance(consumers, list) or not consumers:
            errors.append(_error("ORPHAN_EVIDENCE", f"evidence {record_id or '<unnamed>'} has no consumers"))

    principal_evidence = story.get("principal_evidence")
    if not _is_name(principal_evidence) or principal_evidence not in evidence_ids:
        errors.append(
            _error(
                "BROKEN_REFERENCE",
                f"paper_story.principal_evidence references unknown evidence id {principal_evidence}",
            )
        )

    known_consumer_ids = story_ids | rq_ids
    depth_target_ids = section_ids if depth == "standard" else paragraph_ids
    depth_target_kind = "section" if depth == "standard" else "paragraph"
    for record in evidence_records:
        consumers = record.get("consumers")
        if isinstance(consumers, list):
            for consumer in consumers:
                if not _is_name(consumer) or consumer not in depth_target_ids:
                    errors.append(
                        _error(
                            "DEPTH_CONTRACT",
                            f"{depth} evidence consumer {consumer} must be a declared {depth_target_kind} id",
                        )
                    )
                if not _is_name(consumer) or consumer not in known_consumer_ids:
                    errors.append(_error("BROKEN_REFERENCE", f"evidence {record.get('id', '<unnamed>')} has unknown consumer {consumer}"))
    for chain_id, chain in chain_by_id.items():
        for field in RQ_CHAIN_FIELDS:
            target = chain.get(field)
            if not _is_name(target) or target not in depth_target_ids:
                errors.append(
                    _error(
                        "DEPTH_CONTRACT",
                        f"{chain_id}.{field} target {target} must be a declared {depth_target_kind} id at {depth} depth",
                    )
                )
            if _is_name(target) and target not in story_ids:
                errors.append(_error("BROKEN_REFERENCE", f"RQ chain {chain_id}.{field} references unknown id {target}"))
                continue
            if not _is_name(target):
                continue
            owner_section_id = (
                target if target in section_ids else paragraph_owner_by_id.get(target)
            )
            if owner_section_id is None:
                continue
            expected_role = RQ_CHAIN_ROLE_MAP[field]
            actual_role = section_role_by_id.get(owner_section_id)
            if actual_role != expected_role:
                errors.append(
                    _error(
                        "RQ_CHAIN_ROLE",
                        f"{chain_id}.{field} must resolve to {expected_role}, not {actual_role}",
                    )
                )
            rq_consumers = section_by_id.get(owner_section_id, {}).get("rq_consumers")
            if not isinstance(rq_consumers, list) or chain_id not in rq_consumers:
                errors.append(
                    _error(
                        "RQ_CHAIN_CONSUMER",
                        f"{chain_id}.{field} target section {owner_section_id} does not consume {chain_id}",
                    )
                )

    def check_story_reference(owner: str, target: Any) -> None:
        valid = False
        if _is_name(target):
            if target.startswith("paper_story."):
                field = target.split(".", 1)[1]
                valid = bool(field) and field in story
            else:
                valid = target in known_consumer_ids
        if not valid:
            errors.append(_error("BROKEN_REFERENCE", f"{owner} references unknown id {target}"))

    def check_inheritance(owner: str, target: Any) -> None:
        if not _is_name(target):
            return
        if target in rq_ids:
            errors.append(
                _error("BROKEN_INHERITANCE", f"{owner} cannot inherit from RQ id {target}")
            )
        elif target.startswith("paper_story."):
            field = target.split(".", 1)[1]
            if field not in INHERITANCE_STORY_FIELDS or field not in story:
                errors.append(
                    _error(
                        "BROKEN_INHERITANCE",
                        f"{owner} cannot inherit from story field {target}",
                    )
                )

    precedence_graph: dict[str, set[str]] = {story_id: set() for story_id in story_ids}
    for section in section_records:
        owner = section.get("id", "<unnamed section>")
        inherited = section.get("inherits_from_previous")
        check_story_reference(f"section {owner}.inherits_from_previous", inherited)
        check_inheritance(f"section {owner}.inherits_from_previous", inherited)
        if _is_name(owner) and _is_name(inherited) and inherited in story_order:
            precedence_graph[inherited].add(owner)
            if story_order[inherited] >= story_order.get(owner, (-1, -1)):
                errors.append(
                    _error(
                        "BROKEN_ORDER",
                        f"section {owner} inherits from non-upstream id {inherited}",
                    )
                )
        rq_consumers = section.get("rq_consumers")
        if isinstance(rq_consumers, list):
            for rq_consumer in rq_consumers:
                if not _is_name(rq_consumer) or rq_consumer not in rq_ids:
                    errors.append(
                        _error(
                            "BROKEN_REFERENCE",
                            f"section {owner}.rq_consumers references unknown RQ id {rq_consumer}",
                        )
                    )
        for target in section.get("must_precede", []) if isinstance(section.get("must_precede"), list) else []:
            if not _is_name(target) or target not in section_ids:
                errors.append(
                    _error(
                        "BROKEN_REFERENCE",
                        f"section {owner}.must_precede references unknown section id {target}",
                    )
                )
                continue
            if _is_name(owner):
                precedence_graph.setdefault(owner, set()).add(target)
                if target == owner:
                    errors.append(
                        _error(
                            "BROKEN_ORDER",
                            f"section {owner}.must_precede contains a self-reference",
                        )
                    )
                elif section_positions[target] <= section_positions.get(owner, -1):
                    errors.append(
                        _error(
                            "BROKEN_ORDER",
                            f"section {owner} must precede {target}, but the target is not later",
                        )
                    )
        for evidence_id in section.get("evidence_inputs", []) if isinstance(section.get("evidence_inputs"), list) else []:
            if not _is_name(evidence_id) or evidence_id not in evidence_ids:
                errors.append(_error("BROKEN_REFERENCE", f"section {owner}.evidence_inputs references unknown id {evidence_id}"))

    for paragraph, _parent_id in paragraph_records:
        owner = paragraph.get("id", "<unnamed paragraph>")
        for field in ("inherits_from", "consumed_by"):
            values = paragraph.get(field)
            if isinstance(values, list):
                for target in values:
                    check_story_reference(f"paragraph {owner}.{field}", target)
                    if field == "inherits_from":
                        check_inheritance(f"paragraph {owner}.inherits_from", target)
                    if not _is_name(owner) or not _is_name(target):
                        continue
                    if field == "inherits_from" and target in story_order:
                        precedence_graph[target].add(owner)
                        if story_order[target] >= story_order.get(owner, (-1, -1)):
                            errors.append(
                                _error(
                                    "BROKEN_ORDER",
                                    f"paragraph {owner} inherits from non-upstream id {target}",
                                )
                            )
                    elif field == "consumed_by" and target in story_order:
                        precedence_graph[owner].add(target)
                        if story_order[target] <= story_order.get(owner, (-1, -1)):
                            errors.append(
                                _error(
                                    "BROKEN_ORDER",
                                    f"paragraph {owner} is consumed by non-downstream id {target}",
                                )
                            )
                    elif (
                        field == "consumed_by"
                        and target.startswith("paper_story.")
                        and target != "paper_story.closure_claim"
                    ):
                        errors.append(
                            _error(
                                "BROKEN_REFERENCE",
                                f"paragraph {owner}.consumed_by permits only paper_story.closure_claim as a root target",
                            )
                        )

    visit_state: dict[str, int] = {}

    def has_precedence_cycle(node: str) -> bool:
        state = visit_state.get(node, 0)
        if state == 1:
            return True
        if state == 2:
            return False
        visit_state[node] = 1
        if any(has_precedence_cycle(target) for target in precedence_graph.get(node, ())):
            return True
        visit_state[node] = 2
        return False

    if any(has_precedence_cycle(node) for node in precedence_graph):
        errors.append(_error("BROKEN_ORDER", "story dependency cycle detected"))

    gates = story.get("semantic_gates")
    if gates is None:
        gates = []
    elif not isinstance(gates, list):
        errors.append(_error("INVALID_GATE", "semantic_gates must be a list"))
        gates = []
    gate_by_id: dict[str, dict[str, Any]] = {}
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict):
            errors.append(_error("INVALID_GATE", f"semantic_gates[{index}] must be a mapping"))
            continue
        gate_id = gate.get("id")
        if not _is_name(gate_id):
            errors.append(_error("INVALID_GATE", f"semantic_gates[{index}] id must be a non-empty string"))
        elif gate_id in gate_by_id:
            errors.append(_error("DUPLICATE_ID", f"duplicate id {gate_id} in semantic_gates"))
        else:
            gate_by_id[gate_id] = gate
    if depth == "deep":
        for gate_id in REQUIRED_GATES:
            gate = gate_by_id.get(gate_id)
            if gate is None:
                errors.append(_error("MISSING_GATE", f"semantic gate {gate_id} is missing"))
                continue
            verdict = gate.get("verdict")
            if verdict not in ("PASS", "FAIL"):
                errors.append(_error("INVALID_GATE", f"semantic gate {gate_id} needs PASS or FAIL verdict"))
            elif verdict == "FAIL":
                errors.append(_error("FAILED_GATE", f"semantic gate {gate_id} has verdict FAIL"))
            if not _is_name(gate.get("reason")):
                errors.append(_error("INVALID_GATE", f"semantic gate {gate_id} needs a reason"))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", choices=("standard", "deep"), default="deep")
    parser.add_argument("blueprint", help="path to the blueprint Markdown file")
    args = parser.parse_args()
    errors = validate_blueprint(args.blueprint, depth=args.depth)
    if errors:
        print("\n".join(errors))
        return 1
    print("PASS: blueprint structure is complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
