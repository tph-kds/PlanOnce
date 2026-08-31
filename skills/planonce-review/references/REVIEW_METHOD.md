# Review method

## High-signal review

Review behavior and evidence, not formatting preferences already handled by deterministic tools. Use repository linters/formatters for mechanical concerns.

### Review lenses

1. Requirements and non-goals
2. Correctness and edge cases
3. Contracts/backward compatibility
4. Tests and verification quality
5. Security/trust boundaries
6. Data/migration/rollback
7. Failure recovery and idempotency
8. Observability and operations
9. Performance/resource/cost proportionality
10. Maintainability and repository consistency

## False-positive control

For each potential blocker ask:
- What exact code path proves this?
- Is it introduced by this diff or pre-existing?
- Is there an existing control/test that disproves it?
- Can a small reproducer or deterministic check confirm it?

Default defect-reporting threshold is 80/100 confidence. When confidence remains below that threshold, report as investigation/unverified/backlog rather than a categorical defect unless the possible impact itself requires a human stop.

## Independent review

A reviewer should not blindly trust the implementer's summary. Prefer a fresh worker with accepted requirements, diff, and verification artifacts. Without worker isolation, use a deliberate context reset/second-pass checklist.


## Production evidence

When access is authorized, prefer read-only evidence from CI, deployments, error tracking, logs/traces, alerts/SLOs, incidents, and migration state. Absence of access is not evidence of health; mark the operational dimension `UNVERIFIED`/`BLOCKED` as appropriate. Never mutate production as part of review.
