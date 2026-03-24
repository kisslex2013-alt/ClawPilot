# ClawLoop Integration

ClawLoop is ClawPilot's evaluation and learning companion.
ClawPilot consumes ClawLoop outputs; it does not own the eval logic.

## Existing entrypoints

TODO: verify the exact entrypoint list from the current ClawLoop repo state.
Likely reusable surfaces include:
- full cycle
- smoke
- notify summary
- dashboard refresh
- manifest write
- disagreement report
- policy effectiveness

## Artifacts ClawPilot will read

- manifest snapshot data
- dashboard markdown
- latest delta summary
- weekly review report
- disagreement report
- policy effectiveness outputs

## v1 boundaries

ClawPilot should not rewrite ClawLoop internals in v1.
It should treat ClawLoop as the source of truth for evaluation and learning signals.

## Candidate wrapped activities

- full cycle
- smoke
- notify summary
- dashboard refresh
- manifest write
- disagreement report
- policy effectiveness
