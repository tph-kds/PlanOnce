# Codex adapter

- **Ask human:** use the active Codex interaction/approval surface; fallback to a normal user turn and wait.
- **Read/write:** use repository editing/file capabilities available in the active Codex environment.
- **Run command:** use shell/terminal execution.
- Fresh context: use isolated workers only when the runtime exposes them safely; otherwise execute bounded waves sequentially.
- `npx skills` target ID: `codex`; current Skills CLI uses portable `.agents/skills/` at project scope and Codex's global skills directory for `-g` installs.
- The root `.codex-plugin/plugin.json` is a secondary native surface; it points to the same canonical `skills/` tree.
- **Fallback:** generic capability contract.
