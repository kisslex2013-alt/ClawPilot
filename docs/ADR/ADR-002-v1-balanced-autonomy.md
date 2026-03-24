# ADR-002: v1 Uses Balanced Autonomy

## Status
Accepted

## Context
The system should be useful before it is fully autonomous.
Full autonomy introduces higher risk and more surface area than v1 needs.

## Decision
Ship v1 as balanced autonomy rather than full autonomy.

## Consequences
- approvals remain part of the flow
- the system can pause on uncertainty
- control remains human-legible
- implementation remains bounded

## Alternatives considered
- full autonomy first
- always-manual operation
- constrained autonomy with no learning loop

## Rationale
Balanced autonomy gives enough autonomy to be useful while preserving the ability to intervene, inspect, and correct behavior.
