# Provider guidance

PlanOnce is provider-neutral. Preserve the workflow contract and map these semantic capabilities to whatever the active coding runtime exposes.

| Runtime | Exact `npx skills --agent` ID | Invocation / capability guidance |
|---|---|---|
| Claude Code | `claude-code` | Invoke the canonical `planonce-*` skill; use normal human questions/approvals, repository tools, shell, and fresh workers/subagents only when available. |
| Codex | `codex` | Invoke/select the canonical skill; use repository/shell tools and conversational approval gates. Fresh workers are optional. |
| OpenCode | `opencode` | Use the canonical skill name. Project `.agents/skills` is portable and officially discovered by OpenCode; do not assume Claude-only tools. |
| Cursor | `cursor` | Use Agent Skills/rules integration available in the client; keep approvals in chat and execution bounded to the accepted plan. |
| Gemini CLI | `gemini-cli` | Use the canonical skill name and available filesystem/shell tools; use sequential compact handoffs if worker isolation is unavailable. |
| GitHub Copilot | `github-copilot` | Use the installed skill/instructions surface; map human questions to the available chat/question UI and tool execution to the host. |
| Cline | `cline` | Use the canonical skill name; Plan/Act-style surfaces may help with human gates, but PlanOnce remains the planning authority. |
| Kilo Code | `kilo` | Current Kilo docs prefer `.kilo/skills` and also discover portable `.agents/skills`. Current Skills CLI still carries a legacy `.kilocode/skills` mapping, so verify discovery after installation. |
| Kiro | `kiro-cli` | Workspace skills live in `.kiro/skills`. Default agents auto-discover them; custom agents must include `skill://.kiro/skills/*/SKILL.md` in `resources`. |
| Roo Code | `roo` | Use the installed skill through Roo's active mode; preserve human gates and bounded scope even if mode/tool availability differs. |
| Windsurf | `windsurf` | Use the installed skill and available workspace/terminal capabilities; fall back to sequential state-backed execution when isolation is unavailable. |
| Qwen Code / Goose / OpenHands | `qwen-code` / `goose` / `openhands` | Supported through the portable Agent Skills contract; use the generic capability mapping unless a provider-specific adapter is added later. |
| Generic | — | Required capabilities are **Ask human**, **Read/write**, and **Run command**. **Fresh worker** and **Isolated workspace** are optional optimizations. |

## Fallback rules

1. No slash command: ask the agent to “use `<skill-name>` to …”.
2. No subagents/fresh workers: execute waves sequentially and write a compact handoff into `STATE.md` before context changes.
3. No native question tool: ask in normal conversation and stop until the human answers.
4. No isolated workspace: stay in the current worktree, keep diffs bounded, and never weaken verification.
5. Provider limitations may change execution mechanics, never requirements, accepted design, human gates, or evidence requirements.
6. If a provider's native skill path changes upstream, prefer the portable Agent Skills directory supported by that provider and update `providers/registry.json` in a reviewed PlanOnce release.
