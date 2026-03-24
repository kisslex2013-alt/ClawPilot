# Telegram Integration

Telegram is the human-facing transport for ClawPilot v1.

## Roles

- live progress feed
- daily digest
- approval requests
- feedback acknowledgements

## Builder vs sender

- **Builder**: turns state into semantic messages
- **Sender**: delivers the message over Telegram

The two concerns should stay separate.

## Anti-spam rules

- emit only meaningful transitions
- deduplicate repeated states
- keep live updates short
- send digests on schedule, not on every event

## Why semantic progress events

Direct progress events should describe task meaning, not raw workflow history.
Raw workflow noise is for logs; humans need state transitions.
