---
name: planonce-green-small
description: "Implement a small Greenfield change with selected standards, one approved micro-plan, interactive bounded execution, and fresh verification evidence."
---

# Greenfield Small

Read `references/UPSTREAM_RUNTIME.md` for the compiled upstream capability contract.
Read `references/UPSTREAM_GUIDANCE.md` when selecting standards/execution mode.
Read `references/PROVIDER_GUIDANCE.md` only when runtime-specific adaptation or fallback is needed.
Use the `assets/CONTEXT.template.md`, `assets/STATE.template.md`, and `assets/VERIFY.template.md` skeletons when creating change artifacts.


## Non-negotiable contracts — critical invariants (always loaded)

- **Plan once — micro-plan.** One accepted micro-plan in `CONTEXT.md` per change. Do not create `PLAN.md`/`DESIGN.md` for Small. Record `approved_plan_digest: NOT_APPLICABLE` in `STATE.md`.
- **Explicit human approval required.** Stop at micro-plan approval and final ship. Wait for explicit human approval.
- **Evidence freshness is revision-bound.** `VERIFY.md` with `evidence_status: FRESH` is bound to `revision` + `working_tree_digest` and `plan_digest: NOT_APPLICABLE`. Any relevant code/worktree change makes prior `FRESH` stale → re-verify. Machine: `validate-work` / `evidence check`.
- **State transitions are formal.** `DISCOVERY→PLANNED→AWAITING_APPROVAL→APPROVED→EXECUTING→VERIFYING→REVIEWING→READY→COMPLETE`; any may go to `BLOCKED`. Recovery: `FIX_REVERIFY` vs `BLOCKED_AMEND` else `DIAGNOSE`. No invented transitions.
- **Human gate.** Wait for explicit approval; never self-approve.
- **Fresh context** when supported; else sequential compact handoff.
- **Provider fallback:** without subagents/fresh workers, execute sequentially; without ask-human tool, ask in normal chat and wait.
- **Store resumable state under `.planonce/work/<change>/`; never depend on chat memory alone.**
- **Completion requires** fresh evidence, requirement coverage, lightweight `planonce-review`, `planonce-security` when security-sensitive, and human ship gate.
- **Deterministic CLI:** `planonce doctor`, `planonce evidence check`, `planonce readiness`, `planonce verify-state`.

## Reliability layer

- **Workspace safety:** snapshot the baseline revision, branch and dirty state before edits. Preserve user changes; prefer an isolated workspace for risky/parallel work and use cooperative scope locks when multiple workers may touch the same files.
- **Approved plan digest:** Normal/Large record the accepted `PLAN.md` SHA-256 in `STATE.md` immediately after human approval. Small records `approved_plan_digest: NOT_APPLICABLE` and keeps the approved micro-plan in `CONTEXT.md`; Small must not create `PLAN.md`.
- **Revision-bound evidence:** `VERIFY.md` binds fresh evidence to the current Git revision plus working-tree digest. Any relevant code/worktree change makes prior `FRESH` evidence stale and requires re-verification.
- **Failure routing:** use `FIX_REVERIFY` when implementation is wrong but the accepted direction remains valid. Use `BLOCKED_AMEND` only when repository evidence invalidates the accepted micro-plan/`PLAN.md`/`DESIGN.md`; obtain human approval before resuming via the **plan amendment** protocol.
- When repository-level helpers are present, `scripts/reliability.py` validates these contracts. A targeted skill install must still follow the same semantics from `references/RELIABILITY_GUIDANCE.md`.

## Workflow

1. Preflight: read project instructions, relevant `.planonce/PROJECT.md`, and only the standards matching this task.
2. Confirm the change is truly Small: one localized behavior/logical component, no public-contract/security/data one-way door.
3. Write a short **micro-plan** in `CONTEXT.md`: outcome, non-goal, likely files/interfaces, test, verification commands.
4. **Human gate — approve micro-plan.**
5. Execute in **interactive**/sequential style. For behavior changes, prefer RED → GREEN → REFACTOR; if test-first is impractical, state why before implementation.
6. Run targeted tests and project-required lint/type/build checks; inspect the diff for scope creep. Verify `evidence check` would PASS.
7. Record fresh evidence in `VERIFY.md`; status may move to `VERIFIED` only when required checks support it.
8. **Security trigger:** if the diff touches auth/authz, secrets, untrusted input, tenant/data boundaries, payments, destructive operations, or AI/tool trust boundaries, run `planonce-security` on the diff before review.
9. Run `planonce-review` in lightweight diff-first mode. A Small change may keep the report concise, but introduced blockers and missing required evidence still stop ship.
10. **Human gate — ship.** Require `FRESH` evidence and readiness PASS.

## Scope discipline

**Do not create** a full architecture/design document for a Small change. **Upgrade to Normal** if multiple components/contracts become involved or meaningful uncertainty appears.
