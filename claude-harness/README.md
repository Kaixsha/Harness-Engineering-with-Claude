# Claude Code Harness

This system configures a Claude Code project harness with hierarchical instructions, modular standards, path-scoped rules, a project command, and an isolated read-only skill.

## Goals

- Provide a root `CLAUDE.md` configuration.
- Import modular standards using `@path` references.
- Apply conventions through path-scoped rule files.
- Provide a project-scoped slash command.
- Configure an investigation skill with `context: fork`.
- Restrict the forked skill to read-only tools.
- Validate the complete configuration automatically.
- Pass a 35-test automated test suite.

## Planned Structure

```text
claude-harness/
├── CLAUDE.md
├── validate_config.py
├── .claude/
│   ├── standards/
│   ├── rules/
│   ├── commands/
│   └── skills/
└── tests/
