---
description: Validate the Claude Code harness and run its automated tests
allowed-tools:
  - Bash
---

# Verify Claude Code Harness

Validate the current project configuration.

Perform these steps:

1. Run the configuration validator:

   `python validate_config.py`

2. Confirm that the validator prints:

   `OK`

3. Confirm that the validator exits with code `0`.

4. Run the automated test suite:

   `python -m pytest -v`

5. Report the validator result and the pytest summary.

Do not modify project files while performing verification.
