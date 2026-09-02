# State contract

Each active change lives under `.planonce/work/<change>/` and can **resume** after interruption without relying on chat memory.

## Files

- `CONTEXT.md` — request, constraints, repository evidence, assumptions, selected standards.
- `DESIGN.md` — architecture/risk/rollback decisions for Large changes only.
- `PLAN.md` — the single accepted planning authority for Normal/Large changes.
- `STATE.md` — status, current phase/wave/task, approved gates, blockers, next action.
- `VERIFY.md` — fresh verification evidence, requirement coverage, gaps, residual risks.

## Formal state machine (machine-enforced)

No agent or provider may invent an undocumented transition.

```
DISCOVERY
  ↓
PLANNED
  ↓
AWAITING_APPROVAL
  ↓
APPROVED
  ↓
EXECUTING
  ↓
VERIFYING
  ↓
REVIEWING
  ↓
READY
  ↓
COMPLETE
```

`BLOCKED` may be entered from any active state when repository evidence invalidates the plan or a required dependency/verification cannot proceed. `BLOCKED` resumes only via `BLOCKED_AMEND` (smallest amendment, human re-approval).

Legacy aliases still understood: `NOT_STARTED` (≈ DISCOVERY start), `IN_PROGRESS` (≈ EXECUTING), `IMPLEMENTED_NOT_VERIFIED` (≈ VERIFYING entry), `VERIFIED` (≈ REVIEWING entry). The canonical machine set is:

`NOT_STARTED, DISCOVERY, PLANNED, AWAITING_APPROVAL, APPROVED, EXECUTING, VERIFYING, REVIEWING, IMPLEMENTED_NOT_VERIFIED, VERIFIED, READY, BLOCKED, COMPLETE`

Allowed transitions (enforced by `python scripts/reliability.py verify-state --from X --to Y`):

- `NOT_STARTED` → `DISCOVERY`, `PLANNED`, `AWAITING_APPROVAL`, `BLOCKED`
- `DISCOVERY` → `PLANNED`, `AWAITING_APPROVAL`, `BLOCKED`
- `PLANNED` → `AWAITING_APPROVAL`, `APPROVED`, `BLOCKED`
- `AWAITING_APPROVAL` → `APPROVED`, `BLOCKED`
- `APPROVED` → `EXECUTING`, `BLOCKED`
- `EXECUTING` → `VERIFYING`, `IMPLEMENTED_NOT_VERIFIED`, `BLOCKED`
- `IMPLEMENTED_NOT_VERIFIED` → `VERIFYING`, `BLOCKED`
- `VERIFYING` → `VERIFIED`, `REVIEWING`, `BLOCKED`, `EXECUTING` (FIX_REVERIFY loop)
- `VERIFIED` → `REVIEWING`, `READY`, `BLOCKED`
- `REVIEWING` → `READY`, `BLOCKED`, `EXECUTING`
- `READY` → `COMPLETE`, `BLOCKED`
- `BLOCKED` → `DISCOVERY`, `PLANNED`, `AWAITING_APPROVAL`, `APPROVED`, `EXECUTING`, `VERIFYING`, `REVIEWING`
- `COMPLETE` → (terminal)

Validate:

```bash
python scripts/reliability.py verify-state --from APPROVED --to EXECUTING
python scripts/reliability.py verify-state --from EXECUTING --to READY  # BLOCKED - invalid
```

## Status vocabulary (human-readable)

- `IMPLEMENTED_NOT_VERIFIED` means code exists but completion claims are forbidden.
- `VERIFIED` means required checks and requirement coverage have fresh evidence.
- `COMPLETE` additionally requires the final human ship gate.

## Resume rule

On resume, read `STATE.md`, the accepted plan/micro-plan, selected standards, and only the evidence needed for the next action. Do not replay the entire conversation or re-plan completed work.

## Plan amendment

Execution cannot silently modify accepted scope/design. When reality invalidates the plan: set `BLOCKED`, record evidence, propose the smallest amendment, identify affected tasks/tests/risks, obtain human approval, update the same plan with an amendment section, then resume.

## v1 machine contract — human approval (machine-enforced)

`STATE.md` uses `schema: planonce.state/v1` frontmatter and carries the accepted workflow identity, baseline/current revision, workspace mode, status and `approved_plan_digest`.

For Normal/Large, `approved_plan_digest` fingerprints the human-approved `PLAN.md` (normalized SHA-256 → `sha256:<hex>`). A mismatch on resume/execution is a blocker until it is explained; semantic changes require the amendment protocol. Small records `NOT_APPLICABLE` and keeps its approved micro-plan in `CONTEXT.md`.

Machine-enforced approval:

```yaml
approval:
  status: pending        # or approved
  plan_digest: sha256:<digest>
  approved_by: null      # human after approval
  approved_at: null
```

After human approval (via `python scripts/reliability.py approve .planonce/work/<change>` or manual digest record):

```yaml
approval:
  status: approved
  plan_digest: sha256:<digest>
  approved_by: human
  approved_at: <timestamp>
```

Also stored flat in `STATE.md` frontmatter for compatibility:

```yaml
approved_plan_digest: sha256:<digest>
approval_status: approved
approved_by: human
approved_at: 2026-09-02T00:00:00+00:00
status: APPROVED
```

Execution gate:

```bash
python scripts/reliability.py gate .planonce/work/<change> --repo .
# or roadmap alias: planonce gate execution <change>
```

Result is `PASS` or `BLOCKED` with `Required transition: BLOCKED_AMEND` when:

- approval missing / pending
- approved digest does not match current plan
- plan changed after approval

## Evidence binding (machine-enforced)

Verification evidence is bound to:

```
approved_plan_digest
revision (git HEAD or unavailable)
working_tree_digest (excluding .planonce/ or unavailable)
verification_command / result / timestamp
evidence_status: FRESH
```

A `FRESH` result becomes stale when `revision` changes OR `working_tree_digest` changes OR `approved_plan_digest` changes. Stale evidence is rejected by `validate-work` / `evidence check` / `readiness`:

```bash
python scripts/reliability.py validate-work .planonce/work/<change> --repo .
python scripts/reliability.py evidence .planonce/work/<change> --repo . --check
python scripts/reliability.py readiness .planonce/work/<change> --repo .
```

Old evidence + new code → `STALE` → re-verify before `READY`/`COMPLETE`.

## Doctor

```bash
python scripts/reliability.py doctor --repo .
# roadmap alias: planonce doctor
```

Checks `.planonce/` structure, each `work/<change>/` artifacts, and git snapshot.

## Failure route

Not every failed check invalidates the plan:

- `FIX_REVERIFY` — implementation defect while accepted direction is still valid. Fix code/tests and rerun affected evidence.
- `BLOCKED_AMEND` — repository evidence invalidates accepted scope/design/approach. Set `BLOCKED`, amend the same accepted artifact with human approval, then resume.
- `DIAGNOSE` — cause unknown; gather evidence before deciding.

This distinction avoids unnecessary re-planning while preventing silent redesign.
