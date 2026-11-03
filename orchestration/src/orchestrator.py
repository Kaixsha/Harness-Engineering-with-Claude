"""Layer 3 orchestration for shift processing."""

from datetime import datetime, timezone

from src.defect_store import (
    get_all_defects,
    get_shift_defects,
)
from src.recovery import choose_recovery
from src.state import (
    add_fork_note,
    build_hot_state,
    build_warm_state,
    fork_state,
    hot_state_size_bytes,
    hot_state_within_budget,
)


def process_shift(
    connection,
    shift_id,
    checkpoint_timestamp=None,
    now=None,
):
    """Process one shift using a SQL-filtered defect slice."""

    if now is None:
        now = datetime.now(timezone.utc)

    all_defects = get_all_defects(connection)

    shift_defects = get_shift_defects(
        connection,
        shift_id,
    )

    recovery_decision = choose_recovery(
        checkpoint_timestamp,
        now,
    )

    hot_state = build_hot_state(
        shift_id,
        shift_defects,
    )

    warm_state = build_warm_state(
        shift_id,
        shift_defects,
    )

    return {
        "shift_id": shift_id,
        "recovery_decision": recovery_decision,
        "total_defects_in_cold_state": len(all_defects),
        "selected_defect_count": len(shift_defects),
        "selected_defect_ids": [
            defect[0]
            for defect in shift_defects
        ],
        "query_strategy": (
            "SQL-filtered by shift_id and active status"
        ),
        "hot_state": hot_state,
        "warm_state": warm_state,
        "hot_state_size_bytes": (
            hot_state_size_bytes(hot_state)
        ),
        "hot_state_within_budget": (
            hot_state_within_budget(hot_state)
        ),
    }


def investigate_hypotheses(main_state):
    """Create two isolated investigation forks."""

    fork_a = fork_state(
        main_state,
        "fork-A",
        "Recent deployment introduced regression",
    )

    fork_b = fork_state(
        main_state,
        "fork-B",
        "Dependent service instability caused failures",
    )

    add_fork_note(
        fork_a,
        (
            "Investigate recent deployment changes "
            "and application behavior."
        ),
    )

    add_fork_note(
        fork_b,
        (
            "Investigate dependency health "
            "and connectivity."
        ),
    )

    return {
        "fork_a": fork_a,
        "fork_b": fork_b,
    }
