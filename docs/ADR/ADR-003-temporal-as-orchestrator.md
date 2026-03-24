# ADR-003: Temporal as the Orchestrator

## Status
Accepted

## Context
ClawPilot needs durable workflow state, retries, pauses, and long-running orchestration.

## Decision
Use Temporal as the orchestration core.

## Consequences
- workflow state is durable
- retries and resumptions are first-class
- approval waits fit naturally
- workflows stay explicit instead of being spread across scripts

## Alternatives considered
- ad hoc scripts
- cron-only orchestration
- custom in-process job queue

## Rationale
Temporal matches the control-plane problem: durable orchestration with explicit state transitions.
