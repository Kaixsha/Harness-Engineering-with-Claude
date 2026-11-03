"""Evaluate whether assembled context preserves answerability."""

from src.context_builder import (
    assemble_context,
    assemble_control_context,
)
from src.sample_data import CASE, EVENTS, HISTORY


EVALUATION_QUESTIONS = [
    {
        "id": "Q1",
        "question": "What is the case ID?",
        "field": "case_id",
        "expected": "CASE-2048",
    },
    {
        "id": "Q2",
        "question": "Which customer is affected?",
        "field": "customer",
        "expected": "Northwind Retail",
    },
    {
        "id": "Q3",
        "question": "Which product is affected?",
        "field": "product",
        "expected": "Cloud Inventory API",
    },
    {
        "id": "Q4",
        "question": "What is the severity?",
        "field": "severity",
        "expected": "high",
    },
    {
        "id": "Q5",
        "question": "What is the current status?",
        "field": "status",
        "expected": "investigating",
    },
    {
        "id": "Q6",
        "question": "What is the current issue?",
        "field": "current_issue",
        "expected": (
            "Inventory synchronization requests are timing out."
        ),
    },
]


def answer_question(context, question):
    """Answer one evaluation question using only supplied context."""
    case_facts = context.get("case_facts", {})
    field = question["field"]

    if field in case_facts:
        return case_facts[field]

    return None


def evaluate_context(context):
    """Evaluate all six questions against one context."""
    results = []

    for question in EVALUATION_QUESTIONS:
        answer = answer_question(context, question)
        correct = answer == question["expected"]

        results.append(
            {
                "id": question["id"],
                "question": question["question"],
                "expected": question["expected"],
                "answer": answer,
                "correct": correct,
            }
        )

    correct_count = sum(
        1
        for result in results
        if result["correct"]
    )

    return {
        "correct": correct_count,
        "total": len(EVALUATION_QUESTIONS),
        "results": results,
    }


def run_full_evaluation():
    """Evaluate the complete assembled context."""
    context = assemble_context(
        CASE,
        HISTORY,
        EVENTS,
    )

    return evaluate_context(context)


def run_control_evaluation():
    """Evaluate context with the Case Facts block removed."""
    context = assemble_control_context(
        CASE,
        HISTORY,
        EVENTS,
    )

    return evaluate_context(context)


def compare_evaluations():
    """Compare full and control evaluation performance."""
    full = run_full_evaluation()
    control = run_control_evaluation()

    regressions = []

    for full_result, control_result in zip(
        full["results"],
        control["results"],
    ):
        if (
            full_result["correct"]
            and not control_result["correct"]
        ):
            regressions.append(full_result["id"])

    return {
        "full_score": full["correct"],
        "control_score": control["correct"],
        "total_questions": full["total"],
        "regressions": regressions,
        "has_regression": len(regressions) > 0,
    }
