# Upstream runtime contract

**PlanOnce is the orchestration authority.** Agent OS and GSD Core are vendored engines/methodology sources used to compile this skill; they are not competing user-facing workflows.

Do not invoke raw `/agent-os:*`, `/gsd:*`, `agent-os/*`, or GSD commands as a prerequisite for this PlanOnce skill. The skill must remain self-contained when installed alone with `npx skills add --skill planonce-green-normal`.

## Agent OS capabilities compiled here

- `plan-product (when project context is missing)`
- `inject-standards`
- `shape-spec`

## GSD Core capabilities compiled here

- `discuss-phase`
- `plan-phase quality/reversibility checks`
- `execute-phase`
- `verify-work`
- `review`

## PlanOnce normalization

PlanOnce owns the single PLAN.md. GSD planning semantics are used as a quality/decomposition check only after requirements are fixed.

The upstream sources are preserved under repository `upstream/` for audit and maintenance. Runtime mechanics may differ by provider, but the PlanOnce requirements, human gates, state and evidence contract do not.
