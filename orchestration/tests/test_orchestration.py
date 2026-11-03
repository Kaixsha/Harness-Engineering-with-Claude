from datetime import datetime, timedelta, timezone

from src.defect_store import (
    get_all_defects,
    get_shift_defects,
    open_memory_database,
)
from src.orchestrator import (
    investigate_hypotheses,
    process_shift,
)
from src.recovery import (
    FRESH,
    RESUME,
    STALE_AFTER_SECONDS,
    choose_recovery,
)
from src.state import (
    HOT_STATE_BUDGET_BYTES,
    build_hot_state,
    build_warm_state,
    fork_state,
    hot_state_size_bytes,
    hot_state_within_budget,
)


def test_cold_state_contains_all_seeded_defects():
    connection = open_memory_database()

    assert len(get_all_defects(connection)) == 6

    connection.close()


def test_shift_a_returns_two_active_defects():
    connection = open_memory_database()

    defects = get_shift_defects(
        connection,
        "SHIFT-A",
    )

    assert len(defects) == 2

    connection.close()


def test_shift_a_excludes_closed_defect():
    connection = open_memory_database()

    defects = get_shift_defects(
        connection,
        "SHIFT-A",
    )

    ids = [defect[0] for defect in defects]

    assert "DEF-1003" not in ids

    connection.close()


def test_shift_a_excludes_other_shifts():
    connection = open_memory_database()

    defects = get_shift_defects(
        connection,
        "SHIFT-A",
    )

    assert all(
        defect[1] == "SHIFT-A"
        for defect in defects
    )

    connection.close()


def test_shift_filter_returns_smaller_slice():
    connection = open_memory_database()

    all_defects = get_all_defects(connection)
    shift_defects = get_shift_defects(
        connection,
        "SHIFT-A",
    )

    assert len(shift_defects) < len(all_defects)

    connection.close()


def test_hot_state_contains_shift_id():
    connection = open_memory_database()
    defects = get_shift_defects(connection, "SHIFT-A")

    state = build_hot_state("SHIFT-A", defects)

    assert state["shift_id"] == "SHIFT-A"

    connection.close()


def test_hot_state_contains_active_defect_ids():
    connection = open_memory_database()
    defects = get_shift_defects(connection, "SHIFT-A")

    state = build_hot_state("SHIFT-A", defects)

    assert state["active_defect_ids"] == [
        "DEF-1001",
        "DEF-1002",
    ]

    connection.close()


def test_hot_state_is_under_budget():
    connection = open_memory_database()
    defects = get_shift_defects(connection, "SHIFT-A")

    state = build_hot_state("SHIFT-A", defects)

    assert hot_state_within_budget(state) is True

    connection.close()


def test_hot_state_size_less_than_5kb():
    connection = open_memory_database()
    defects = get_shift_defects(connection, "SHIFT-A")

    state = build_hot_state("SHIFT-A", defects)

    assert (
        hot_state_size_bytes(state)
        < HOT_STATE_BUDGET_BYTES
    )

    connection.close()


def test_warm_state_records_defect_count():
    connection = open_memory_database()
    defects = get_shift_defects(connection, "SHIFT-A")

    state = build_warm_state("SHIFT-A", defects)

    assert state["active_defect_count"] == 2

    connection.close()


def test_warm_state_records_components():
    connection = open_memory_database()
    defects = get_shift_defects(connection, "SHIFT-A")

    state = build_warm_state("SHIFT-A", defects)

    assert state["components"] == [
        "api",
        "database",
    ]

    connection.close()


def test_recent_checkpoint_resumes():
    now = datetime(
        2026,
        11,
        3,
        5,
        0,
        tzinfo=timezone.utc,
    )

    checkpoint = now - timedelta(minutes=10)

    assert choose_recovery(checkpoint, now) == RESUME


def test_stale_checkpoint_starts_fresh():
    now = datetime(
        2026,
        11,
        3,
        5,
        0,
        tzinfo=timezone.utc,
    )

    checkpoint = now - timedelta(minutes=45)

    assert choose_recovery(checkpoint, now) == FRESH


def test_missing_checkpoint_starts_fresh():
    now = datetime(
        2026,
        11,
        3,
        5,
        0,
        tzinfo=timezone.utc,
    )

    assert choose_recovery(None, now) == FRESH


def test_exact_threshold_resumes():
    now = datetime(
        2026,
        11,
        3,
        5,
        0,
        tzinfo=timezone.utc,
    )

    checkpoint = now - timedelta(
        seconds=STALE_AFTER_SECONDS
    )

    assert choose_recovery(checkpoint, now) == RESUME


def test_one_second_over_threshold_starts_fresh():
    now = datetime(
        2026,
        11,
        3,
        5,
        0,
        tzinfo=timezone.utc,
    )

    checkpoint = now - timedelta(
        seconds=STALE_AFTER_SECONDS + 1
    )

    assert choose_recovery(checkpoint, now) == FRESH


def test_process_shift_uses_sql_filtered_slice():
    connection = open_memory_database()

    result = process_shift(
        connection,
        "SHIFT-A",
    )

    assert result["selected_defect_count"] == 2
    assert result["total_defects_in_cold_state"] == 6
    assert result["selected_defect_count"] < (
        result["total_defects_in_cold_state"]
    )

    connection.close()
