from pathlib import Path

from validate_config import (
    API_STANDARD,
    CLAUDE_FILE,
    INVESTIGATION_SKILL,
    PYTHON_RULE,
    REQUIRED_FILES,
    TESTING_STANDARD,
    TEST_RULE,
    VERIFY_COMMAND,
    check_claude_imports,
    check_command,
    check_investigation_skill,
    check_path_scoped_rules,
    check_required_files,
    read_file,
    validate_config,
)


def test_claude_file_exists():
    assert CLAUDE_FILE.is_file()


def test_api_standard_exists():
    assert API_STANDARD.is_file()


def test_testing_standard_exists():
    assert TESTING_STANDARD.is_file()


def test_python_rule_exists():
    assert PYTHON_RULE.is_file()


def test_test_rule_exists():
    assert TEST_RULE.is_file()


def test_verify_command_exists():
    assert VERIFY_COMMAND.is_file()


def test_investigation_skill_exists():
    assert INVESTIGATION_SKILL.is_file()


def test_all_required_files_exist():
    assert all(path.is_file() for path in REQUIRED_FILES)


def test_required_file_count():
    assert len(REQUIRED_FILES) == 7


def test_read_file_returns_text():
    content = read_file(CLAUDE_FILE)

    assert isinstance(content, str)


def test_claude_md_is_not_empty():
    content = read_file(CLAUDE_FILE)

    assert content.strip()


def test_claude_imports_api_standard():
    content = read_file(CLAUDE_FILE)

    assert "@.claude/standards/api.md" in content


def test_claude_imports_testing_standard():
    content = read_file(CLAUDE_FILE)

    assert "@.claude/standards/testing.md" in content


def test_claude_import_check_passes():
    assert check_claude_imports() == []


def test_required_file_check_passes():
    assert check_required_files() == []


def test_python_rule_has_frontmatter():
    content = read_file(PYTHON_RULE)

    assert content.startswith("---")


def test_python_rule_declares_paths():
    content = read_file(PYTHON_RULE)

    assert "paths:" in content


def test_python_rule_has_source_glob():
    content = read_file(PYTHON_RULE)

    assert '"src/**/*.py"' in content


def test_test_rule_has_frontmatter():
    content = read_file(TEST_RULE)

    assert content.startswith("---")


def test_test_rule_declares_paths():
    content = read_file(TEST_RULE)

    assert "paths:" in content


def test_test_rule_has_recursive_test_glob():
    content = read_file(TEST_RULE)

    assert '"**/tests/**/*.py"' in content


def test_path_scoped_rule_check_passes():
    assert check_path_scoped_rules() == []


def test_verify_command_runs_validator():
    content = read_file(VERIFY_COMMAND)

    assert "python validate_config.py" in content


def test_verify_command_runs_pytest():
    content = read_file(VERIFY_COMMAND)

    assert "python -m pytest -v" in content


def test_command_check_passes():
    assert check_command() == []


def test_skill_uses_forked_context():
    content = read_file(INVESTIGATION_SKILL)

    assert "context: fork" in content


def test_skill_allows_read():
    content = read_file(INVESTIGATION_SKILL)

    assert "- Read" in content


def test_skill_allows_grep():
    content = read_file(INVESTIGATION_SKILL)

    assert "- Grep" in content


def test_skill_allows_glob():
    content = read_file(INVESTIGATION_SKILL)

    assert "- Glob" in content


def test_skill_does_not_allow_write():
    content = read_file(INVESTIGATION_SKILL)

    assert "- Write" not in content


def test_skill_does_not_allow_edit():
    content = read_file(INVESTIGATION_SKILL)

    assert "- Edit" not in content


def test_skill_does_not_allow_bash():
    content = read_file(INVESTIGATION_SKILL)

    assert "- Bash" not in content


def test_investigation_skill_check_passes():
    assert check_investigation_skill() == []


def test_complete_configuration_is_valid():
    assert validate_config() == []


def test_readme_exists():
    readme = Path(__file__).parents[1] / "README.md"

    assert readme.is_file()
