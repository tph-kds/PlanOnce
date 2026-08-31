# Upstream mapping

PlanOnce is its own workflow product. Agent OS v3.0.0 and GSD Core v1.12.0 are vendored, pinned upstream engines used for auditability and to maintain the compiled PlanOnce behavior.

| PlanOnce behavior | Agent OS v3.0.0 source | GSD Core v1.12.0 source/runtime |
|---|---|---|
| Discover repository standards | `discover-standards` | brownfield current-state evidence complements discovery |
| Keep standards discoverable | `index-standards` | — |
| Select only relevant standards | `inject-standards` | context-budget / scoped-execution discipline |
| Establish product context | `plan-product` | `new-project` / discussion semantics when useful |
| Shape one accepted PlanOnce plan | `shape-spec` | `discuss-phase` + `plan-phase` quality/reversibility semantics |
| Brownfield first-pass mapping | standards discovery | `onboard` / `map-codebase` semantics from the preserved runtime |
| Execution decomposition | — | `execute-phase` wave/dependency semantics after PlanOnce approval |
| Verification + gap closure | — | `verify-work` and verifier/audit runtime support |
| Production/code review | — | `review` and `code-review` semantics |
| State/phase discipline | — | `phase`, runtime state helpers, context/wave guards |
| Security ship gate | PlanOnce-specific | GSD audit ideas may inform evidence, but PlanOnce owns `planonce-security` |

## Non-negotiable PlanOnce difference

Raw Agent OS/GSD commands do not become another user-facing orchestration layer. Once the human accepts a PlanOnce plan, upstream-derived execution decomposition may reorder/split accepted work but cannot redefine requirements or design. Conflict triggers the PlanOnce plan-amendment protocol.

See `docs/RUNTIME_ARCHITECTURE.md`, `docs/WORKFLOW_ENGINE.md`, and each implementation skill's `references/UPSTREAM_RUNTIME.md`.
