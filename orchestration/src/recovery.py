"""Crash recovery decisions for Layer 3 orchestration."""

from datetime import datetime, timezone


STALE_AFTER_SECONDS = 1800

RESUME = "resume"
FRESH = "fresh"


def checkpoint_age_seconds(checkpoint_timestamp, now):
    """Return the age of a checkpoint in seconds."""
    return (
        now - checkpoint_timestamp
    ).total_seconds()


def is_checkpoint_stale(
    checkpoint_timestamp,
    now,
    threshold_seconds=STALE_AFTER_SECONDS,
):
    """Return True when a checkpoint exceeds the staleness threshold."""
    age = checkpoint_age_seconds(
        checkpoint_timestamp,
        now,
    )

    return age > threshold_seconds


def choose_recovery(
    checkpoint_timestamp,
    now,
    threshold_seconds=STALE_AFTER_SECONDS,
):
    """Choose whether to resume or start fresh."""
    if checkpoint_timestamp is None:
        return FRESH

    if is_checkpoint_stale(
        checkpoint_timestamp,
        now,
        threshold_seconds,
    ):
        return FRESH

    return RESUME


def timestamp_now():
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


def serialize_timestamp(timestamp):
    """Convert a timestamp to an ISO 8601 string."""
    return timestamp.isoformat()


def parse_timestamp(value):
    """Convert an ISO 8601 string back into a datetime."""
    return datetime.fromisoformat(value)
