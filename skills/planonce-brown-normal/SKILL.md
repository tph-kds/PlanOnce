---
name: planonce-brown-normal
description: "Implement a normal Brownfield feature by mapping the current implementation, accepting exactly one compatible PLAN.md, executing bounded waves, and verifying regression/contract safety."
---

# Brownfield Normal

Read `references/UPSTREAM_RUNTIME.md` for the compiled upstream capability contract.
Read `references/UPSTREAM_GUIDANCE.md` before mapping/shaping.
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

1. **Inspect the existing repository and current implementation first**: entry points, symbols, tests, interfaces/data contracts, dependencies, migration history, and **analogous** patterns.
2. Capture current-state evidence, compatibility constraints, selected standards, and assumptions in `CONTEXT.md`.
3. Clarify observable **requirements** and non-goals. Prefer established architecture unless the requested change explicitly requires otherwise.
4. Create **exactly one** `PLAN.md`: smallest compatible approach, requirement IDs, exact affected interfaces/files, regression tests, migration/security/observability impact, verification commands, bounded execution **waves**.
5. **Human gate — approve PLAN.md.**
6. Execute waves using **fresh context** where supported or the provider fallback sequential compact handoff. Do not research/design the feature again.
7. If existing-code evidence contradicts the plan, use `BLOCKED` + **plan amendment** before continuing.
8. Run regression/integration/compatibility checks plus repository gates; audit requirements against the final diff and record evidence.
9. **Security trigger:** run `planonce-security` when the change affects trust/security boundaries or repository policy requires security review.
10. Run `planonce-review` against accepted requirements, the final diff, and fresh evidence; separate introduced blockers from pre-existing backlog.
11. **Human gate — ship.**

## Brownfield guardrail

**No drive-by refactors.** Unrelated modernization is out of scope.
