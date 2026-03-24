# ClawPilot Plan

## Project goals

- Coordinate autonomous work with durable workflow state.
- Make progress, blockers, and approvals visible.
- Keep execution boundaries clear between orchestration, runtime, and evaluation.
- Support balanced autonomy first, not maximal autonomy.

## Non-goals

- Online fine-tuning in v1.
- Replacing OpenClaw execution.
- Replacing ClawLoop evaluation and reporting.
- Multi-node or multi-VPS orchestration.

## v1 scope

- Single VPS deployment.
- Temporal-driven orchestration.
- Telegram progress feed.
- Web dashboard refreshes.
- Approval requests and acknowledgements.
- Learning signals limited to policy, exemplar, routing, and verifier updates.

## Out of scope

- Autonomous self-rewrite loops.
- Production-grade multi-region HA.
- Training pipelines.
- General-purpose task marketplace features.
- Broad third-party integrations not needed for v1.

## Success criteria

- A task can be created, tracked, paused for approval, and completed.
- Progress is visible in Telegram and the dashboard.
- ClawLoop outputs can be consumed without duplicating evaluation logic.
- The system stays understandable and bounded.

## Phases

### 1. Foundation

**Goal**: define repo boundaries, docs, data model, and workflow contracts.

**Deliverables**
- core architecture docs
- data model doc
- Temporal workflow inventory
- dashboard data contract
- Telegram progress feed contract
- ADRs for key decisions

**Acceptance criteria**
- Docs are consistent with the agreed architecture.
- No implementation code is required to understand the v1 shape.
- Unknowns are marked explicitly.

### 2. Orchestration Core

**Goal**: define the minimal orchestration layer and durable workflow structure.

**Deliverables**
- workflow descriptions
- task state model
- event model
- approval request flow
- observability hooks

**Acceptance criteria**
- Each workflow has inputs, outputs, and failure handling.
- Approval points are explicit.
- Progress events can be emitted without coupling to a UI.

### 3. Telegram Progress Feed

**Goal**: surface meaningful live progress in Telegram without spam.

**Deliverables**
- feed modes
- anti-spam rules
- canonical message examples
- distinction between live feed and digest messages

**Acceptance criteria**
- Status updates are concise and useful.
- Quiet mode is possible.
- Blockers and approvals are clearly signaled.

### 4. Web Dashboard

**Goal**: define a minimal dashboard contract for task and run visibility.

**Deliverables**
- dashboard data contract
- field mapping from ClawLoop artifacts
- task card model
- run view model

**Acceptance criteria**
- Existing artifacts can be mapped into the dashboard contract.
- The dashboard does not need to infer missing core state.

### 5. Balanced Autonomy

**Goal**: allow autonomous execution within explicit guardrails.

**Deliverables**
- autonomy policy boundaries
- approval rules
- escalation conditions
- fallback behavior for failures and unknowns

**Acceptance criteria**
- The system knows when to continue, pause, or ask.
- Autonomy is bounded by policy and workflow state.

### 6. Learning Integration

**Goal**: feed ClawLoop outputs back into orchestration decisions.

**Deliverables**
- learning signal mapping
- policy update inputs
- exemplar/routing/verifier learning hooks
- feedback handling contract

**Acceptance criteria**
- Learning improves future orchestration without online fine-tune.
- ClawLoop remains the evaluation source of truth.
