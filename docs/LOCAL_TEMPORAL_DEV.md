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

## Not implemented yet

- production rollout
- worker polling loops
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
