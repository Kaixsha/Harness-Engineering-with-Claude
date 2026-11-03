"""Tiered state management for Layer 3 orchestration."""

import copy
import json
from pathlib import Path


HOT_STATE_BUDGET_BYTES = 5 * 1024


def build_hot_state(shift_id, defects):
    """Build compact state for the currently active shift."""
    return {
        "shift_id": shift_id,
        "checkpoint": "defects_loaded",
        "status": "active",
        "active_defect_ids": [
            defect[0]
            for defect in defects
        ],
    }


def build_warm_state(shift_id, defects):
    """Build a compact summary used across nearby runs."""
    return {
        "shift_id": shift_id,
        "active_defect_count": len(defects),
        "components": sorted(
            {
                defect[4]
                for defect in defects
            }
        ),
        "summary": (
            f"{len(defects)} active defects selected "
            f"for {shift_id}."
        ),
    }


def hot_state_size_bytes(state):
    """Return serialized hot-state size in bytes."""
    encoded = json.dumps(
        state,
        sort_keys=True,
    ).encode("utf-8")

    return len(encoded)


def hot_state_within_budget(state):
    """Return whether hot state remains below its size budget."""
    return hot_state_size_bytes(state) < HOT_STATE_BUDGET_BYTES


def write_hot_state(state, output_path):
    """Write hot state to disk."""
    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(state, indent=2),
        encoding="utf-8",
    )

    return path


def read_hot_state(input_path):
    """Read hot state from disk."""
    path = Path(input_path)

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def fork_state(main_state, fork_id, hypothesis):
    """Create an isolated investigation state."""
    forked = copy.deepcopy(main_state)

    forked["fork_id"] = fork_id
    forked["parent_shift_id"] = main_state["shift_id"]
    forked["hypothesis"] = hypothesis
    forked["scratchpad"] = []

    return forked


def add_fork_note(forked_state, note):
    """Add investigation evidence to a fork only."""
    forked_state["scratchpad"].append(note)

    return forked_state
