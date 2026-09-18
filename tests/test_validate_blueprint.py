import importlib.util
import re
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SKILL_ROOT / "scripts" / "validate_blueprint.py"


RESULTS_SECTION = """\
    - id: SEC-RESULTS
      name: Results
      role: results
      entry_question: What evidence answers RQ-1?
      inherits_from_previous: P-METHODS-1
      establishes: The mechanism improves diagnostic accuracy.
      evidence_inputs: [EVID-1]
      prohibited_jobs: [introduce_new_method]
      must_precede: [SEC-DISCUSSION]
      handoff_to_next: Interpret why the measured improvement occurs.
      rq_consumers: [RQ-1]
      paragraphs:
        - id: P-RESULTS-1
          section_id: SEC-RESULTS
          reader_question_received: What is the principal result?
          inherits_from: [P-METHODS-1]
          single_job: Report the principal evidence.
          evidence_form: quantitative_result
          citation_obligation: none
          claim_scope: diagnostic accuracy on the evaluated data
          closure_claim: The evidence answers the empirical part of RQ-1.
          handoff_question: Why does the mechanism produce this result?
          consumed_by: [P-DISCUSSION-1]
"""


COMPLETE_BLUEPRINT = (
    """
# Paper Story Blueprint

```yaml
paper_story:
  central_proposition: Explainable mechanisms turn diagnosis into actionable intervention.
  phenomenon: Productivity diagnostics identify symptoms without actionable causes.
  practical_tension: Managers need causal guidance rather than prediction alone.
  literature_default_or_partial_answer: Prior work prioritizes diagnostic accuracy.
  unresolved_mechanism_or_intersection: How explanations connect diagnoses to interventions.
  research_questions:
    - id: RQ-1
      question: How does the proposed mechanism improve productivity diagnosis?
  method_response: Build and evaluate an explanation-linked diagnostic mechanism.
  principal_evidence: EVID-1
  boundary_evidence: The claim is limited to the evaluated data and task.
  theoretical_or_methodological_reframing: Diagnosis is an evidence-to-action chain.
  stakeholder_actions: Managers inspect exposed causes before selecting interventions.
  closure_claim: The mechanism makes accurate diagnoses actionable.

  sections:
    - id: SEC-INTRODUCTION
      name: Introduction
      role: introduction
      entry_question: Why is actionable productivity diagnosis needed?
      inherits_from_previous: paper_story.practical_tension
      establishes: RQ-1
      evidence_inputs: []
      prohibited_jobs: [report_results]
      must_precede: [SEC-RELATED-WORK]
      handoff_to_next: Identify the unresolved literature gap.
      rq_consumers: [RQ-1]
      paragraphs:
        - id: P-INTRODUCTION-1
          section_id: SEC-INTRODUCTION
          reader_question_received: What practical problem motivates the study?
          inherits_from: [paper_story.practical_tension]
          single_job: Establish the practical problem and its consequence.
          evidence_form: motivating_observation
          citation_obligation: support the practical problem
          claim_scope: productivity diagnosis decisions
          closure_claim: Prediction without causes cannot guide intervention.
          handoff_question: What has prior literature left unresolved?
          consumed_by: [P-RELATED-WORK-1]

    - id: SEC-RELATED-WORK
      name: Related Work
      role: related_work
      entry_question: What mechanism remains unresolved in prior work?
      inherits_from_previous: P-INTRODUCTION-1
      establishes: The explanation-to-intervention gap.
      evidence_inputs: []
      prohibited_jobs: [answer_RQ]
      must_precede: [SEC-METHODS]
      handoff_to_next: Specify the capability required to close the gap.
      rq_consumers: [RQ-1]
      paragraphs:
        - id: P-RELATED-WORK-1
          section_id: SEC-RELATED-WORK
          reader_question_received: Why do existing approaches not solve the problem?
          inherits_from: [P-INTRODUCTION-1]
          single_job: Establish the literature gap.
          evidence_form: literature_synthesis
          citation_obligation: compare closest work
          claim_scope: explanation-enabled productivity diagnosis
          closure_claim: Existing explanations do not identify intervention targets.
          handoff_question: What method capability can close this gap?
          consumed_by: [P-METHODS-1]

    - id: SEC-METHODS
      name: Methods
      role: methods
      entry_question: How is RQ-1 translated into an executable method?
      inherits_from_previous: P-RELATED-WORK-1
      establishes: The explanation-linked diagnostic mechanism.
      evidence_inputs: []
      prohibited_jobs: [interpret_results]
      must_precede: [SEC-RESULTS]
      handoff_to_next: Test the mechanism against the empirical requirement.
      rq_consumers: [RQ-1]
      paragraphs:
        - id: P-METHODS-1
          section_id: SEC-METHODS
          reader_question_received: What capability operationalizes RQ-1?
          inherits_from: [P-RELATED-WORK-1]
          single_job: Define the mechanism and evaluation procedure.
          evidence_form: method_specification
          citation_obligation: justify methodological choices
          claim_scope: the evaluated diagnostic task
          closure_claim: The method exposes actionable causes for each diagnosis.
          handoff_question: Does the mechanism improve diagnostic performance?
          consumed_by: [P-RESULTS-1]

"""
    + RESULTS_SECTION
    + """

    - id: SEC-DISCUSSION
      name: Discussion
      role: discussion
      entry_question: Why does the result answer RQ-1?
      inherits_from_previous: P-RESULTS-1
      establishes: The mechanism-to-outcome interpretation.
      evidence_inputs: [EVID-1]
      prohibited_jobs: [introduce_new_primary_evidence]
      must_precede: [SEC-CONCLUSION]
      handoff_to_next: Close the original practical and literature commitments.
      rq_consumers: [RQ-1]
      paragraphs:
        - id: P-DISCUSSION-1
          section_id: SEC-DISCUSSION
          reader_question_received: What mechanism explains the principal result?
          inherits_from: [P-RESULTS-1]
          single_job: Interpret the result and delimit the claim.
          evidence_form: evidence_bounded_interpretation
          citation_obligation: place the answer in literature dialogue
          claim_scope: explanation-linked diagnosis under evaluated conditions
          closure_claim: Exposed causes connect diagnostic accuracy to actionability.
          handoff_question: What supported answer should the paper retain?
          consumed_by: [P-CONCLUSION-1]

    - id: SEC-CONCLUSION
      name: Conclusion
      role: conclusion
      entry_question: What supported answer closes RQ-1?
      inherits_from_previous: P-DISCUSSION-1
      establishes: The final evidence-bounded answer.
      evidence_inputs: [EVID-1]
      prohibited_jobs: [introduce_new_branch]
      must_precede: []
      handoff_to_next: none
      rq_consumers: [RQ-1]
      paragraphs:
        - id: P-CONCLUSION-1
          section_id: SEC-CONCLUSION
          reader_question_received: What is the final answer to RQ-1?
          inherits_from: [P-DISCUSSION-1]
          single_job: Close the RQ without adding new evidence.
          evidence_form: supported_synthesis
          citation_obligation: none
          claim_scope: evaluated productivity diagnosis setting
          closure_claim: Explanation-linked diagnosis is both accurate and actionable.
          handoff_question: none
          consumed_by: [paper_story.closure_claim]

  rq_return_chains:
    - id: RQ-1
      problem: P-INTRODUCTION-1
      gap: P-RELATED-WORK-1
      consequence: P-INTRODUCTION-1
      method: P-METHODS-1
      result: P-RESULTS-1
      discussion: P-DISCUSSION-1
      conclusion: P-CONCLUSION-1

  evidence_ledger:
    - id: EVID-1
      source: results/table-1
      finding: The proposed mechanism improves diagnostic accuracy over the baseline.
      consumers: [P-RESULTS-1, P-DISCUSSION-1, P-CONCLUSION-1]

  semantic_gates:
    - id: reverse-outline
      verdict: PASS
      reason: Every paragraph has one dominant job and a downstream consumer.
    - id: adjacent-swap
      verdict: PASS
      reason: Swapping adjacent sections breaks an explicit dependency.
    - id: deletion
      verdict: PASS
      reason: Deleting any section leaves a named commitment unresolved.
    - id: reader-question
      verdict: PASS
      reason: Every section answers its declared entry question.
    - id: claim-return
      verdict: PASS
      reason: RQ-1 returns through method, evidence, interpretation, and closure.
    - id: forward-reference
      verdict: PASS
      reason: No section depends on a concept introduced later.
    - id: backward-justification
      verdict: PASS
      reason: Every method and claim traces to an earlier need.
    - id: order-preservation
      verdict: PASS
      reason: The RQ order is preserved through the complete return chain.
    - id: no-new-branch
      verdict: PASS
      reason: Discussion and Conclusion introduce no unsupported branch.
    - id: version-consistency
      verdict: PASS
      reason: Identifiers and claims refer to one consistent blueprint version.
    - id: evidence-consumer
      verdict: PASS
      reason: Every evidence record names at least one paragraph consumer.
```
"""
)


def make_standard_blueprint():
    blueprint = re.sub(
        r"\n      paragraphs:\n(?:(?:        |          ).*\n)+",
        "\n",
        COMPLETE_BLUEPRINT,
    )
    replacements = {
        "problem: P-INTRODUCTION-1": "problem: SEC-INTRODUCTION",
        "gap: P-RELATED-WORK-1": "gap: SEC-RELATED-WORK",
        "consequence: P-INTRODUCTION-1": "consequence: SEC-INTRODUCTION",
        "method: P-METHODS-1": "method: SEC-METHODS",
        "result: P-RESULTS-1": "result: SEC-RESULTS",
        "discussion: P-DISCUSSION-1": "discussion: SEC-DISCUSSION",
        "conclusion: P-CONCLUSION-1": "conclusion: SEC-CONCLUSION",
        "inherits_from_previous: P-INTRODUCTION-1": "inherits_from_previous: SEC-INTRODUCTION",
        "inherits_from_previous: P-RELATED-WORK-1": "inherits_from_previous: SEC-RELATED-WORK",
        "inherits_from_previous: P-METHODS-1": "inherits_from_previous: SEC-METHODS",
        "inherits_from_previous: P-RESULTS-1": "inherits_from_previous: SEC-RESULTS",
        "inherits_from_previous: P-DISCUSSION-1": "inherits_from_previous: SEC-DISCUSSION",
        "consumers: [P-RESULTS-1, P-DISCUSSION-1, P-CONCLUSION-1]": (
            "consumers: [SEC-RESULTS, SEC-DISCUSSION, SEC-CONCLUSION]"
        ),
    }
    for old, new in replacements.items():
        blueprint = blueprint.replace(old, new, 1)
    gate_start = blueprint.index("\n  semantic_gates:\n")
    gate_end = blueprint.index("```", gate_start)
    return blueprint[:gate_start] + "\n" + blueprint[gate_end:]


def load_validator_module():
    """Load the future validator by file path, independent of package layout."""
    spec = importlib.util.spec_from_file_location(
        "paper_story_architect_validate_blueprint", VALIDATOR_PATH
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load validator from {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BlueprintValidatorTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator_module()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def write_blueprint(self, content):
        path = Path(self.temp_dir.name) / "blueprint.md"
        path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
        return path

    def assert_rejected_with(self, content, code, target):
        errors = self.validator.validate_blueprint(self.write_blueprint(content))
        prefix = f"FAIL {code}: "
        matching_errors = [
            str(error)
            for error in errors
            if str(error).startswith(prefix) and target in str(error)
        ]
        self.assertTrue(
            matching_errors,
            f"expected one error containing both {prefix!r} and {target!r}; got {errors!r}",
        )

    def assert_rejected_with_depth(self, content, depth, code, target):
        errors = self.validator.validate_blueprint(
            self.write_blueprint(content), depth=depth
        )
        prefix = f"FAIL {code}: "
        matching_errors = [
            str(error)
            for error in errors
            if str(error).startswith(prefix) and target in str(error)
        ]
        self.assertTrue(
            matching_errors,
            f"expected one error containing both {prefix!r} and {target!r}; got {errors!r}",
        )

    def test_accepts_complete_blueprint(self):
        errors = self.validator.validate_blueprint(
            self.write_blueprint(COMPLETE_BLUEPRINT)
        )
        self.assertEqual([], errors)

    def test_rejects_missing_required_section(self):
        incomplete = COMPLETE_BLUEPRINT.replace(RESULTS_SECTION, "", 1)
        self.assert_rejected_with(incomplete, "MISSING_SECTION", "Results")

    def test_rejects_unresolved_placeholder(self):
        unresolved = COMPLETE_BLUEPRINT.replace(
            "The mechanism makes accurate diagnoses actionable.",
            "TODO define the closure claim",
            1,
        )
        self.assert_rejected_with(unresolved, "PLACEHOLDER", "TODO")

    def test_rejects_duplicate_record_id(self):
        duplicate = COMPLETE_BLUEPRINT.replace(
            "id: P-RESULTS-1", "id: P-METHODS-1", 1
        )
        self.assert_rejected_with(duplicate, "DUPLICATE_ID", "P-METHODS-1")

    def test_rejects_orphan_evidence(self):
        orphaned = COMPLETE_BLUEPRINT.replace(
            "consumers: [P-RESULTS-1, P-DISCUSSION-1, P-CONCLUSION-1]",
            "consumers: []",
            1,
        )
        self.assert_rejected_with(orphaned, "ORPHAN_EVIDENCE", "EVID-1")

    def test_rejects_broken_rq_return_chain(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "      discussion: P-DISCUSSION-1\n", "", 1
        )
        self.assert_rejected_with(broken, "BROKEN_RQ_CHAIN", "RQ-1")

    def test_rejects_section_with_only_malformed_paragraph(self):
        start = COMPLETE_BLUEPRINT.index("      paragraphs:\n        - id: P-INTRODUCTION-1\n")
        end = COMPLETE_BLUEPRINT.index("\n\n    - id: SEC-RELATED-WORK", start)
        malformed = (
            COMPLETE_BLUEPRINT[:start]
            + "      paragraphs:\n        - malformed_scalar"
            + COMPLETE_BLUEPRINT[end:]
        )
        self.assert_rejected_with(malformed, "INVALID_PARAGRAPH", "Introduction")

    def test_rejects_malformed_research_question(self):
        malformed = COMPLETE_BLUEPRINT.replace(
            "    - id: RQ-1\n"
            "      question: How does the proposed mechanism improve productivity diagnosis?",
            "    - malformed_scalar",
            1,
        )
        self.assert_rejected_with(
            malformed, "INVALID_RQ", "research_questions[0]"
        )

    def test_rejects_research_question_without_id(self):
        missing_id = COMPLETE_BLUEPRINT.replace("    - id: RQ-1\n", "    - question: RQ text\n", 1)
        self.assert_rejected_with(missing_id, "INVALID_RQ", "missing id")

    def test_rejects_non_list_evidence_ledger(self):
        start = COMPLETE_BLUEPRINT.index("  evidence_ledger:\n")
        end = COMPLETE_BLUEPRINT.index("\n  semantic_gates:", start)
        malformed = (
            COMPLETE_BLUEPRINT[:start]
            + "  evidence_ledger: malformed_mapping\n"
            + COMPLETE_BLUEPRINT[end:]
        )
        self.assert_rejected_with(
            malformed, "INVALID_EVIDENCE_LEDGER", "list of mappings"
        )

    def test_rejects_malformed_evidence_item(self):
        start = COMPLETE_BLUEPRINT.index("  evidence_ledger:\n")
        end = COMPLETE_BLUEPRINT.index("\n  semantic_gates:", start)
        malformed = (
            COMPLETE_BLUEPRINT[:start]
            + "  evidence_ledger:\n    - malformed_scalar\n"
            + COMPLETE_BLUEPRINT[end:]
        )
        self.assert_rejected_with(
            malformed, "INVALID_EVIDENCE", "evidence_ledger[0]"
        )

    def test_returns_read_error_for_missing_path(self):
        missing = Path(self.temp_dir.name) / "missing.md"
        errors = self.validator.validate_blueprint(missing)
        self.assertEqual([f"FAIL READ_ERROR: cannot read {missing}"], errors)

    def test_cli_reports_read_error_without_traceback(self):
        missing = Path(self.temp_dir.name) / "missing.md"
        result = subprocess.run(
            ["python3", str(VALIDATOR_PATH), str(missing)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertEqual(f"FAIL READ_ERROR: cannot read {missing}\n", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_rejects_list_valued_section_name_without_type_error(self):
        malformed = COMPLETE_BLUEPRINT.replace("      name: Results\n", "      name: [Results]\n", 1)
        self.assert_rejected_with(malformed, "INVALID_SECTION", "section[3]")

    def test_cli_rejects_list_valued_paragraph_id_without_traceback(self):
        malformed = COMPLETE_BLUEPRINT.replace(
            "        - id: P-RESULTS-1\n", "        - id: [P-RESULTS-1]\n", 1
        )
        path = self.write_blueprint(malformed)
        result = subprocess.run(
            ["python3", str(VALIDATOR_PATH), str(path)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("FAIL INVALID_PARAGRAPH:", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_standard_accepts_complete_sections_without_paragraphs_or_gates(self):
        errors = self.validator.validate_blueprint(
            self.write_blueprint(make_standard_blueprint()), depth="standard"
        )
        self.assertEqual([], errors)

    def test_deep_rejects_blueprint_without_paragraphs_or_gates(self):
        errors = self.validator.validate_blueprint(
            self.write_blueprint(make_standard_blueprint()), depth="deep"
        )
        self.assertTrue(any(error.startswith("FAIL EMPTY_SECTION:") for error in errors))
        self.assertTrue(any(error.startswith("FAIL MISSING_GATE:") for error in errors))

    def test_cli_depth_standard_passes_and_default_deep_fails(self):
        path = self.write_blueprint(make_standard_blueprint())
        standard = subprocess.run(
            ["python3", str(VALIDATOR_PATH), "--depth", "standard", str(path)],
            text=True,
            capture_output=True,
            check=False,
        )
        deep = subprocess.run(
            ["python3", str(VALIDATOR_PATH), str(path)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, standard.returncode)
        self.assertEqual("PASS: blueprint structure is complete\n", standard.stdout)
        self.assertEqual(1, deep.returncode)
        self.assertIn("FAIL EMPTY_SECTION:", deep.stdout)
        self.assertNotIn("Traceback", standard.stderr + deep.stderr)

    def test_rejects_section_missing_required_field(self):
        missing = COMPLETE_BLUEPRINT.replace(
            "      entry_question: What evidence answers RQ-1?\n", "", 1
        )
        self.assert_rejected_with(
            missing, "MISSING_SECTION_FIELD", "SEC-RESULTS.entry_question"
        )

    def test_rejects_paragraph_missing_required_field(self):
        missing = COMPLETE_BLUEPRINT.replace(
            "          single_job: Report the principal evidence.\n", "", 1
        )
        self.assert_rejected_with(
            missing, "MISSING_PARAGRAPH_FIELD", "P-RESULTS-1.single_job"
        )

    def test_rejects_unknown_evidence_consumer(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "consumers: [P-RESULTS-1, P-DISCUSSION-1, P-CONCLUSION-1]",
            "consumers: [P-NOT-FOUND]",
            1,
        )
        self.assert_rejected_with(broken, "BROKEN_REFERENCE", "P-NOT-FOUND")

    def test_rejects_unknown_rq_chain_result(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "      result: P-RESULTS-1\n", "      result: P-NOT-FOUND\n", 1
        )
        self.assert_rejected_with(broken, "BROKEN_REFERENCE", "P-NOT-FOUND")

    def test_rejects_duplicate_collection_ids(self):
        rq_item = (
            "    - id: RQ-1\n"
            "      question: How does the proposed mechanism improve productivity diagnosis?\n"
        )
        chain_start = COMPLETE_BLUEPRINT.index("    - id: RQ-1\n", COMPLETE_BLUEPRINT.index("  rq_return_chains:"))
        chain_end = COMPLETE_BLUEPRINT.index("\n\n  evidence_ledger:", chain_start)
        chain_item = COMPLETE_BLUEPRINT[chain_start:chain_end]
        evidence_start = COMPLETE_BLUEPRINT.index("    - id: EVID-1\n")
        evidence_end = COMPLETE_BLUEPRINT.index("\n\n  semantic_gates:", evidence_start)
        evidence_item = COMPLETE_BLUEPRINT[evidence_start:evidence_end]
        gate_item = (
            "    - id: reverse-outline\n"
            "      verdict: PASS\n"
            "      reason: Every paragraph has one dominant job and a downstream consumer.\n"
        )
        cases = {
            "RQ-1": COMPLETE_BLUEPRINT.replace(rq_item, rq_item + rq_item, 1),
            "RQ-1 chain": COMPLETE_BLUEPRINT[:chain_end] + "\n" + chain_item + COMPLETE_BLUEPRINT[chain_end:],
            "EVID-1": COMPLETE_BLUEPRINT[:evidence_end] + "\n" + evidence_item + COMPLETE_BLUEPRINT[evidence_end:],
            "reverse-outline": COMPLETE_BLUEPRINT.replace(gate_item, gate_item + gate_item, 1),
        }
        for target, blueprint in cases.items():
            with self.subTest(target=target):
                self.assert_rejected_with(blueprint, "DUPLICATE_ID", target)

    def test_rejects_rq_and_chain_id_set_mismatch(self):
        mismatch = COMPLETE_BLUEPRINT.replace(
            "  rq_return_chains:\n    - id: RQ-1\n",
            "  rq_return_chains:\n    - id: RQ-2\n",
            1,
        )
        self.assert_rejected_with(mismatch, "RQ_CHAIN_MISMATCH", "RQ-1")

    def test_rejects_research_question_without_question_text(self):
        missing = COMPLETE_BLUEPRINT.replace(
            "      question: How does the proposed mechanism improve productivity diagnosis?\n",
            "",
            1,
        )
        self.assert_rejected_with(
            missing, "MISSING_RQ_FIELD", "RQ-1.question"
        )

    def test_rejects_evidence_missing_source_or_finding(self):
        cases = {
            "EVID-1.source": COMPLETE_BLUEPRINT.replace(
                "      source: results/table-1\n", "", 1
            ),
            "EVID-1.finding": COMPLETE_BLUEPRINT.replace(
                "      finding: The proposed mechanism improves diagnostic accuracy over the baseline.\n",
                "",
                1,
            ),
        }
        for target, blueprint in cases.items():
            with self.subTest(target=target):
                self.assert_rejected_with(
                    blueprint, "MISSING_EVIDENCE_FIELD", target
                )

    def test_rejects_semantically_invalid_references_without_known_prefix(self):
        cases = {
            "GHOST must_precede": COMPLETE_BLUEPRINT.replace(
                "      must_precede: [SEC-RESULTS]\n",
                "      must_precede: [GHOST]\n",
                1,
            ),
            "INTRO-P99 rq consumer": COMPLETE_BLUEPRINT.replace(
                "      rq_consumers: [RQ-1]\n",
                "      rq_consumers: [INTRO-P99]\n",
                1,
            ),
            "GHOST inherits": COMPLETE_BLUEPRINT.replace(
                "      inherits_from_previous: P-INTRODUCTION-1\n",
                "      inherits_from_previous: GHOST\n",
                1,
            ),
            "INTRO-P99 paragraph inherits": COMPLETE_BLUEPRINT.replace(
                "          inherits_from: [P-INTRODUCTION-1]\n",
                "          inherits_from: [INTRO-P99]\n",
                1,
            ),
            "GHOST consumed_by": COMPLETE_BLUEPRINT.replace(
                "          consumed_by: [P-RESULTS-1]\n",
                "          consumed_by: [GHOST]\n",
                1,
            ),
            "GHOST evidence input": COMPLETE_BLUEPRINT.replace(
                "      evidence_inputs: [EVID-1]\n",
                "      evidence_inputs: [GHOST]\n",
                1,
            ),
            "paper_story.ghost": COMPLETE_BLUEPRINT.replace(
                "      inherits_from_previous: paper_story.practical_tension\n",
                "      inherits_from_previous: paper_story.ghost\n",
                1,
            ),
        }
        for target, blueprint in cases.items():
            with self.subTest(target=target):
                self.assert_rejected_with(blueprint, "BROKEN_REFERENCE", target.split()[0])

    def test_accepts_multiple_rq_consumers(self):
        rq_block = (
            "    - id: RQ-1\n"
            "      question: How does the proposed mechanism improve productivity diagnosis?\n"
        )
        rq2_block = (
            "    - id: RQ-2\n"
            "      question: How does the mechanism support intervention decisions?\n"
        )
        chain_start = COMPLETE_BLUEPRINT.index(
            "    - id: RQ-1\n", COMPLETE_BLUEPRINT.index("  rq_return_chains:")
        )
        chain_end = COMPLETE_BLUEPRINT.index("\n\n  evidence_ledger:", chain_start)
        chain2 = COMPLETE_BLUEPRINT[chain_start:chain_end].replace(
            "    - id: RQ-1\n", "    - id: RQ-2\n", 1
        )
        blueprint = COMPLETE_BLUEPRINT.replace(rq_block, rq_block + rq2_block, 1)
        evidence_marker = blueprint.index("\n\n  evidence_ledger:")
        blueprint = blueprint[:evidence_marker] + "\n" + chain2 + blueprint[evidence_marker:]
        blueprint = blueprint.replace("rq_consumers: [RQ-1]", "rq_consumers: [RQ-1, RQ-2]")
        self.assertEqual([], self.validator.validate_blueprint(self.write_blueprint(blueprint)))

    def test_accepts_free_section_name_when_role_is_canonical(self):
        renamed = COMPLETE_BLUEPRINT.replace("      name: Results\n", "      name: Empirical Findings\n", 1)
        self.assertEqual([], self.validator.validate_blueprint(self.write_blueprint(renamed)))

    def test_rejects_missing_section_role(self):
        missing = COMPLETE_BLUEPRINT.replace("      role: results\n", "", 1)
        self.assert_rejected_with(missing, "MISSING_SECTION_FIELD", "SEC-RESULTS.role")

    def test_rejects_duplicate_and_missing_required_role(self):
        duplicate = COMPLETE_BLUEPRINT.replace("      role: results\n", "      role: methods\n", 1)
        self.assert_rejected_with(duplicate, "DUPLICATE_ROLE", "methods")
        self.assert_rejected_with(duplicate, "MISSING_SECTION_ROLE", "results")

    def test_rejects_empty_deep_paragraph_dependencies(self):
        cases = {
            "P-RESULTS-1.inherits_from": COMPLETE_BLUEPRINT.replace(
                "          inherits_from: [P-METHODS-1]\n",
                "          inherits_from: []\n",
                1,
            ),
            "P-RESULTS-1.consumed_by": COMPLETE_BLUEPRINT.replace(
                "          consumed_by: [P-DISCUSSION-1]\n",
                "          consumed_by: []\n",
                1,
            ),
        }
        for target, blueprint in cases.items():
            with self.subTest(target=target):
                self.assert_rejected_with(
                    blueprint, "MISSING_PARAGRAPH_FIELD", target
                )

    def test_rejects_self_must_precede(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "      must_precede: [SEC-DISCUSSION]\n",
            "      must_precede: [SEC-RESULTS]\n",
            1,
        )
        self.assert_rejected_with(broken, "BROKEN_ORDER", "self-reference")

    def test_rejects_must_precede_target_that_is_already_earlier(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "      must_precede: [SEC-DISCUSSION]\n",
            "      must_precede: [SEC-METHODS]\n",
            1,
        )
        self.assert_rejected_with(broken, "BROKEN_ORDER", "SEC-METHODS")

    def test_rejects_must_precede_cycle(self):
        cyclic = COMPLETE_BLUEPRINT.replace(
            "      must_precede: [SEC-CONCLUSION]\n",
            "      must_precede: [SEC-RESULTS]\n",
            1,
        )
        self.assert_rejected_with(cyclic, "BROKEN_ORDER", "cycle")

    def test_rejects_noncanonical_role_order(self):
        swapped = COMPLETE_BLUEPRINT.replace("      role: methods\n", "      role: TEMP\n", 1)
        swapped = swapped.replace("      role: results\n", "      role: methods\n", 1)
        swapped = swapped.replace("      role: TEMP\n", "      role: results\n", 1)
        self.assert_rejected_with(swapped, "BROKEN_ORDER", "canonical")

    def test_rejects_rq_chain_target_in_wrong_section_role(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "      result: P-RESULTS-1\n", "      result: P-METHODS-1\n", 1
        )
        self.assert_rejected_with(broken, "RQ_CHAIN_ROLE", "RQ-1.result")

    def test_rejects_rq_chain_target_section_missing_consumer(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "    - id: SEC-RESULTS\n"
            "      name: Results\n"
            "      role: results\n",
            "    - id: SEC-RESULTS\n"
            "      name: Results\n"
            "      role: results\n",
            1,
        ).replace(
            "      rq_consumers: [RQ-1]\n",
            "      rq_consumers: []\n",
            4,
        )
        self.assert_rejected_with(broken, "RQ_CHAIN_CONSUMER", "RQ-1.result")

    def test_rejects_results_paragraph_inheriting_from_conclusion(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "          inherits_from: [P-METHODS-1]\n",
            "          inherits_from: [P-CONCLUSION-1]\n",
            1,
        )
        self.assert_rejected_with(broken, "BROKEN_ORDER", "P-CONCLUSION-1")

    def test_rejects_paragraph_consuming_backward_to_methods(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "          consumed_by: [P-DISCUSSION-1]\n",
            "          consumed_by: [P-METHODS-1]\n",
            1,
        )
        self.assert_rejected_with(broken, "BROKEN_ORDER", "P-METHODS-1")

    def test_rejects_section_forward_inheritance(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "      inherits_from_previous: paper_story.practical_tension\n",
            "      inherits_from_previous: SEC-RESULTS\n",
            1,
        )
        self.assert_rejected_with(broken, "BROKEN_ORDER", "SEC-RESULTS")

    def test_rejects_empty_evidence_ledger_even_with_empty_inputs(self):
        start = COMPLETE_BLUEPRINT.index("  evidence_ledger:\n")
        end = COMPLETE_BLUEPRINT.index("\n  semantic_gates:", start)
        broken = (
            COMPLETE_BLUEPRINT[:start]
            + "  evidence_ledger: []\n"
            + COMPLETE_BLUEPRINT[end:]
        ).replace("evidence_inputs: [EVID-1]", "evidence_inputs: []")
        self.assert_rejected_with(
            broken, "EMPTY_EVIDENCE_LEDGER", "evidence_ledger"
        )

    def test_rejects_unknown_principal_evidence(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "  principal_evidence: EVID-1\n",
            "  principal_evidence: EVID-NOT-FOUND\n",
            1,
        )
        self.assert_rejected_with(
            broken, "BROKEN_REFERENCE", "EVID-NOT-FOUND"
        )

    def test_rejects_section_inheriting_from_rq_id(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "      inherits_from_previous: paper_story.practical_tension\n",
            "      inherits_from_previous: RQ-1\n",
            1,
        )
        self.assert_rejected_with(broken, "BROKEN_INHERITANCE", "RQ-1")

    def test_rejects_paragraph_inheriting_from_rq_id(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "          inherits_from: [P-METHODS-1]\n",
            "          inherits_from: [RQ-1]\n",
            1,
        )
        self.assert_rejected_with(broken, "BROKEN_INHERITANCE", "RQ-1")

    def test_rejects_section_inheriting_from_terminal_story_field(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "      inherits_from_previous: paper_story.practical_tension\n",
            "      inherits_from_previous: paper_story.closure_claim\n",
            1,
        )
        self.assert_rejected_with(
            broken, "BROKEN_INHERITANCE", "paper_story.closure_claim"
        )

    def test_rejects_paragraph_inheriting_from_later_story_field(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "          inherits_from: [P-METHODS-1]\n",
            "          inherits_from: [paper_story.method_response]\n",
            1,
        )
        self.assert_rejected_with(
            broken, "BROKEN_INHERITANCE", "paper_story.method_response"
        )

    def test_accepts_inheritance_from_allowed_story_root_list_field(self):
        allowed = COMPLETE_BLUEPRINT.replace(
            "          inherits_from: [P-METHODS-1]\n",
            "          inherits_from: [paper_story.research_questions]\n",
            1,
        )
        self.assertEqual([], self.validator.validate_blueprint(self.write_blueprint(allowed)))

    def test_standard_rejects_paragraph_level_rq_chain_target(self):
        self.assert_rejected_with_depth(
            COMPLETE_BLUEPRINT,
            "standard",
            "DEPTH_CONTRACT",
            "RQ-1.result",
        )

    def test_deep_rejects_section_level_rq_chain_target(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "      result: P-RESULTS-1\n", "      result: SEC-RESULTS\n", 1
        )
        self.assert_rejected_with_depth(
            broken, "deep", "DEPTH_CONTRACT", "RQ-1.result"
        )

    def test_standard_rejects_paragraph_level_evidence_consumer(self):
        self.assert_rejected_with_depth(
            COMPLETE_BLUEPRINT,
            "standard",
            "DEPTH_CONTRACT",
            "P-RESULTS-1",
        )

    def test_deep_rejects_section_level_evidence_consumer(self):
        broken = COMPLETE_BLUEPRINT.replace(
            "consumers: [P-RESULTS-1, P-DISCUSSION-1, P-CONCLUSION-1]",
            "consumers: [SEC-RESULTS, SEC-DISCUSSION, SEC-CONCLUSION]",
            1,
        )
        self.assert_rejected_with_depth(
            broken, "deep", "DEPTH_CONTRACT", "SEC-RESULTS"
        )


if __name__ == "__main__":
    unittest.main()
