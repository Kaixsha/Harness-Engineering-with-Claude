"""Generate evidence artifacts for the context strategy system."""

import json
from pathlib import Path

from src.budget import measure_context_budget
from src.evaluation import (
    compare_evaluations,
    run_control_evaluation,
    run_full_evaluation,
)


def write_json(path, data):
    """Write formatted JSON evidence to a file."""
    path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


def generate_artifacts():
    """Generate all context-strategy evidence artifacts."""
    artifacts_directory = Path("artifacts")
    artifacts_directory.mkdir(exist_ok=True)

    budget = measure_context_budget()
    full_evaluation = run_full_evaluation()
    control_evaluation = run_control_evaluation()
    comparison = compare_evaluations()

    write_json(
        artifacts_directory / "budget.json",
        budget,
    )

    write_json(
        artifacts_directory / "evaluation-full.json",
        full_evaluation,
    )

    write_json(
        artifacts_directory / "evaluation-control.json",
        control_evaluation,
    )

    write_json(
        artifacts_directory / "evaluation-comparison.json",
        comparison,
    )

    return {
        "budget": budget,
        "full_evaluation": full_evaluation,
        "control_evaluation": control_evaluation,
        "comparison": comparison,
    }


def main():
    """Generate and display context-strategy evidence."""
    evidence = generate_artifacts()

    print("Context Strategy Evidence")
    print("=========================")

    print(
        "Raw tokens:",
        evidence["budget"]["raw_tokens"],
    )

    print(
        "Assembled tokens:",
        evidence["budget"]["assembled_tokens"],
    )

    print(
        "Reduction:",
        evidence["budget"]["reduction_percent"],
        "%",
    )

    print(
        "Meets 50% target:",
        evidence["budget"]["meets_50_percent_target"],
    )

    print(
        "Full evaluation:",
        f'{evidence["full_evaluation"]["correct"]}/'
        f'{evidence["full_evaluation"]["total"]}',
    )

    print(
        "Control evaluation:",
        f'{evidence["control_evaluation"]["correct"]}/'
        f'{evidence["control_evaluation"]["total"]}',
    )

    print(
        "Regressions:",
        evidence["comparison"]["regressions"],
    )


if __name__ == "__main__":
    main()
