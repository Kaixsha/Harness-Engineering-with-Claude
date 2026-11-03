"""SQLite-backed cold-state defect storage."""

import sqlite3


DEFECTS = [
    (
        "DEF-1001",
        "SHIFT-A",
        "critical",
        "open",
        "api",
        "API requests are timing out.",
    ),
    (
        "DEF-1002",
        "SHIFT-A",
        "high",
        "investigating",
        "database",
        "Database connections are intermittently failing.",
    ),
    (
        "DEF-1003",
        "SHIFT-A",
        "medium",
        "closed",
        "frontend",
        "UI alignment issue resolved.",
    ),
    (
        "DEF-2001",
        "SHIFT-B",
        "high",
        "open",
        "network",
        "Network latency increased.",
    ),
    (
        "DEF-2002",
        "SHIFT-B",
        "low",
        "closed",
        "documentation",
        "Documentation typo corrected.",
    ),
    (
        "DEF-3001",
        "SHIFT-C",
        "medium",
        "open",
        "worker",
        "Background worker retries increased.",
    ),
]


def create_database(connection):
    """Create the cold-state defects table."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS defects (
            defect_id TEXT PRIMARY KEY,
            shift_id TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            component TEXT NOT NULL,
            summary TEXT NOT NULL
        )
        """
    )

    connection.commit()


def seed_database(connection):
    """Insert controlled defect history for the demonstration."""
    connection.executemany(
        """
        INSERT OR REPLACE INTO defects (
            defect_id,
            shift_id,
            severity,
            status,
            component,
            summary
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        DEFECTS,
    )

    connection.commit()


def get_all_defects(connection):
    """Return the complete cold-state defect history."""
    cursor = connection.execute(
        """
        SELECT
            defect_id,
            shift_id,
            severity,
            status,
            component,
            summary
        FROM defects
        ORDER BY defect_id
        """
    )

    return cursor.fetchall()


def get_shift_defects(connection, shift_id):
    """Return only active defects relevant to one shift."""
    cursor = connection.execute(
        """
        SELECT
            defect_id,
            shift_id,
            severity,
            status,
            component,
            summary
        FROM defects
        WHERE shift_id = ?
          AND status IN ('open', 'investigating')
        ORDER BY defect_id
        """,
        (shift_id,),
    )

    return cursor.fetchall()


def open_memory_database():
    """Create and prepare an in-memory demonstration database."""
    connection = sqlite3.connect(":memory:")

    create_database(connection)
    seed_database(connection)

    return connection
