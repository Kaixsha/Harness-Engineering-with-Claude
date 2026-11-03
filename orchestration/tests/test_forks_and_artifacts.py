import copy
from datetime import datetime, timezone

from src.defect_store import open_memory_database
from src.generate_artifacts import (
    build_fork_evidence,
    build_recovery_evidence,
    generate_artifacts,
)
from src.orchestrator import (
    investigate_hypotheses,
    process_shift,
)
from src.recovery import STALE_AFTER_SECONDS
from src.state import (
    add_fork_note,
    fork_state,
)


def build_main_state():
    connection = open_memory_database()

    result = process_shift(
        connection,
        "SHIFT-A",
    )

    connection.close()

    return result["hot_state"]


def test_fork_has_fork_id():
    main = build_main_state()

    forked = fork_state(
        main,
        "fork-test",
        "test hypothesis",
    )

    assert forked["fork_id"] == "fork-test"


def test_fork_records_parent_shift():
    main = build_main_state()

    forked = fork_state(
        main,
        "fork-test",
        "test hypothesis",
    )

    assert forked["parent_shift_id"] == "SHIFT-A"


def test_fork_records_hypothesis():
    main = build_main_state()

    forked = fork_state(
        main,
        "fork-test",
        "test hypothesis",
    )

    assert forked["hypothesis"] == "test hypothesis"


def test_fork_starts_with_empty_scratchpad():
    main = build_main_state()

    forked = fork_state(
        main,
        "fork-test",
        "test hypothesis",
    )

    assert forked["scratchpad"] == []


def test_adding_note_changes_fork():
    main = build_main_state()

    forked = fork_state(
        main,
        "fork-test",
        "test hypothesis",
    )

    add_fork_note(
        forked,
        "investigation note",
    )

    assert forked["scratchpad"] == [
        "investigation note"
    ]


def test_fork_note_does_not_change_main_state():
    main = build_main_state()
    original = copy.deepcopy(main)

    forked = fork_state(
        main,
        "fork-test",
        "test hypothesis",
    )

    add_fork_note(
        forked,
        "investigation note",
    )

    assert main == original


def test_two_hypothesis_forks_are_created():
    main = build_main_state()

    forks = investigate_hypotheses(main)

    assert set(forks) == {
        "fork_a",
        "fork_b",
    }


def test_fork_hypotheses_are_different():
    main = build_main_state()

    forks = investigate_hypotheses(main)

    assert (
        forks["fork_a"]["hypothesis"]
        != forks["fork_b"]["hypothesis"]
    )


def test_fork_scratchpads_are_different():
    main = build_main_state()

    forks = investigate_hypotheses(main)

    assert (
        forks["fork_a"]["scratchpad"]
        != forks["fork_b"]["scratchpad"]
    )


def test_investigations_leave_main_unchanged():
    main = build_main_state()
    original = copy.deepcopy(main)

    investigate_hypotheses(main)

    assert main == original


def test_recovery_evidence_has_threshold():
    now = datetime(
        2026,
        11,
        3,
        5,
        0,
        tzinfo=timezone.utc,
    )

    evidence = build_recovery_evidence(now)

    assert (
        evidence["staleness_threshold_seconds"]
        == STALE_AFTER_SECONDS
    )


def test_recovery_evidence_recent_resumes():
    now = datetime(
        2026,
        11,
        3,
        5,
        0,
        tzinfo=timezone.utc,
    )

    evidence = build_recovery_evidence(now)

    assert (
        evidence["recent_checkpoint_decision"]
        == "resume"
    )


def test_recovery_evidence_stale_starts_fresh():
    now = datetime(
        2026,
        11,
        3,
        5,
        0,
        tzinfo=timezone.utc,
    )

    evidence = build_recovery_evidence(now)

    assert (
        evidence["stale_checkpoint_decision"]
        == "fresh"
    )


def test_fork_evidence_reports_main_unchanged():
    main = build_main_state()

    evidence = build_fork_evidence(main)

    assert evidence["main_state_unchanged"] is True


def test_fork_evidence_reports_isolation():
    main = build_main_state()

    evidence = build_fork_evidence(main)

    assert (
        evidence["fork_scratchpads_are_isolated"]
        is True
    )


def test_generated_evidence_meets_core_requirements():
    evidence = generate_artifacts()

    assert (
        evidence["shift"]["selected_defect_count"]
        < evidence["shift"]["total_defects_in_cold_state"]
    )

    assert (
        evidence["shift"]["hot_state_within_budget"]
        is True
    )

    assert (
        evidence["forks"]["main_state_unchanged"]
        is True
    )
