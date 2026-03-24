# Telegram Rendering

## Why builder comes before sender

Rendering and sending are different concerns.
Builders turn structured state into chat-safe messages.
Sender integration can come later without changing the message logic.

## Message types

- live progress
- digest
- blocker
- approval request
- completion
- failure

## Anti-spam approach

- quiet mode suppresses low-value step noise
- normal mode emits meaningful transitions only
- verbose mode preserves more detail for debugging
- grouping/collapsing happens before rendering

## Preview-only rendering flow

1. take sample or persisted run data
2. apply notification policy
3. render to plain text or markdown-safe text
4. inspect output locally

## Future separation

- builder: structured data to message objects
- sender: transport to Telegram
- routing: decides what to send, when, and to whom
