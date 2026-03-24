# Dashboard Data Contract

## What ClawLoop already provides

ClawLoop already produces evaluation and reporting artifacts such as:
- manifest.json
- dashboard.md
- latest-delta.md
- weekly-review-report.md
- judge-disagreements.md

## What ClawPilot adds

ClawPilot adds orchestration-facing task state, workflow events, approvals, and normalized progress data.
It does not replace ClawLoop output; it consumes and presents it.

## Minimal dashboard data contract

The dashboard should be able to render:
- task cards
- run views
- progress status
- approval state
- linked artifacts
- latest evaluation summary

## Required fields for task cards

- task_id
- title
- status
- priority
- updated_at
- current_step
- blocker_state
- approval_state
- latest_summary
- artifact_refs

## Required fields for run view

- run_id
- task_id
- started_at
- updated_at
- status
- current_phase
- progress_events
- evaluation_ref
- artifact_refs
- failure_reason
- approval_state

## Mapping from existing artifacts

### manifest.json
Use as the source for run identity, environment metadata, and linked artifacts.

### dashboard.md
Use as a human summary source for the dashboard view.

### latest-delta.md
Use as the source for recent changes, deltas, and recent decision context.

### weekly-review-report.md
Use as the source for longer-horizon summary and review signals.

### judge-disagreements.md
Use as the source for risk signals and points requiring human attention.

## Notes

- The contract should stay small and stable.
- If a field cannot be derived reliably, mark it TODO or Unknown rather than inventing it.
