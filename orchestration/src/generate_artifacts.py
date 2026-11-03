"""Generate evidence artifacts for Layer 3 orchestration."""

import copy
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.defect_store import open_memory_database
from src.orchestrator import (
    investigate_hypotheses,
    process_shift,
)
from src.recovery import (
    STALE_AFTER_SECONDS,
    choose_recovery,
)
from src.state import write_hot_state


ARTIFACTS_DIR = Path("artifacts")
STATE_DIR = Path("state")


def write_json(path, data):
    """Write formatted JSON data to disk."""
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

    return path


def build_recovery_evidence(now):
    """Demonstrate resume and fresh recovery decisions."""

    recent_checkpoint = (
        now
        - timedelta(
            seconds=STALE_AFTER_SECONDS - 60
        )
    )

    stale_checkpoint = (
        now
        - timedelta(
            seconds=STALE_AFTER_SECONDS + 60
        )
    )

    return {
        "staleness_threshold_seconds": STALE_AFTER_SECONDS,
        "staleness_threshold_minutes": (
            STALE_AFTER_SECONDS // 60
        ),
        "recent_checkpoint_age_seconds": (
            STALE_AFTER_SECONDS - 60
        ),
        "recent_checkpoint_decision": choose_recovery(
            recent_checkpoint,
            now,
        ),
        "stale_checkpoint_age_seconds": (
            STALE_AFTER_SECONDS + 60
        ),
        "stale_checkpoint_decision": choose_recovery(
            stale_checkpoint,
            now,
        ),
        "missing_checkpoint_decision": choose_recovery(
            None,
            now,
        ),
    }


def build_fork_evidence(main_state):
    """Demonstrate 
