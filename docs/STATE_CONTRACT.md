# State contract

Each active change lives under `.planonce/work/<change>/` and can **resume** after interruption without relying on chat memory.

## Files

- `CONTEXT.md` — request, constraints, repository evidence, assumptions, selected standards.
- `DESIGN.md` — architecture/risk/rollback decisions for Large changes only.
- `PLAN.md` — the single accepted planning authority for Normal/Large changes.
- `STATE.md` — status, current phase/wave/task, approved gates, blockers, next action.
- `VERIFY.md` — fresh verification evidence, requirement coverage, gaps, residual risks.

## Status vocabulary

`NOT_STARTED` → `IN_PROGRESS` → `IMPLEMENTED_NOT_VERIFIED` → `VERIFIED` → `COMPLETE`

`BLOCKED` may occur from any active state when repository evidence invalidates the plan or a required dependency/verification cannot proceed.

- `IMPLEMENTED_NOT_VERIFIED` means code exists but completion claims are forbidden.
- `VERIFIED` means required checks and requirement coverage have fresh evidence.
- `COMPLETE` additionally requires the final human ship gate.

## Resume rule

On resume, read `STATE.md`, the accepted plan/micro-plan, selected standards, and only the evidence needed for the next action. Do not replay the entire conversation or re-plan completed work.

## Plan amendment

Execution cannot silently modify accepted scope/design. When reality invalidates the plan: set `BLOCKED`, record evidence, propose the smallest amendment, identify affected tasks/tests/risks, obtain human approval, update the same plan with an amendment section, then resume.

## v1 machine contract

`STATE.md` uses `schema: planonce.state/v1` frontmatter and carries the accepted workflow identity, baseline/current revision, workspace mode, status and `approved_plan_digest`.

For Normal/Large, `approved_plan_digest` fingerprints the human-approved `PLAN.md`. A mismatch on resume/execution is a blocker until it is explained; semantic changes require the existing amendment protocol. Small records `NOT_APPLICABLE` and keeps its approved micro-plan in `CONTEXT.md`.

## Failure route

Not every failed check invalidates the plan:

- `FIX_REVERIFY` — implementation defect while accepted direction is still valid. Fix code/tests and rerun affected evidence.
- `BLOCKED_AMEND` — repository evidence invalidates accepted scope/design/approach. Set `BLOCKED`, amend the same accepted artifact with human approval, then resume.
- `DIAGNOSE` — cause unknown; gather evidence before deciding.

This distinction avoids unnecessary re-planning while preventing silent redesign.
