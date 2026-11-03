# Claude Code Project Instructions

This project uses modular standards and path-scoped rules to keep project guidance organized and maintainable.

## Imported Standards

@.claude/standards/api.md

@.claude/standards/testing.md

## Project Principles

- Keep application behavior deterministic when a rule must be enforced.
- Keep model guidance separate from code-level enforcement.
- Prefer small, testable functions.
- Keep tests deterministic and repeatable.
- Use project-scoped commands for repeatable development workflows.
- Use isolated forked context for investigations that should not modify the main working context.

## Verification

Before considering a project change complete:

1. Run the configuration validator.
2. Run the automated test suite.
3. Confirm the validator reports `OK`.
4. Confirm all tests pass.
