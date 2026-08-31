---
name: planonce-green-large
description: "Implement a large Greenfield subsystem with architecture and one-way-door review, design/plan/phase human gates, reversible phased execution, and comprehensive production verification."
---

# Greenfield Large

Read `references/UPSTREAM_RUNTIME.md` for the compiled upstream capability contract.
Read `references/UPSTREAM_GUIDANCE.md` before design/planning.
Read `references/PROVIDER_GUIDANCE.md` only when runtime-specific adaptation or fallback is needed.
Use the templates in `assets/` for CONTEXT, DESIGN, PLAN, STATE, and VERIFY artifacts; remove irrelevant placeholder sections rather than inventing content.


## Non-negotiable contracts

- **Plan once.** One accepted planning authority per change. Execution decomposition is not a second design pass.
- **Human gate.** Stop at each defined approval point and wait for explicit approval.
- If repository evidence invalidates accepted work, set `BLOCKED` and use the **plan amendment** protocol; never silently redesign.
- Prefer **fresh context** for independent execution slices when the runtime supports it.
- **Provider fallback:** without subagents/fresh workers, execute sequentially using a compact handoff; without a native question tool, ask in normal chat and wait.
- Store resumable state under `.planonce/work/<change>/`; never depend on chat memory alone.
- Completion requires fresh **evidence**, requirement coverage, final diff review, and the human ship gate.


## Reliability layer

- **Workspace safety:** snapshot the baseline revision, branch and dirty state before edits. Preserve user changes; prefer an isolated workspace for risky/parallel work and use cooperative scope locks when multiple workers may touch the same files.
- **Approved plan digest:** Normal/Large record the accepted `PLAN.md` SHA-256 in `STATE.md` immediately after human approval. Small records `approved_plan_digest: NOT_APPLICABLE` and keeps the approved micro-plan in `CONTEXT.md`; Small must not create `PLAN.md`.
- **Revision-bound evidence:** `VERIFY.md` binds fresh evidence to the current Git revision plus working-tree digest. Any relevant code/worktree change makes prior `FRESH` evidence stale and requires re-verification.
- **Failure routing:** use `FIX_REVERIFY` when implementation is wrong but the accepted direction remains valid. Use `BLOCKED_AMEND` only when repository evidence invalidates the accepted micro-plan/`PLAN.md`/`DESIGN.md`; obtain human approval before resuming.
- When repository-level helpers are present, `scripts/reliability.py` may validate these contracts. A targeted skill install must still follow the same semantics from `references/RELIABILITY_GUIDANCE.md`.

## Workflow

1. Establish requirements/non-goals, architecture boundaries, integrations, data ownership, security/authorization model, threat model when trust/security boundaries change, operational constraints, success metrics, and rollout assumptions.
2. Create `DESIGN.md`: component/interfaces/data flow, failure modes, observability, security, compatibility, **risk**, migration/rollout and **rollback** strategy.
3. Explicitly classify costly or **one-way** decisions; a one-way door must have a decision checkpoint before implementation.
4. **Human gate — design approval.**
5. Create **exactly one** `PLAN.md` mapping requirement IDs to independently verifiable phases and bounded waves; include test strategy and rollback/verification per phase.
6. **Human gate — plan approval.**
7. Execute phase by phase. Prefer **fresh context** workers for independent waves; use provider fallback sequential handoffs otherwise.
8. At every contract/data/deployment boundary, run the phase checks and stop at a **human phase gate** with evidence and rollback readiness.
9. Any design contradiction triggers `BLOCKED` + **plan amendment** (and design amendment if architecture changes) before execution resumes.
10. Run comprehensive tests/build/lint/types/migrations/compatibility/performance/operational checks as applicable, plus user-facing acceptance validation.
11. **Security trigger — mandatory for Large:** run `planonce-security` on the final diff and any material trust/security boundary. Resolve or explicitly disposition validated Critical/High findings.
12. Audit requirements and residual risk; record fresh evidence in `VERIFY.md`.
13. Run `planonce-review` as the mandatory final production-readiness review; require `READY` or explicitly human-accepted `READY_WITH_BACKLOG`.
14. **Human gate — ship.**
