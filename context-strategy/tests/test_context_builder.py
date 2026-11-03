from src.context_builder import (
    assemble_context,
    assemble_control_context,
    build_case_facts,
    select_relevant_events,
    summarize_history,
)
from src.sample_data import CASE, EVENTS, HISTORY


def test_case_facts_preserve_case_id():
    facts = build_case_facts(CASE)

    assert facts["case_id"] == "CASE-2048"


def test_case_facts_preserve_customer():
    facts = build_case_facts(CASE)

    assert facts["customer"] == "Northwind Retail"


def test_case_facts_preserve_product():
    facts = build_case_facts(CASE)

    assert facts["product"] == "Cloud Inventory API"


def test_case_facts_preserve_severity():
    facts = build_case_facts(CASE)

    assert facts["severity"] == "high"


def test_case_facts_preserve_status():
    facts = build_case_facts(CASE)

    assert facts["status"] == "investigating"


def test_case_facts_preserve_current_issue():
    facts = build_case_facts(CASE)

    assert facts["current_issue"] == (
        "Inventory synchronization requests are timing out."
    )


def test_history_is_summarized():
    summary = summarize_history(HISTORY)

    assert "historical events recorded" in summary


def test_empty_history_has_default_summary():
    summary = summarize_history([])

    assert summary == "No prior history."


def test_only_relevant_events_are_selected():
    selected = select_relevant_events(EVENTS)

    assert len(selected) == 3


def test_selected_events_are_relevant():
    selected = select_relevant_events(EVENTS)

    assert all(event["relevant"] is True for event in selected)


def test_full_context_contains_case_facts():
    context = assemble_context(
        CASE,
        HISTORY,
        EVENTS,
    )

    assert "case_facts" in context


def test_full_context_contains_history_summary():
    context = assemble_context(
        CASE,
        HISTORY,
        EVENTS,
    )

    assert "history_summary" in context


def test_full_context_contains_relevant_events():
    context = assemble_context(
        CASE,
        HISTORY,
        EVENTS,
    )

    assert "relevant_events" in context


def test_control_context_removes_case_facts():
    context = assemble_control_context(
        CASE,
        HISTORY,
        EVENTS,
    )

    assert "case_facts" not in context


def test_control_still_contains_relevant_events():
    context = assemble_control_context(
        CASE,
        HISTORY,
        EVENTS,
    )

    assert "relevant_events" in context
