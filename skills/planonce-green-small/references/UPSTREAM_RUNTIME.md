# Upstream runtime contract

**PlanOnce is the orchestration authority.** Agent OS and GSD Core are vendored engines/methodology sources used to compile this skill; they are not competing user-facing workflows.

Do not invoke raw `/agent-os:*`, `/gsd:*`, `agent-os/*`, or GSD commands as a prerequisite for this PlanOnce skill. The skill must remain self-contained when installed alone with `npx skills add --skill planonce-green-small`.

## Agent OS capabilities compiled here

- `inject-standards`
- `index-standards`

## GSD Core capabilities compiled here

- `execute-phase`
- `verify-work`
- `review`

## PlanOnce normalization

Use selective standards context, then a sequential bounded implementation slice. No second planning pass.

The upstream sources are preserved under repository `upstream/` for audit and maintenance. Runtime mechanics may differ by provider, but the PlanOnce requirements, human gates, state and evidence contract do not.
