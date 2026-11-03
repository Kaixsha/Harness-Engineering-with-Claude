"""Measure context size and generate budget evidence."""

import json

from src.context_builder import assemble_context
from src.sample_data import CASE, EVENTS, HISTORY, RAW_NOTES


def serialize(data):
    """Convert data into a consistent text representation."""
    return json.dumps(data, sort_keys=True)


def estimate_tokens(text):
    """
    Estimate tokens deterministically for this project.

    This project uses a simple approximation of four characters
    per token so that measurements are reproducible.
    """
    return max(1, (len(text) + 3) // 4)


def build_raw_context():
    """Build the unoptimized baseline context."""
    return {
        "case": CASE,
        "history": HISTORY,
        "events": EVENTS,
        "raw_notes": RAW_NOTES,
    }


def measure_context_budget():
    """Compare the raw baseline with the assembled context."""
    raw_context = build_raw_context()

    assembled_context = assemble_context(
        CASE,
        HISTORY,
        EVENTS,
    )

    raw_text = serialize(raw_context)
    assembled_text = serialize(assembled_context)

    raw_tokens = estimate_tokens(raw_text)
    assembled_tokens = estimate_tokens(assembled_text)

    reduction_percent = round(
        (1 - (assembled_tokens / raw_tokens)) * 100,
        2,
    )

    return {
        "raw_tokens": raw_tokens,
        "assembled_tokens": assembled_tokens,
        "reduction_percent": reduction_percent,
        "meets_50_percent_target": reduction_percent >= 50,
    }
