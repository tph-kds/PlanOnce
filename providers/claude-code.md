# Claude Code adapter

- **Ask human:** use the runtime's interactive question/approval surface when available; fallback to a normal user turn.
- **Read/write:** use repository Read/Edit/Write capabilities.
- **Run command:** use Bash/terminal capability.
- Fresh context: subagents may be used for independent waves when useful; otherwise use sequential execution.
- `npx skills` target ID: `claude-code`; current Skills CLI project path is `.claude/skills/` and global path is `~/.claude/skills/`.
- Slash presentation may expose the skill as `/planonce-*`; the canonical identity remains the skill name.
- **Fallback:** never assume a particular Claude-only tool exists; use the generic capability contract.
