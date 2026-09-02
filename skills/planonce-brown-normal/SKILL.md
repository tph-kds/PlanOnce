---
name: planonce-brown-normal
description: "Implement a normal Brownfield feature by mapping the current implementation, accepting exactly one compatible PLAN.md, executing bounded waves, and verifying regression/contract safety."
---

# Brownfield Normal

Read `references/UPSTREAM_RUNTIME.md` for the compiled upstream capability contract.
Read `references/UPSTREAM_GUIDANCE.md` before mapping/shaping.
Read `references/PROVIDER_GUIDANCE.md` only when runtime-specific adaptation or fallback is needed.
Use the templates in `assets/` for CONTEXT, PLAN, STATE, and VERIFY artifacts; keep them concise and evidence-based.


## Non-negotiable contracts — critical invariants (always loaded)

- **Plan once — one planning authority.** Exactly one `PLAN.md` per change. Execution decomposition is not a second design pass; never re-plan after approval.
- **Explicit human approval required.** Stop at `PLAN.md` approval and final ship. Record `approved_plan_digest: sha256:<hex>` in `STATE.md` immediately after human says approved. `approved_plan_digest` is normalized SHA-256 (CRLF→LF, trim trailing whitespace, strip trailing blank lines, end with one LF).
- **Approved plan is immutable without amendment.** If current `PLAN.md` digest != `approved_plan_digest`, execution is **BLOCKED** and required transition is `BLOCKED_AMEND` (smallest amendment, re-approval). Machine gate: `python scripts/reliability.py gate .planonce/work/<change> --repo .` or `planonce gate execution <change>`.
- **Evidence freshness is revision-bound.** `VERIFY.md` with `evidence_status: FRESH` is bound to `approved_plan_digest` + `revision` (Git HEAD) + `working_tree_digest` (tracked+untracked excluding `.planonce/`). Any relevant code/worktree change or plan change makes prior `FRESH` stale → re-verify. Machine gate: `python scripts/reliability.py validate-work .planonce/work/<change> --repo .` / `evidence check`.
- **State transitions are formal.** Allowed: `DISCOVERY→PLANNED→AWAITING_APPROVAL→APPROVED→EXECUTING→VERIFYING→REVIEWING→READY→COMPLETE`; any state may go to `BLOCKED`; `BLOCKED` requires `BLOCKED_AMEND` before resuming. No agent may invent a transition. `FIX_REVERIFY` (implementation defect, plan still valid) vs `BLOCKED_AMEND` (evidence invalidates plan) are the only recovery routes; else `DIAGNOSE`.
- **Human gate.** Wait for explicit approval; never self-approve.
- **Fresh context** for independent waves when runtime supports it; else sequential compact handoff.
- **Provider fallback:** without subagents/fresh workers, execute sequentially; without ask-human tool, ask in normal chat and wait.
- **Store resumable state under `.planonce/work/<change>/`; never depend on chat memory alone.**
- **Completion requires** fresh evidence, requirement coverage, `planonce-review` (mandatory for Normal), `planonce-security` when security-sensitive, and human ship gate.
- **Deterministic CLI (when available):** `planonce hash-plan`, `planonce approve`, `planonce gate execution`, `planonce evidence check`, `planonce readiness`, `planonce doctor`, `planonce verify-state`.

## Reliability layer

- **Workspace safety:** snapshot the baseline revision, branch and dirty state before edits. Preserve user changes; prefer an isolated workspace for risky/parallel work and use cooperative scope locks when multiple workers may touch the same files.
- **Approved plan digest:** Normal/Large record the accepted `PLAN.md` SHA-256 in `STATE.md` immediately after human approval. Small records `approved_plan_digest: NOT_APPLICABLE` and keeps the approved micro-plan in `CONTEXT.md`; Small must not create `PLAN.md`. Use `python scripts/reliability.py plan-digest` or `hash-plan` (identical to `references/RELIABILITY_GUIDANCE.md` one-liners when scripts absent).
- **Revision-bound evidence:** `VERIFY.md` binds fresh evidence to the current Git revision plus working-tree digest. Any relevant code/worktree change makes prior `FRESH` evidence stale and requires re-verification. Without Git, use `revision: unavailable` / `working_tree_digest: unavailable` and re-verify when relevant files change.
- **Failure routing:** use `FIX_REVERIFY` when implementation is wrong but the accepted direction remains valid. Use `BLOCKED_AMEND` only when repository evidence invalidates the accepted micro-plan/`PLAN.md`/`DESIGN.md`; obtain human approval before resuming.
- When repository-level helpers are present, `scripts/reliability.py` validates these contracts. A targeted skill install must still follow the same semantics from `references/RELIABILITY_GUIDANCE.md`.

## Workflow

1. **Inspect the existing repository and current implementation first**: entry points, symbols, tests, interfaces/data contracts, dependencies, migration history, and **analogous** patterns.
2. Capture current-state evidence, compatibility constraints, selected standards, and assumptions in `CONTEXT.md`.
3. Clarify observable **requirements** and non-goals. Prefer established architecture unless the requested change explicitly requires otherwise.
4. Create **exactly one** `PLAN.md`: smallest compatible approach, requirement IDs, exact affected interfaces/files, regression tests, migration/security/observability impact, verification commands, bounded execution **waves**.
5. **Human gate — approve PLAN.md.** After approval run `python scripts/reliability.py approve .planonce/work/<change>` or compute `planonce hash-plan` and record digest; verify `gate execution` is PASS before coding.
6. Execute waves using **fresh context** where supported or the provider fallback sequential compact handoff. Do not research/design the feature again.
7. Before each wave, run `gate execution`; if BLOCKED, follow `BLOCKED_AMEND` (do not silently edit PLAN.md).
8. If existing-code evidence contradicts the plan, use `BLOCKED` + **plan amendment** before continuing.
9. Run regression/integration/compatibility checks plus repository gates; audit requirements against the final diff and record evidence. Evidence is stale after code change → re-run.
10. **Security trigger:** run `planonce-security` when the change is security-sensitive (auth, tenant, credentials, payment, destructive data, trust boundary) or repo policy requires; Normal security-sensitive still requires this gate before ship.
11. Run `planonce-review` against accepted requirements, the final diff, and fresh evidence; separate introduced blockers from pre-existing backlog.
12. **Human gate — ship.** Require `VERIFY.md` `FRESH` bound to current revision/working_tree/plan_digest and `readiness` PASS.

## Brownfield guardrail

**No drive-by refactors.** Unrelated modernization is out of scope.
