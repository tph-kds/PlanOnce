# OpenCode adapter

- **Ask human:** use OpenCode's interactive host surface; fallback to a normal user turn and wait.
- **Read/write:** use repository/file tools available to the active agent.
- **Run command:** use shell/terminal capability.
- Fresh context: use supported agent/session delegation when available, otherwise sequential compact handoff execution.
- `npx skills` target ID: `opencode`; the current Skills CLI installs project skills through portable `.agents/skills/` and global skills under `~/.config/opencode/skills/`.
- OpenCode itself officially discovers `.opencode/skills/`, `.claude/skills/`, and `.agents/skills/`, so the portable PlanOnce path is native-compatible.
- PlanOnce must not assume GSD's native OpenCode plugin is installed.
- **Fallback:** generic capability contract.
