# Portable Contract Matrix

Machine-readable contract status for PlanOnce v1.0 + roadmap target. This matrix is the release goal tracker for moving critical rows from `Partial` to `Yes` (machine-enforced).

| Capability | Source | Portable | Machine Enforced | Evidence / CLI |
|---|---:|---:|---|---|
| Standards discovery | Agent OS | Yes | Partial | `planonce-init`, `standards/index.yml` |
| Brownfield mapping | GSD | Yes | Partial | `CONTEXT.md` evidence |
| One-plan authority | PlanOnce | Yes | Partial → **Target: Yes** | `gate execution` blocks on digest drift |
| Bounded waves | GSD / PlanOnce | Yes | Partial | `PLAN.md` waves, `STATE.md` |
| Plan digest | PlanOnce | Yes | **Yes** | `planonce hash-plan` / `plan-digest` → `sha256:<hex>` |
| Revision-bound evidence | PlanOnce | Yes | **Yes** | `validate-work` / `evidence check` + `VERIFY.md` binds `revision`+`working_tree_digest`+`plan_digest` |
| Human approval | PlanOnce | Yes | **Target: Yes** | `planonce approve` + `gate execution` (BLOCKED if missing/pending/mismatch) |
| State transitions | PlanOnce | Yes | **Target: Yes** | `verify-state --from --to` validates only documented transitions |
| Failure routing FIX_REVERIFY / BLOCKED_AMEND | PlanOnce | Yes | Partial → Yes | `failure-route` helper |
| Security gate | PlanOnce | Yes | Partial | `planonce-security` mandatory for Large / security-sensitive Normal (`needs_security_review`) |
| Readiness gate | PlanOnce | Yes | **Target: Yes** | `readiness` checks `FRESH` + `READY`/`COMPLETE` + approval |
| Workspace safety / scope locks | PlanOnce+GSD | Yes | **Yes** | `snapshot`, `lock-acquire`/`lock-release`, `working_tree_digest` |
| Provider fallback | PlanOnce | Yes | Partial | `references/PROVIDER_GUIDANCE.md`, `providers/*.md` |

## Release goal

Move critical rows from `Partial` to `Yes` without adding a daemon, database, Docker, or GSD/Agent OS runtime dependency. The consumer project must still need only `SKILL.md + references/ + assets/` (no `upstream/` or `scripts/` at runtime, with `RELIABILITY_GUIDANCE.md` one-liners as fallback).

## Verification

```bash
python scripts/reliability.py plan-digest .planonce/work/demo/PLAN.md
python scripts/reliability.py hash-plan .planonce/work/demo/PLAN.md
python scripts/reliability.py approve .planonce/work/demo
python scripts/reliability.py gate .planonce/work/demo --repo .
python scripts/reliability.py evidence .planonce/work/demo --repo . --check
python scripts/reliability.py readiness .planonce/work/demo --repo .
python scripts/reliability.py verify-state --from APPROVED --to EXECUTING
python scripts/reliability.py doctor --repo .
```

Portable fallbacks (when `scripts/` not copied with `npx skills add --copy`) are in `references/RELIABILITY_GUIDANCE.md` and `docs/ARTIFACT_SCHEMA.md` (identical normalized SHA-256).

See `CAPABILITY_PROVENANCE.json` for capability-level provenance and upstream impact analysis, and `docs/STATE_CONTRACT.md` for the formal state machine.
