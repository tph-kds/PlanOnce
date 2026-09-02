---
name: planonce-brown-large
description: "Implement a high-risk Brownfield change with deep existing-system evidence, architecture/rollback design, one-way-door gates, phased execution, and comprehensive compatibility verification."
---

# Brownfield Large

Read `references/UPSTREAM_RUNTIME.md` for the compiled upstream capability contract.
Read `references/UPSTREAM_GUIDANCE.md` before deep mapping/design.
Read `references/PROVIDER_GUIDANCE.md` only when runtime-specific adaptation or fallback is needed.
Use the templates in `assets/` for CONTEXT, DESIGN, PLAN, STATE, and VERIFY artifacts; remove irrelevant placeholder sections rather than inventing content.


## Non-negotiable contracts — critical invariants (always loaded)

- **Plan once.** One accepted planning authority per change. Execution decomposition is not a second design pass; `DESIGN.md` + exactly one `PLAN.md`.
- **Explicit human approval required.** Stop at design approval, plan approval, each phase gate, and final ship. Record `approved_plan_digest: sha256:<hex>` in `STATE.md` after plan approval. Digest is normalized SHA-256 (CRLF→LF, trim trailing whitespace, strip trailing blank lines, one LF).
- **Approved plan is immutable without amendment.** If `PLAN.md` digest != `approved_plan_digest`, execution is **BLOCKED**, required transition `BLOCKED_AMEND`. Machine gate: `python scripts/reliability.py gate .planonce/work/<change> --repo .`.
- **Evidence freshness is revision-bound.** `VERIFY.md` with `evidence_status: FRESH` is bound to `approved_plan_digest` + `revision` + `working_tree_digest` (excluding `.planonce/`). Any code/worktree/plan change makes prior `FRESH` stale → re-verify. Machine: `validate-work` / `evidence check`.
- **State transitions are formal.** `DISCOVERY→PLANNED→AWAITING_APPROVAL→APPROVED→EXECUTING→VERIFYING→REVIEWING→READY→COMPLETE`; any may go to `BLOCKED`; `BLOCKED` requires `BLOCKED_AMEND`. No invented transitions. Recovery: `FIX_REVERIFY` (implementation defect, plan valid) vs `BLOCKED_AMEND` (evidence invalidates plan) else `DIAGNOSE`.
- **One-way doors earn a human gate** before implementation; rollback strategy must be tested.
- **Fresh context** for independent execution slices when runtime supports it; else sequential compact handoff.
- **Provider fallback:** without subagents/fresh workers, execute sequentially; without ask-human tool, ask in normal chat and wait.
- **Store resumable state under `.planonce/work/<change>/`; never depend on chat memory alone.**
- **Completion requires** fresh evidence, `planonce-security` (mandatory for Large) + `planonce-review` `READY`, and human ship gate.
- **Deterministic CLI:** `planonce hash-plan`, `planonce approve`, `planonce gate execution`, `planonce evidence check`, `planonce readiness`, `planonce doctor`, `planonce verify-state`.

## Reliability layer

- **Workspace safety:** snapshot the baseline revision, branch and dirty state before edits. Preserve user changes; prefer an isolated workspace for risky/parallel work and use cooperative scope locks when multiple workers may touch the same files.
- **Approved plan digest:** Normal/Large record the accepted `PLAN.md` SHA-256 in `STATE.md` immediately after human approval. Small records `approved_plan_digest: NOT_APPLICABLE` and keeps the approved micro-plan in `CONTEXT.md`; Small must not create `PLAN.md`.
- **Revision-bound evidence:** `VERIFY.md` binds fresh evidence to the current Git revision plus working-tree digest. Any relevant code/worktree change makes prior `FRESH` evidence stale and requires re-verification. Without Git, use `revision: unavailable` / `working_tree_digest: unavailable`.
- **Failure routing:** use `FIX_REVERIFY` when implementation is wrong but the accepted direction remains valid. Use `BLOCKED_AMEND` only when repository evidence invalidates the accepted micro-plan/`PLAN.md`/`DESIGN.md`; obtain human approval before resuming.
- When repository-level helpers are present, `scripts/reliability.py` validates these contracts. A targeted skill install must still follow the same semantics from `references/RELIABILITY_GUIDANCE.md`.

## Workflow

1. **Map the existing code and implementation deeply first**: architecture, dependency/call paths, data model, public/internal APIs, tests, deployments, observability, migration history, failure boundaries, and representative **analogous** code.
2. Build `CONTEXT.md` from repository evidence: current behavior, invariants, compatibility constraints, selected standards, known risks, and unresolved unknowns.
3. Create `DESIGN.md`: target architecture, transition strategy, migration/data safety, security/authorization impact, **threat model when trust/security boundaries change**, observability, performance, **risk**, and tested **rollback** strategy.
4. Mark costly/**one-way** decisions explicitly; a one-way door earns a human decision checkpoint before implementation.
5. **Human gate — design approval.**
6. Create **exactly one** `PLAN.md` mapping requirements to reversible/independently verifiable phases and bounded waves, including compatibility/regression and rollback checks.
7. **Human gate — plan approval.** After approval run `python scripts/reliability.py approve .planonce/work/<change>` and verify `gate execution` PASS before coding.
8. Execute phase by phase using **fresh context** workers where supported; use provider fallback sequential compact handoffs otherwise. Before each phase, run `gate execution`; BLOCKED → `BLOCKED_AMEND`.
9. At each material boundary, present fresh migration/contract/test evidence and rollback readiness at a **human phase gate**.
10. If repository reality invalidates design/plan, set `BLOCKED`, record evidence, and require the smallest **plan amendment** (plus design amendment when needed) before resuming.
11. Run comprehensive regression/integration/migration/build/lint/types/performance/operational checks and user-facing acceptance validation. Re-verify after any code change (stale evidence rule).
12. **Security trigger — mandatory for Large:** run `planonce-security` on the final diff and material trust/security boundaries. Resolve or explicitly disposition validated Critical/High findings.
13. Audit every requirement/non-goal against the final diff; record residual risk and fresh evidence in `VERIFY.md` bound to revision/working_tree/plan_digest.
14. Run `planonce-review` as the mandatory final production-readiness review; separate introduced blockers from pre-existing backlog and require `READY` or explicitly human-accepted `READY_WITH_BACKLOG`. Verify `readiness` PASS.
15. **Human gate — ship.** Require `FRESH` evidence and `COMPLETE` only after human ship.

## Brownfield guardrail

**No drive-by refactors.** Do not use a large change as permission to rewrite unrelated legacy code.
