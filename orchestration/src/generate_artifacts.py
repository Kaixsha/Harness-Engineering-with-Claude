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
    """Demonstrate isolation between investigation forks."""

    original_main_state = copy.deepcopy(main_state)

    forks = investigate_hypotheses(main_state)

    fork_a = forks["fork_a"]
    fork_b = forks["fork_b"]

    return {
        "main_shift_id": main_state["shift_id"],
        "main_state_unchanged": (
            main_state == original_main_state
        ),
        "fork_a": {
            "fork_id": fork_a["fork_id"],
            "hypothesis": fork_a["hypothesis"],
            "scratchpad": fork_a["scratchpad"],
        },
        "fork_b": {
            "fork_id": fork_b["fork_id"],
            "hypothesis": fork_b["hypothesis"],
            "scratchpad": fork_b["scratchpad"],
        },
        "fork_scratchpads_are_isolated": (
            fork_a["scratchpad"]
            != fork_b["scratchpad"]
        ),
    }


def generate_artifacts():
    """Run the orchestration demonstration and write evidence."""

    connection = open_memory_database()

    now = datetime(
        2026,
        11,
        3,
        5,
        0,
        tzinfo=timezone.utc,
    )

    recent_checkpoint = (
        now
        - timedelta(minutes=10)
    )

    shift_result = process_shift(
        connection=connection,
        shift_id="SHIFT-A",
        checkpoint_timestamp=recent_checkpoint,
        now=now,
    )

    hot_state_path = write_hot_state(
        shift_result["hot_state"],
        STATE_DIR / "hot_state.json",
    )

    actual_hot_state_file_size = (
        hot_state_path.stat().st_size
    )

    shift_artifact = {
        "run_id": "orchestration-run-001",
        "shift_id": shift_result["shift_id"],
        "query_strategy": shift_result["query_strategy"],
        "total_defects_in_cold_state
