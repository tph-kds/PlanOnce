# Generic Agent Skills runtime

PlanOnce is capability-based. Map the workflow to whatever tools the runtime exposes.

| Capability | Preferred | Fallback |
|---|---|---|
| **Ask human** | Native interactive question/approval tool | Stop and ask in normal chat; do not continue until answered |
| **Read/write** | Repository read/edit tools | Standard filesystem tools |
| **Run command** | Shell/terminal tool | Ask the human to run the exact command and provide output |
| Fresh worker | Subagent/fresh context | Sequential execution with compact handoff |
| Isolated workspace | Worktree/sandbox | Require a clean working tree and scoped diff discipline |

Extended `npx skills` targets currently tracked by PlanOnce include Qwen Code (`qwen-code`), Goose (`goose`), and OpenHands (`openhands`). They use this generic adapter until PlanOnce has a provider-specific reason to specialize their execution mapping.

**Fallback:** a provider limitation never removes a human gate or verification requirement.
