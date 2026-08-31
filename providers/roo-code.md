# Roo Code adapter

- **Ask human:** use Roo Code's interactive chat/approval surface; otherwise stop and ask in normal conversation.
- **Read/write:** use repository/file tools exposed by the active Roo mode.
- **Run command:** use terminal/shell execution when the active mode permits it.
- Fresh context: use delegated modes/workers only if they preserve the accepted PlanOnce scope; otherwise use sequential bounded waves.
- `npx skills` target ID: `roo`; current Skills CLI maps project skills to `.roo/skills/` and global skills to `~/.roo/skills/`.
- **Fallback:** generic capability contract.
