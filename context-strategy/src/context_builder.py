"""Build compact context while preserving critical case facts."""


def build_case_facts(case):
    """Preserve critical case facts in a compact block."""
    return {
        "case_id": case["case_id"],
        "customer": case["customer"],
        "product": case["product"],
        "severity": case["severity"],
        "status": case["status"],
        "current_issue": case["current_issue"],
    }


def summarize_history(history):
    """Compress older history into a short summary."""
    if not history:
        return "No prior history."

    count = len(history)
    latest = history[-1]

    return (
        f"{count} historical events recorded. "
        f"Latest historical event: {latest}"
    )


def select_relevant_events(events):
    """Keep only events marked as relevant."""
    return [
        event
        for event in events
        if event.get("relevant") is True
    ]


def assemble_context(case, history, events):
    """Assemble the optimized context used by the system."""
    return {
        "case_facts": build_case_facts(case),
        "relevant_events": select_relevant_events(events),
        "history_summary": summarize_history(history),
    }


def assemble_control_context(case, history, events):
    """Build the control variant without the Case Facts block."""
    return {
        "relevant_events": select_relevant_events(events),
        "history_summary": summarize_history(history),
    }
