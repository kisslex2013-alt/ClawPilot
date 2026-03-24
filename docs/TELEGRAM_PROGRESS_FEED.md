# Telegram Progress Feed

## Goals

- show live task progress
- expose blockers early
- keep humans informed without flooding chat
- distinguish orchestration updates from evaluation digests

## Semantic events

- task accepted
- step started
- step completed
- blocker found
- approval requested
- approval received
- task completed
- task failed

## Modes

### Quiet
- only major milestones
- blockers and approvals only

### Normal
- milestone updates
- blocker updates
- completion notices

### Verbose
- step-level progress
- richer context
- useful for debugging, not for default operation

## Anti-spam rules

- do not repeat unchanged status
- collapse noisy intermediate updates
- prefer one message per meaningful transition
- do not emit verbose updates for trivial internals
- rate-limit repeated blockers

## Examples of messages

### Взял в работу
- `Task accepted: investigating the dashboard mapping.`
- `Started: planning the orchestration boundary.`

### Завершил этап
- `Completed: foundation docs drafted.`
- `Step done: approval flow defined.`

### Нашел блокер
- `Blocked: source artifact contract is missing a required field.`
- `Stopped: approval context is incomplete.`

### Жду approval
- `Approval needed: proceed with the next workflow stage?`
- `Waiting for approval on the escalation path.`

### Готово
- `Done: task finished and summary published.`
- `Completed successfully.`

## Live progress vs daily digest vs feedback acknowledgements

### Live progress
Real-time or near-real-time task state changes. Short. Actionable. Limited.

### Daily digest
A scheduled summary of what happened across tasks or runs. More compact, less urgent.

### Feedback acknowledgements
Confirm that feedback was received or registered. These are not task progress updates.

Unknown delivery limits and transport details are TODO until implementation.
