---
paths:
  - "tests/**/*.py"
  - "**/tests/**/*.py"
---

# Python Test Rules

These instructions apply to Python test files throughout the project.

- Use pytest.
- Give each test a descriptive name.
- Keep tests deterministic and independent.
- Do not require network connectivity.
- Cover normal, boundary, and failure conditions.
- Test observable behavior.
- Use controlled data and avoid shared mutable state.
