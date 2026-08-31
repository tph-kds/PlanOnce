---
name: planonce-review
description: "Review implemented code or a Git diff for correctness, requirement coverage, production readiness, operations, security, migrations, performance, maintainability, and evidence; separate introduced blockers from pre-existing backlog and issue a clear ship decision."
argument-hint: "[diff|path|commit]"
---

# PlanOnce Review

Use after implementation and verification, before a human ship/merge decision. It works for Greenfield and Brownfield changes and can also audit an already-running production code path.

Read `references/REVIEW_METHOD.md`; use `assets/REVIEW.template.md` for the durable report.

If `.planonce/POLICY.yml` exists, read it before issuing a ship decision. Project policy may strengthen this review but must not silently weaken higher-authority repository/company policy.

## Review contract

- **Diff-first** for a change: establish baseline/current revisions and inspect the final diff before widening scope.
- Re-read accepted **requirements**, non-goals, PLAN/DESIGN, repository standards, and verification evidence. A review is not a new planning phase.
- Review **correctness**, error handling, data/contract behavior, **tests**, maintainability, **operations**, **observability**, **migration**/rollback safety, **performance**, **security**, and user-facing acceptance as applicable.
- Separate **introduced** issues from **pre-existing** debt. Brownfield legacy issues that are unrelated and not worsened by the change belong in the **backlog**, not as surprise blockers.
- Every blocking finding needs direct evidence. Use **confidence** and challenge likely false positives before reporting them. Default to reporting defect findings only at **80/100 confidence or higher**; lower-confidence material concerns become an investigation/unverified item unless project policy requires a stop.
- Prefer an **independent** reviewer/fresh context from the implementer. **Provider fallback:** perform a second-pass clean-context review using only the accepted plan, diff, and evidence.
- A green test suite is necessary where applicable but not sufficient for production readiness.
- A **ship decision** requires **fresh evidence**. Do not inherit yesterday's test result or an agent's “done” claim.

## Reliability preflight

When `.planonce/work/<change>/` uses `planonce.* /v1` metadata, confirm the accepted-plan digest still matches and that `FRESH` verification is bound to the current revision/working-tree digest. Stale evidence is `UNVERIFIED`; if a required release check depends on it, the ship decision is `BLOCKED` until re-verification. Do not downgrade stale evidence to backlog.

## Workflow

1. Identify review scope and baseline/current revision. If Git is unavailable, explicitly list files/symbols reviewed.
2. Read accepted PlanOnce artifacts and repository instructions. Do not re-plan the feature.
3. Inspect the diff for unnecessary changes, incomplete paths, debug/dead code, generated artifacts, unsafe defaults, surprising dependencies, compatibility breaks, and missing tests.
4. Trace changed behavior into adjacent call sites/contracts where needed; review runtime failure paths rather than style alone.
5. Audit requirement/non-goal coverage against the actual implementation and tests.
6. Inspect verification evidence: exact commands, exit codes, scope, revision, and missing checks.
7. Evaluate production readiness: configuration, migrations/rollback, deployment assumptions, observability/alerts/log safety, failure recovery, performance/cost, security, and operational ownership as applicable. When authorized **read-only production evidence** is available, inspect relevant **CI** status, error **logs**, **traces**, alerts/SLOs, recent **incident** evidence, and migration/deployment health. If unavailable, mark it unverified rather than assuming operations are okay.
8. For security-sensitive changes, require a current `planonce-security` review or equivalent repository security evidence. **Security trigger** is mandatory when auth/authz, tenant isolation, secrets, payments, untrusted input, destructive data operations, or AI/tool trust boundaries changed.
9. Challenge each P0/P1 finding independently. Downgrade or remove unsupported claims; never fabricate evidence.
10. Classify findings:
   - `P0 BLOCKER` — critical correctness/security/data-loss issue.
   - `P1 MUST_FIX` — must be resolved before ship.
   - `P2 SHOULD_FIX` — important but can ship only when explicitly accepted.
   - `P3 BACKLOG` — non-blocking improvement/debt.
11. Label each finding `INTRODUCED`, **PRE-EXISTING**, or `UNKNOWN`, with evidence and owner/next action when known.
12. Write `REVIEW.md` and choose exactly one **ship decision**:
   - `READY` — no blockers; all required checks fresh/pass.
   - `READY_WITH_BACKLOG` — no P0/P1; residual P2/P3 is explicitly documented/accepted.
   - `NOT_READY` — blockers or failed required checks remain.
   - `BLOCKED` — required evidence cannot be obtained.
13. **Human gate — ship/merge remains a human decision.** Review may recommend; it never self-ships.

## Existing production audit

When reviewing already-deployed code, use **read-only** access by default and also capture known errors/incidents, failing/disabled **CI** checks, material error **logs**/**traces**, stale TODO/FIXME debt only when material, operational gaps, and observability blind spots. Do not convert the entire repository into scope: report adjacent **backlog** separately.
