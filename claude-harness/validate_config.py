"""Validate the Claude Code harness configuration."""

from pathlib import Path
import sys


ROOT = Path(__file__).parent

CLAUDE_FILE = ROOT / "CLAUDE.md"

API_STANDARD = (
    ROOT / ".claude" / "standards" / "api.md"
)

TESTING_STANDARD = (
    ROOT / ".claude" / "standards" / "testing.md"
)

PYTHON_RULE = (
    ROOT / ".claude" / "rules" / "python.md"
)

TEST_RULE = (
    ROOT / ".claude" / "rules" / "tests.md"
)

VERIFY_COMMAND = (
    ROOT / ".claude" / "commands" / "verify.md"
)

INVESTIGATION_SKILL = (
    ROOT
    / ".claude"
    / "skills"
    / "investigation"
    / "SKILL.md"
)


REQUIRED_FILES = [
    CLAUDE_FILE,
    API_STANDARD,
    TESTING_STANDARD,
    PYTHON_RULE,
    TEST_RULE,
    VERIFY_COMMAND,
    INVESTIGATION_SKILL,
]


def read_file(path):
    """Read a configuration file."""
    return path.read_text(encoding="utf-8")


def check_required_files():
    """Return missing required configuration files."""
    return [
        str(path.relative_to(ROOT))
        for path in REQUIRED_FILES
        if not path.is_file()
    ]


def check_claude_imports():
    """Verify CLAUDE.md imports the modular standards."""
    content = read_file(CLAUDE_FILE)

    required_imports = [
        "@.claude/standards/api.md",
        "@.claude/standards/testing.md",
    ]

    return [
        item
        for item in required_imports
        if item not in content
    ]


def check_path_scoped_rules():
    """Verify rule files declare path glob patterns."""
    errors = []

    python_rule = read_file(PYTHON_RULE)
    test_rule = read_file(TEST_RULE)

    if 'paths:' not in python_rule:
        errors.append(
            "python rule is missing paths frontmatter"
        )

    if '"src/**/*.py"' not in python_rule:
        errors.append(
            "python rule is missing source glob"
        )

    if 'paths:' not in test_rule:
        errors.append(
            "test rule is missing paths frontmatter"
        )

    if '"**/tests/**/*.py"' not in test_rule:
        errors.append(
            "test rule is missing test glob"
        )

    return errors


def check_command():
    """Verify the project verification command."""
    content = read_file(VERIFY_COMMAND)

    errors = []

    if "python validate_config.py" not in content:
        errors.append(
            "verify command does not run validator"
        )

    if "python -m pytest -v" not in content:
        errors.append(
            "verify command does not run pytest"
        )

    return errors


def check_investigation_skill():
    """Verify the investigation skill is forked and read-only."""
    content = read_file(INVESTIGATION_SKILL)

    errors = []

    if "context: fork" not in content:
        errors.append(
            "investigation skill is not forked"
        )

    required_tools = [
        "Read",
        "Grep",
        "Glob",
    ]

    for tool in required_tools:
        if f"- {tool}" not in content:
            errors.append(
                f"investigation skill is missing {tool}"
            )

    forbidden_tools = [
        "Write",
        "Edit",
        "Bash",
    ]

    for tool in forbidden_tools:
        if f"- {tool}" in content:
            errors.append(
                f"investigation skill allows {tool}"
            )

    return errors


def validate_config():
    """Run every harness validation check."""
    errors = []

    missing_files = check_required_files()

    if missing_files:
        errors.extend(
            f"missing file: {path}"
            for path in missing_files
        )

        return errors

    errors.extend(check_claude_imports())
    errors.extend(check_path_scoped_rules())
    errors.extend(check_command())
    errors.extend(check_investigation_skill())

    return errors


def main():
    """Print validation result and return an exit code."""
    errors = validate_config()

    if errors:
        print("CONFIGURATION INVALID")

        for error in errors:
            print(f"- {error}")

        return 1

    print("OK")

    return 0


if __name__ == "__main__":
    sys.exit(main())
