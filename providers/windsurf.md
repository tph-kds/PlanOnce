# Windsurf adapter

- **Ask human:** use the interactive conversation/approval surface; fall back to a normal user turn and wait.
- **Read/write:** use workspace editing capabilities available in Windsurf.
- **Run command:** use terminal/shell execution when available.
- Fresh context: delegate only when the active workflow supports safely isolated work; otherwise keep execution sequential and state-backed.
- `npx skills` target ID: `windsurf`; current Skills CLI maps project skills to `.windsurf/skills/` and global skills to `~/.codeium/windsurf/skills/`.
- **Fallback:** generic capability contract.
