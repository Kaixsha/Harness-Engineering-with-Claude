## System 2: Context Strategy

### Context Reduction

The context-management strategy is implemented in:

`context-strategy/src/context_builder.py`

The system separates information into three categories:

- Critical Case Facts are preserved.
- Relevant events are retained.
- Historical information is summarized.

Context budget measurement is implemented in:

`context-strategy/src/budget.py`

The generated artifact is:

`context-strategy/artifacts/budget.json`

The successful run measured:

- Raw context: 751 estimated tokens
- Assembled context: 169 estimated tokens
- Reduction: 77.5%
- 50% reduction target met: True

The token counts use the deterministic approximation defined in
`estimate_tokens()`, which estimates one token for every four
characters. These numbers therefore represent the project's
reproducible token estimate rather than an exact model tokenizer count.

### Information Preserved and Summarized

Critical information is preserved verbatim in the Case Facts block,
including the case ID, customer, product, severity, status, and current
issue.

Lower-priority historical information is compressed using
`summarize_history()` rather than retaining the complete history in
the assembled context.

Events are filtered by `select_relevant_events()` so that events marked
as irrelevant are excluded from the assembled context.

This strategy reduced the estimated context from 751 tokens to 169
tokens while retaining the information needed by the evaluation.

### Answerability Evaluation

Evaluation logic is implemented in:

`context-strategy/src/evaluation.py`

Six evaluation questions are defined in `EVALUATION_QUESTIONS`.

The full assembled context achieved:

**6/6 correct**

This exceeds the required minimum of 5/6.

The evidence is generated in:

`context-strategy/artifacts/evaluation-full.json`

### Case Facts Control Experiment

A control context is created by:

`assemble_control_context()`

The control removes the Case Facts block while retaining the other
context components.

The control evaluation achieved:

**0/6 correct**

Compared with the full score of 6/6, all six evaluation questions
regressed:

`Q1, Q2, Q3, Q4, Q5, Q6`

This demonstrates that the Case Facts block contains information
necessary for answering the evaluation questions and is not simply
additional context overhead.

The comparison evidence is generated in:

`context-strategy/artifacts/evaluation-comparison.json`

### Automated Verification

The System 2 automated test suite contains:

**30 passing tests**

The tests verify context construction, Case Facts preservation,
history summarization, relevant-event filtering, context reduction,
the 50% budget requirement, six-question evaluation behavior, and
the Case Facts control regression.

The GitHub Actions workflow is:

`.github/workflows/context-strategy-tests.yml`

The workflow also generates and uploads the context-strategy evidence
artifacts.
