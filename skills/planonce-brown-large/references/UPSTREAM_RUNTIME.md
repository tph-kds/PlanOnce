# Upstream runtime contract

**PlanOnce is the orchestration authority.** Agent OS and GSD Core are vendored engines/methodology sources used to compile this skill; they are not competing user-facing workflows.

Do not invoke raw `/agent-os:*`, `/gsd:*`, `agent-os/*`, or GSD commands as a prerequisite for this PlanOnce skill. The skill must remain self-contained when installed alone with `npx skills add --skill planonce-brown-large`.

## Agent OS capabilities compiled here

- `discover-standards`
- `index-standards`
- `inject-standards`
- `plan-product when product intent is missing`
- `shape-spec`

## GSD Core capabilities compiled here

- `onboard semantics`
- `map-codebase semantics`
- `discuss-phase`
- `plan-phase reversibility checks`
- `phase`
- `execute-phase`
- `verify-work`
- `review`
- `code-review`

## PlanOnce normalization

Deep brownfield work requires current-state mapping, DESIGN.md, migration/rollback analysis, security/readiness gates and phased evidence before ship.

The upstream sources are preserved under repository `upstream/` for audit and maintenance. Runtime mechanics may differ by provider, but the PlanOnce requirements, human gates, state and evidence contract do not.
