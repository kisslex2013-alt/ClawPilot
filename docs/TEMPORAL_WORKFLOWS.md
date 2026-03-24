# Temporal Workflows

## clawloop_full_cycle_workflow

**Purpose**: run the ClawLoop evaluation/report cycle as a durable workflow.

**Trigger**: scheduled, manual, or task-completion event.

**Inputs**
- task_id
- run context
- artifact refs

**Steps**
1. gather inputs
2. invoke ClawLoop cycle
3. collect report artifacts
4. publish progress and summary events
5. store evaluation episode

**Outputs**
- evaluation_episode
- report artifacts
- progress events

**Failure handling**
- retry transient failures
- surface hard failures as blockers
- preserve partial artifacts when available

**Approval points**
- usually none
- escalate if evaluation reveals a decision boundary

**Observability/progress hooks**
- start
- stage completion
- failure
- final verdict

## smoke_check_workflow

**Purpose**: verify that the orchestration path is healthy.

**Trigger**: manual, startup, or scheduled health check.

**Inputs**
- environment context
- task or run identifier

**Steps**
1. validate prerequisites
2. check integration surfaces
3. emit health summary

**Outputs**
- smoke result
- status events

**Failure handling**
- fail fast on missing prerequisites
- report precise blockers

**Approval points**
- none

**Observability/progress hooks**
- one concise status update

## notify_summary_workflow

**Purpose**: produce a concise summary notification.

**Trigger**: task milestone, run completion, or digest schedule.

**Inputs**
- task state
- key artifacts
- audience mode

**Steps**
1. collect relevant state
2. render summary
3. send notification

**Outputs**
- notification record
- delivery status

**Failure handling**
- retry delivery failures when safe
- degrade to digest if live send fails

**Approval points**
- none

**Observability/progress hooks**
- message sent
- delivery failure

## dashboard_refresh_workflow

**Purpose**: refresh dashboard-facing data.

**Trigger**: schedule, task event, or artifact update.

**Inputs**
- task id
- artifact refs
- latest summaries

**Steps**
1. read source artifacts
2. normalize contract data
3. publish dashboard payload

**Outputs**
- dashboard data snapshot
- refresh timestamp

**Failure handling**
- retry source read failures
- keep last known good snapshot on partial failure

**Approval points**
- none

**Observability/progress hooks**
- refresh started
- refresh completed
- refresh degraded
