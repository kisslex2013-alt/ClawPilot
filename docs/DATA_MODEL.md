# Data Model

## task

**Purpose**: top-level unit of work.

**Minimal required fields**
- task_id
- title
- status
- created_at
- updated_at

**Optional fields**
- description
- priority
- owner
- source
- tags
- due_at

**Relations**
- has many task_step
- has many task_event
- may have many approval_request
- may reference artifacts

**Notes for v1**
- Keep status values small and explicit.
- Unknown ownership semantics should remain TODO.

## task_step

**Purpose**: named stage within a task.

**Minimal required fields**
- step_id
- task_id
- name
- status
- order

**Optional fields**
- started_at
- completed_at
- summary
- blocker

**Relations**
- belongs to task
- has many task_event
- may emit progress_event

**Notes for v1**
- Steps should be human-readable.

## task_event

**Purpose**: immutable audit trail for task lifecycle changes.

**Minimal required fields**
- event_id
- task_id
- type
- timestamp
- payload

**Optional fields**
- step_id
- actor
- source
- correlation_id

**Relations**
- belongs to task
- may belong to task_step

**Notes for v1**
- Keep payload compact and machine-readable.

## progress_event

**Purpose**: live user-facing progress signal.

**Minimal required fields**
- event_id
- task_id
- kind
- timestamp
- message

**Optional fields**
- step_id
- verbosity
- channel
- correlation_id
- metadata

**Relations**
- derived from task_event or workflow state

**Notes for v1**
- This is not the same thing as an internal audit event.

## approval_request

**Purpose**: request human decision before continuation.

**Minimal required fields**
- approval_id
- task_id
- reason
- status
- requested_at

**Optional fields**
- step_id
- context
- options
- resolved_at
- resolved_by

**Relations**
- belongs to task
- may belong to task_step

**Notes for v1**
- Approval flow must be explicit and traceable.

## artifact_ref

**Purpose**: pointer to an output produced elsewhere.

**Minimal required fields**
- artifact_id
- task_id
- kind
- uri
- created_at

**Optional fields**
- label
- checksum
- source
- metadata

**Relations**
- belongs to task
- may belong to step or evaluation episode

**Notes for v1**
- Prefer references over copying large payloads.

## evaluation_episode

**Purpose**: record of a run evaluated by ClawLoop.

**Minimal required fields**
- episode_id
- task_id
- run_id
- verdict
- evaluated_at

**Optional fields**
- report_ref
- disagreement_ref
- policy_signals
- notes

**Relations**
- belongs to task
- may reference artifacts

**Notes for v1**
- Use this as the bridge between orchestration and learning signals.
