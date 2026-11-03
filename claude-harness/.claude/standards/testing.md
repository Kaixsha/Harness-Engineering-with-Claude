# Testing Standards

These standards apply to automated tests in this project.

## Test Design

- Use pytest for Python tests.
- Keep tests deterministic and repeatable.
- Give each test a descriptive name.
- Test observable behavior rather than implementation details.
- Cover normal, boundary, and failure conditions.

## Isolation

- Tests must not depend on execution order.
- Avoid shared mutable state between tests.
- Use controlled test data.
- Do not require network access for unit tests.

## Verification

A project change is considered verified only when:

1. The configuration validator succeeds.
2. The validator reports `OK`.
3. The validator exits with code `0`.
4. The automated test suite passes.
