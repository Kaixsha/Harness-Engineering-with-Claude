from src.budget import (
    build_raw_context,
    estimate_tokens,
    measure_context_budget,
    serialize,
)
from src.evaluation import (
    EVALUATION_QUESTIONS,
    compare_evaluations,
    run_control_evaluation,
    run_full_evaluation,
)


def test_raw_context_contains_case():
    context = build_raw_context()

    assert "case" in context


def test_raw_context_contains_history():
    context = build_raw_context()

    assert "history" in context


def test_raw_context_contains_events():
    context = build_raw_context()

    assert "events" in context


def test_raw_context_contains_raw_notes():
    context = build_raw_context()

    assert "raw_notes" in context


def test_serialize_returns_string():
    text = serialize({"status": "ok"})

    assert isinstance(text, str)


def test_token_estimate_is_positive():
    tokens = estimate_tokens("hello world")

    assert tokens > 0


def test_budget_raw_tokens_are_positive():
    budget = measure_context_budget()

    assert budget["raw_tokens"] > 0


def test_budget_assembled_tokens_are_positive():
    budget = measure_context_budget()

    assert budget["assembled_tokens"] > 0


def test_assembled_context_is_smaller():
    budget = measure_context_budget()

    assert budget["assembled_tokens"] < budget["raw_tokens"]


def test_context_reduction_meets_50_percent_target():
    budget = measure_context_budget()

    assert budget["reduction_percent"] >= 50


def test_budget_reports_target_as_met():
    budget = measure_context_budget()

    assert budget["meets_50_percent_target"] is True


def test_evaluation_contains_six_questions():
    assert len(EVALUATION_QUESTIONS) == 6


def test_full_evaluation_answers_at_least_five_questions():
    result = run_full_evaluation()

    assert result["correct"] >= 5
    assert result["total"] == 6


def test_control_scores_lower_than_full_evaluation():
    full = run_full_evaluation()
    control = run_control_evaluation()

    assert control["correct"] < full["correct"]


def test_case_facts_removal_causes_regression():
    comparison = compare_evaluations()

    assert comparison["has_regression"] is True
    assert len(comparison["regressions"]) >= 1
