# Telegram Direct Sender

## Purpose

Provide an explicit, opt-in direct Telegram sender for local and controlled live sends.

## Explicit opt-in rule

Live sending only happens when `telegram_direct` transport is selected and `--live` is explicitly provided.

## Why live send is not default

Accidental network sends are worse than a boring preview. The default remains preview or local file log.

## Preview vs live

- preview: render and inspect only
- live: explicit Bot API send attempt

## Required config

- telegram bot token
- telegram chat id
- optional API base
- send timeout

## Safe command order

1. `python -m clawpilot.cli show-transport-mode`
2. `python -m clawpilot.cli show-telegram-target`
3. `python -m clawpilot.cli send-telegram-progress`
4. `python -m clawpilot.cli send-telegram-progress --live`

## Not implemented

- inbound replies
- routing integration
- daemonization
