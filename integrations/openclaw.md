# OpenClaw Integration

OpenClaw is the execution and runtime layer for ClawPilot.
It provides tool execution, runtime state, and messaging integration.

## Expected dependencies

- workspace path
- config path
- messaging/channel integration

## Boundary

ClawPilot does not replace the OpenClaw gateway.
It coordinates work that OpenClaw executes.

## v1 integration points

- command execution
- status checks
- workspace path usage
- messaging transport reuse where practical

Unknown gateway details should stay TODO until implementation is verified.
