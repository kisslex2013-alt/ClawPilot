# Architecture

## System layers

### Control plane
ClawPilot owns task orchestration, approvals, workflow state, and progress surfacing.

### Execution plane
OpenClaw executes tools and performs concrete work.

### Evaluation plane
ClawLoop evaluates runs, generates reports, and produces learning signals.

### UI plane
Telegram and the web dashboard present state to humans.

## Component responsibilities

### ClawPilot
- owns task lifecycle
- coordinates workflows
- emits progress and approval requests
- stores orchestration state
- consumes eval and learning signals

### OpenClaw
- runs tools and actions
- executes automation steps
- exposes runtime/tool integration

### ClawLoop
- judges and reports outcomes
- tracks regressions and patterns
- produces policy and learning artifacts

### Telegram
- live status updates
- approval prompts
- concise acknowledgements

### Web dashboard
- task cards
- run views
- summary and drill-down views

## Control plane vs execution plane vs evaluation plane

This separation keeps orchestration decisions from being mixed with runtime execution and evaluation logic.
It also avoids coupling UI state to tool execution details.

## Why separate repo

- clear ownership boundary
- smaller blast radius for orchestration changes
- easier versioning of the control plane
- avoids leaking executor or evaluator concerns into orchestration design

## Why Temporal

Temporal provides durable orchestration, retries, checkpoints, and long-running workflow state.
That matches the control-plane problem better than ad hoc scripts.

## Why balanced autonomy first

v1 needs useful autonomy without losing control.
Balanced autonomy is easier to reason about, safer to operate, and enough to validate the architecture.

## Integration boundaries with ClawLoop and OpenClaw

- **ClawPilot → OpenClaw**: dispatch work, observe runtime events, request progress updates
- **ClawPilot → ClawLoop**: consume eval outputs, summaries, and learning signals
- **OpenClaw → ClawPilot**: execution status, tool results, progress hooks
- **ClawLoop → ClawPilot**: verdicts, reports, policy signals, artifacts

## Verifier / notifier / approval roles

### Verifier
Checks whether a step or run satisfied the expected condition.

### Notifier
Surfaces concise updates to Telegram and dashboard consumers.

### Approval role
Pauses execution when human confirmation is required.

Unknowns about exact runtime wiring remain TODO until implementation starts.
