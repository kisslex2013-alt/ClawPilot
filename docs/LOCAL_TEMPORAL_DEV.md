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
