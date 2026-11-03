---
name: investigation
description: Investigate repository issues using read-only tools and return evidence without modifying the main working context.
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Repository Investigation

Investigate the reported issue using read-only repository access.

## Process

1. Identify files related to the reported issue.
2. Search those files for relevant functions, settings, and error messages.
3. Gather evidence from repository content.
4. Compare the evidence against the reported behavior.
5. Return a concise investigation report.

## Required Output

Return the following sections:

### Relevant Files

List the files connected to the issue.

### Evidence

Describe the repository evidence found through read-only inspection.

### Likely Cause

Explain the likely cause supported by the available evidence.

### Recommended Next Action

Recommend a next action without modifying project files.

## Restrictions

- Do not edit files.
- Do not create files.
- Do not delete files.
- Do not run commands that change repository state.
- Use only the tools listed in `allowed-tools`.
- Keep investigation notes isolated inside the forked context.
