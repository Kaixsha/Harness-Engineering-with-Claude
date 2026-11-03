# Context Strategy System

This project implements a context-management strategy that reduces model input while preserving answerability.

## Goals

- Assemble a smaller context from a larger raw baseline.
- Preserve critical Case Facts verbatim.
- Summarize lower-priority historical information.
- Reduce assembled context size by at least 50%.
- Answer at least 5 of 6 evaluation questions correctly.
- Compare the full context against a control variant with the Case Facts block removed.

## Evidence

The system will generate:

- `budget.json`
- full evaluation results
- control evaluation results

These artifacts will be used to demonstrate context reduction and answerability.

## Verification

The system will be verified using an automated pytest suite containing 30 tests.
