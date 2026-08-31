---
name: planonce-brown-small
description: "Implement a small Brownfield fix by inspecting existing behavior and analogous code, approving one micro-plan, making the smallest coherent diff, and verifying the regression."
---

# Brownfield Small

Read `references/UPSTREAM_RUNTIME.md` for the compiled upstream capability contract.
Read `references/UPSTREAM_GUIDANCE.md` before the preflight.
Read `references/PROVIDER_GUIDANCE.md` only when runtime-specific adaptation or fallback is needed.
Use the `assets/CONTEXT.template.md`, `assets/STATE.template.md`, and `assets/VERIFY.template.md` skeletons when creating change artifacts.


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

1. **Inspect the existing implementation first**: current code path, tests, contracts, relevant standards, and nearby **analogous** code.
2. Reproduce or characterize current behavior; distinguish the observed problem from assumptions about its cause.
3. Confirm Small scope. Write a **micro-plan** in `CONTEXT.md`: root-cause evidence, intended behavior, non-goals, files, regression test, verification.
4. **Human gate — approve micro-plan.**
5. Execute in **interactive**/sequential style. Prefer a failing regression test before the fix when practical.
6. Make the smallest coherent compatible diff, then run targeted regression + repository-required checks.
7. Inspect final diff and requirement coverage; record fresh evidence in `VERIFY.md`.
8. **Security trigger:** if the diff touches auth/authz, secrets, untrusted input, tenant/data boundaries, payments, destructive operations, or AI/tool trust boundaries, run `planonce-security` on the diff.
9. Run `planonce-review` in lightweight diff-first mode; classify unrelated legacy findings as pre-existing backlog rather than expanding the fix.
10. **Human gate — ship.**

## Brownfield guardrail

**No drive-by refactors.** Preserve existing contracts/patterns unless the approved micro-plan explicitly changes them. **Do not create** a full DESIGN.md or PLAN.md for a Small fix. **Upgrade to Normal** when the fix crosses component/contract boundaries.
