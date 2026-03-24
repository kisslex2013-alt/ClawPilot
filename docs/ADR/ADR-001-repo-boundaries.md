# ADR-001: Separate ClawPilot Repo Boundaries

## Status
Accepted

## Context
ClawPilot is the orchestration and autonomy control layer.
ClawLoop is the evaluation and learning layer.
OpenClaw is the execution/runtime layer.

## Decision
Keep ClawPilot in a separate repository.

## Consequences
- clearer ownership boundaries
- less coupling between orchestration and execution code
- easier evolution of the control plane
- safer versioning of workflow contracts

## Alternatives considered
- putting everything in one repo
- merging orchestration into ClawLoop
- placing orchestration inside OpenClaw

## Rationale
A separate repo keeps the orchestration layer explicit and prevents the evaluator or executor from becoming the accidental home of control-plane logic.
