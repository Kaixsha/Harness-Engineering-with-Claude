# Layer 3 Orchestration System

This project implements Layer 3 orchestration with tiered state, SQL-filtered defect retrieval, crash recovery, and isolated investigation forks.

## Goals

- Maintain hot, warm, and cold state.
- Keep the hot-state file below approximately 5 KB.
- Retrieve only defects relevant to the current shift using SQL.
- Avoid passing the complete defect history into the active context.
- Save checkpoints that support crash recovery.
- Decide whether to resume an existing session or start fresh based on checkpoint staleness.
- Keep forked investigations isolated from the main session state.
- Generate run artifacts demonstrating orchestration behavior.

## State Layers

### Hot State

Contains only information needed for the current active shift, such as:

- shift identifier
- current checkpoint
- active defect identifiers
- current orchestration status

### Warm State

Contains compact summaries and recent investigation information that may be useful across nearby runs.

### Cold State

Contains the complete defect history stored in SQLite.

The orchestration layer selects only the required slice of cold-state data before processing a shift.

## Crash Recovery

The system will save checkpoint information containing enough state to determine whether interrupted work should resume.

A configured staleness threshold will determine whether the system:

- resumes the existing state, or
- starts a fresh session.

## Session Forking

Investigations may fork from the main session.

Each fork receives isolated scratch state so experimental hypotheses do not 
