# PlanOnce Workflow Engine

Every implementation workflow uses the same stage machine:

```text
CLASSIFY
   ↓
CONTEXT
   ↓
SHAPE
   ↓
APPROVE
   ↓
EXECUTE
   ↓
VERIFY
   ↓
REVIEW
   ↓
SHIP
```

## Stage contracts

### CLASSIFY

Choose Greenfield/Brownfield and the smallest safe Small/Normal/Large level. Escalation is one-way during a change.

### CONTEXT

Capture only evidence needed for the requested change. Brownfield work must inspect current behavior, tests, interfaces, migrations and analogous code before shaping.

### SHAPE

Use Agent OS-derived standards/product/spec semantics to create **one PlanOnce planning authority**. Small uses a micro-plan. Normal uses `PLAN.md`. Large uses `DESIGN.md` followed by `PLAN.md`.

### APPROVE

Human approval freezes scope and design intent. Execution may split accepted work into waves but may not invent new requirements.

### EXECUTE

Use GSD-derived bounded-wave and fresh-context discipline. If a fresh worker is unavailable, execute sequentially and persist a compact handoff in `STATE.md`.

### VERIFY

Run deterministic repository checks, regression/contract tests and user-facing verification. Missing checks stay visible as `NOT_RUN` or `BLOCKED`.

### REVIEW

Run `planonce-security` when security/trust boundaries or policy require it. Run `planonce-review` for Normal/Large and for any Small change escalated by policy/risk. Separate introduced blockers from pre-existing backlog.

### SHIP

`COMPLETE` requires fresh evidence, final requirement/diff audit and the human ship gate.

## Six implementation routes

| Workflow | Planning | Brownfield mapping | Execution | Final gates |
|---|---|---|---|---|
| Green Small | micro-plan | no | sequential bounded slice | verify + human ship |
| Green Normal | one `PLAN.md` | no | bounded waves | review + human ship |
| Green Large | `DESIGN.md` + one `PLAN.md` | no | phased waves | mandatory security/readiness + human ship |
| Brown Small | micro-plan after current-state inspection | focused | sequential bounded slice | regression verify + human ship |
| Brown Normal | one compatible `PLAN.md` | required | bounded waves | review + conditional security + human ship |
| Brown Large | `DESIGN.md` + one compatible `PLAN.md` | deep | phased waves | mandatory security/readiness + human ship |

## Plan amendment protocol

When repository evidence invalidates an accepted plan:

1. set status `BLOCKED`;
2. record the contradictory evidence;
3. propose the smallest amendment;
4. obtain explicit human approval;
5. resume from the updated accepted plan.

Never silently redesign during execution.

## Reliability control loop

Approval is followed by machine-verifiable integrity rather than trust alone:

```text
APPROVE
   ↓
plan digest / micro-plan checkpoint
   ↓
workspace snapshot + optional scope locks
   ↓
EXECUTE
   ↓
VERIFY bound to revision/worktree
   ↓
   ├─ implementation defect → FIX_REVERIFY → VERIFY
   └─ accepted direction invalid → BLOCKED_AMEND → human approval → EXECUTE
```

`planonce-task` sits before `CLASSIFY` as an optional route-only UX layer. It returns one canonical implementation skill and then exits; it never owns a competing plan.
