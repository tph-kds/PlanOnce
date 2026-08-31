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
   - authentication/authorization, tenant isolation, secrets, or another security boundary;
   - payment/financial correctness;
   - destructive migration or data-loss risk;
   - public API/compatibility contract break;
   - new subsystem/architectural boundary;
   - multi-stage rollout/rollback or cross-service consistency risk.
4. Route to exactly one:
   - `planonce-green-small`
   - `planonce-green-normal`
   - `planonce-green-large`
   - `planonce-brown-small`
   - `planonce-brown-normal`
   - `planonce-brown-large`
5. Explain the choice using observed evidence, not confidence language.
6. Stop routing and begin the selected workflow; do not keep a parallel router state machine.

## Output contract

Return or record:

- `selected_skill`
- family: Greenfield/Brownfield
- size: Small/Normal/Large
- mandatory-Large triggers, if any
- short rationale/evidence
- uncertainty that the selected workflow must resolve during CONTEXT

If facts are insufficient, default to **Normal**, not Large, unless a mandatory-Large trigger is already evident.
