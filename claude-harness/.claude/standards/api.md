# API Standards

These standards apply to API and integration code in this project.

## Design

- Keep API boundaries explicit.
- Validate required inputs before processing.
- Return structured results from integration boundaries.
- Keep external-service logic separate from business rules.
- Handle unsupported operations explicitly.

## Reliability

- Fail clearly when required inputs are missing.
- Do not silently ignore unexpected states.
- Prefer deterministic validation for rules that must always be enforced.
- Keep integration functions small and testable.

## Security

- Do not commit credentials or secrets.
- Do not hard-code API keys.
- Treat external input as untrusted.
