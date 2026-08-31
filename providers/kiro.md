# Kiro adapter

- **Ask human:** use Kiro's interactive conversation surface; fall back to a normal user turn and stop for approval.
- **Read/write:** use the repository/file capabilities available to the Kiro agent.
- **Run command:** use Kiro shell/terminal execution when available.
- Fresh context: Kiro sub-agents may be used for independent bounded work when available; otherwise execute sequentially with compact handoffs.
- `npx skills` target ID: `kiro-cli`; workspace skills live in `.kiro/skills/`, global skills in `~/.kiro/skills/`.
- Default Kiro agents discover these locations automatically. A custom agent must explicitly add `skill://.kiro/skills/*/SKILL.md` (and optionally the global glob) to its `resources`.
- Kiro exposes installed skills as direct slash commands; canonical PlanOnce skill names remain portable across providers.
- **Fallback:** generic capability contract.
