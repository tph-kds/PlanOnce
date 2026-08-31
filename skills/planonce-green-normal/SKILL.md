---
name: planonce-green-normal
description: "Implement a normal Greenfield feature from exactly one approved PLAN.md, then execute it in bounded waves with provider-aware fresh context and evidence-based verification."
---

# Greenfield Normal

Read `references/UPSTREAM_RUNTIME.md` for the compiled upstream capability contract.
Read `references/UPSTREAM_GUIDANCE.md` before shaping the plan.
Read `references/PROVIDER_GUIDANCE.md` only when runtime-specific adaptation or fallback is needed.
Use the templates in `assets/` for CONTEXT, PLAN, STATE, and VERIFY artifacts; keep them concise and evidence-based.


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

1. Preflight: read repository instructions, project context, and only relevant standards.
2. Clarify observable **requirements**, acceptance criteria, non-goals, interfaces, failure behavior, and verification strategy.
3. Create **exactly one** `PLAN.md` with requirement IDs, approach, files/interfaces, tests, risks, dependencies, verification commands, and 2–5 bounded execution **waves**.
4. **Human gate — approve PLAN.md.**
5. Execute the accepted waves. Use a **fresh context** per independent wave/worker when available; otherwise use the provider fallback compact handoff.
6. Keep implementation inside accepted scope. A contradiction discovered during execution triggers `BLOCKED` + **plan amendment**.
7. Run targeted checks during waves, then full required verification and user-facing acceptance checks.
8. Audit every requirement/non-goal against the final diff and record evidence in `VERIFY.md`.
9. **Security trigger:** run `planonce-security` when the change affects trust/security boundaries or repository policy requires security review.
10. Run `planonce-review` against the accepted plan, final diff, and fresh verification evidence. Resolve P0/P1 findings or mark the work `NOT_READY`/`BLOCKED`.
11. **Human gate — ship.**
