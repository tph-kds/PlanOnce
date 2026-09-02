# Workflow matrix

Choose the smallest workflow that can safely contain the change. **Escalation is one-way during a task:** discovered complexity can move Small → Normal → Large, never downward just to save tokens.

| Workflow | Use when | Planning | Human gates | Execution |
|---|---|---|---|---|
| Green Small | Localized new behavior; one logical component | Micro-plan | Approve + ship | Interactive/sequential |
| Green Normal | Bounded feature across a few units/interfaces | Exactly one `PLAN.md` | Plan + ship | Bounded waves |
| Green Large | New subsystem, significant architecture, deployment/data effects | `DESIGN.md` + exactly one `PLAN.md` | Design + plan + phase + ship | Phased waves |
| Brown Small | Localized fix in known existing flow | Inspect + micro-plan | Approve + ship | Smallest coherent diff |
| Brown Normal | Existing production feature crossing a few files/interfaces | Inspect + exactly one `PLAN.md` | Plan + ship | Bounded waves |
| Brown Large | Architectural migration/refactor or high-risk production change | Deep map + `DESIGN.md` + exactly one `PLAN.md` | Design + plan + phase + ship | Phased waves |

## Mandatory upgrade triggers

Upgrade to **Large** when any of these materially apply:

- a **one-way door** decision: rollback requires migration, breaks a published contract, or is practically irreversible;
- **authorization model change**, **tenant isolation/boundary change**, **credential/key storage architecture change**, **token claims/validation contract change**, or **cross-service authentication semantics change**;
- payment/financial correctness, destructive migration, data loss risk, cross-service consistency, or public API compatibility (including public security contract);
- a new subsystem or architectural boundary;
- rollout/rollback requires multiple deployment stages;
- the plan cannot fit into independently verifiable bounded waves without hidden assumptions.

**Security-sensitive does not automatically mean Large.** Use **Normal** when all are true: existing architecture intact, public API contract intact, authorization model unchanged, tenant boundary unchanged, credential/key architecture unchanged, blast radius bounded, rollback straightforward, regression coverage strong. Require **Large** only when changing authorization model, tenant isolation, token claims/validation, credential storage, key-management, cross-service auth semantics, public security contract, or irreversible security migration. Security-sensitive Normal flows automatically require `planonce-security` before ship.

Upgrade Small → Normal when multiple components/contracts become involved or the micro-plan stops being obviously reviewable.


## Review and security routing

| Workflow | `planonce-review` | `planonce-security` |
|---|---|---|
| Small | Lightweight diff-first gate before ship | On **security trigger** or repo policy |
| Normal | Required final review | On **security trigger** or repo policy |
| Large | Mandatory production-readiness review | **Mandatory** before final ship |

Security trigger: auth/authz, tenant isolation, credentials/secrets, payments, destructive data operations, public trust boundaries, untrusted input/content, external action authority, or AI/MCP/tool security boundaries.

## Route-only entry point

`planonce-task` is the recommended generic entry point when the user does not want to choose among six implementation workflows. It performs **classification only**, applies mandatory-Large triggers, returns one canonical `selected_skill`, and exits. It never creates `PLAN.md`/`DESIGN.md` or competes with the selected workflow's planning authority.

## Reliability requirements by size

| Size | Plan integrity | Evidence freshness | Workspace safety |
|---|---|---|---|
| Small | micro-plan in `CONTEXT.md`; `approved_plan_digest: NOT_APPLICABLE` | revision-bound `VERIFY.md` | preserve dirty user changes; lock only if parallel overlap exists |
| Normal | approved `PLAN.md` digest in `STATE.md` | revision + working-tree digest | snapshot preflight; prefer isolation for overlap/risk |
| Large | approved `DESIGN.md` + `PLAN.md` digest | revision + working-tree digest plus risk-scaled checks | prefer worktree/sandbox; cooperative locks for parallel workers |
