---
name: planonce-task
description: "Classify a software change and route it to the smallest safe PlanOnce Greenfield or Brownfield workflow without creating a competing plan."
---

# PlanOnce Task Router

This skill is **CLASSIFY ONLY**. It chooses the canonical implementation workflow; it does not implement, design, or plan the change.

Read `references/UPSTREAM_GUIDANCE.md` for the pinned methodology boundary.
Read `references/PROVIDER_GUIDANCE.md` only when invocation syntax differs by runtime.
Use `assets/ROUTING_DECISION.template.md` when a durable routing record is useful.

## Authority boundary

- **Do not plan** the requested feature in this skill.
- **Do not create** `PLAN.md` or `DESIGN.md` here.
- **Do not invoke raw** Agent OS or GSD commands as a second workflow authority.
- Return one `selected_skill` and a short evidence-based rationale, then hand off to that canonical PlanOnce workflow.

## Classification

1. Inspect just enough repository context to answer whether this is primarily **Greenfield** or **Brownfield**.
2. Estimate the smallest safe size: **Small**, **Normal**, or **Large**.
3. Apply **mandatory Large** triggers before honoring a smaller size:
   - one-way/costly decision;
   - **authorization model change**, **tenant isolation/boundary change**, **credential/key storage architecture change**, **token claims/validation contract change**, **cross-service authentication semantics change**;
   - payment/financial correctness;
   - destructive migration or data-loss risk;
   - public API/compatibility contract break (including public security contract);
   - new subsystem/architectural boundary;
   - multi-stage rollout/rollback or cross-service consistency risk.
   - **Security-sensitive does not automatically mean Large.** Use **Normal** when all are true: existing architecture intact, public API contract intact, authorization model unchanged, tenant boundary unchanged, credential/key architecture unchanged, blast radius bounded, rollback straightforward, regression coverage strong. Require **Large** only when changing authorization model, tenant isolation, token claims/validation, credential storage, key-management, cross-service auth semantics, public security contract, or irreversible security migration.
4. Security-sensitive Normal flows **automatically require `planonce-security`** review before ship; Large always requires `planonce-security` + `planonce-review`.
5. Route to exactly one:
   - `planonce-green-small`
   - `planonce-green-normal`
   - `planonce-green-large`
   - `planonce-brown-small`
   - `planonce-brown-normal`
   - `planonce-brown-large`
6. Explain the choice using observed evidence, not confidence language.
7. Stop routing and begin the selected workflow; do not keep a parallel router state machine.

## Output contract

Return or record:

- `selected_skill`
- family: Greenfield/Brownfield
- size: Small/Normal/Large
- mandatory-Large triggers, if any
- short rationale/evidence
- uncertainty that the selected workflow must resolve during CONTEXT

If facts are insufficient, default to **Normal**, not Large, unless a mandatory-Large trigger is already evident.
