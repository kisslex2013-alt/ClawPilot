# Local Temporal Dev

## Purpose

Provide a safe local path for inspecting Temporal wiring without requiring a live server by default.

## What works today

- registry and worker previews
- client target summaries
- dry-run workflow planning
- local run plan inspection

## Preview mode

Preview mode is the default.
It prints configuration, queue wiring, and bootstrap hints only.

## Optional connect mode

Connect mode is explicit.
Use it only if a Temporal server already exists.

## First real local execution path

The first actual execution path is still intentionally narrow:
- explicit connect only
- no background worker loop by default
- no deployment assumptions

## Bounded real local execution

The local execution layer is bounded and allowlisted.
Only `smoke_check` is intended for `local_execute` in v1.
`dashboard_refresh` and `clawloop_full_cycle` remain preview-only.

## Preview vs dry-run vs local_execute

- `preview`: no command execution, just planning
- `dry_run`: command plan is built and simulated
- `local_execute`: explicit opt-in only; bounded local script execution with persisted artifacts

## Why smoke_check is first

It is the smallest safe path, has the fewest artifacts, and is easiest to validate without widening the blast radius.

## Why full_cycle is still guarded

`full_cycle` touches more surfaces and is not the first bounded local execution path. Keep it preview-only until the smaller path is stable.

## Persisted run artifacts under `.clawpilot/runs/`

Local execution writes per-run artifacts under:
- `.clawpilot/runs/<run_id>/progress.jsonl`
- `.clawpilot/runs/<run_id>/run-summary.json`
- `.clawpilot/runs/<run_id>/command-result.json`

## Preview-only commands

- `show-config`
- `show-task-queue`
- `show-worker-definition`
- `preview-worker`
- `temporal-client-target`
- `temporal-smoke-plan`

## Explicit connect commands

- `temporal-connectivity-check --connect`
- `temporal-connectivity-smoke --connect`
- `temporal-start-workflow smoke-check --connect`

## Safe local smoke flow

1. `python -m clawpilot.cli show-config`
2. `python -m clawpilot.cli show-task-queue`
3. `python -m clawpilot.cli show-worker-definition`
4. `python -m clawpilot.cli temporal-smoke-plan`
5. `python -m clawpilot.cli temporal-connectivity-smoke`
6. `python -m clawpilot.cli temporal-connectivity-smoke --connect`
7. `python -m clawpilot.cli temporal-start-workflow smoke-check`
8. `python -m clawpilot.cli temporal-start-workflow smoke-check --connect`

## Why worker does not auto-run forever

Because this repo is still a local dev surface, not a production daemon. Infinite polling belongs behind an explicit future mode, not the default path.

## Not implemented yet

- production rollout
- worker polling loops by default
- deployment automation
- dashboard frontend
- live Telegram sending

## Safe local validation flow

1. `python -m clawpilot.cli show-config`
2. `python -m clawpilot.cli show-task-queue`
3. `python -m clawpilot.cli show-worker-definition`
4. `python -m clawpilot.cli preview-worker`
5. `python -m clawpilot.cli temporal-client-target`
6. `python -m clawpilot.cli temporal-connectivity-check --connect`

Only use `--connect` when a real server is present.

## Bounded local ClawLoop execution

- `python -m clawpilot.cli local-exec smoke-check`
- `python -m clawpilot.cli local-exec smoke-check --execute`
- `python -m clawpilot.cli local-exec full-cycle`
- `python -m clawpilot.cli show-latest-run-summary`
- `python -m clawpilot.cli show-run-files`
