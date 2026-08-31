# GitHub Copilot adapter

- **Ask human:** use the active chat/question/approval UI; fallback to a normal user turn and wait.
- **Read/write:** use repository editing capabilities exposed by the active Copilot environment.
- **Run command:** use terminal/command execution when the host allows it.
- Fresh context: use delegated workers only when available and scoped; otherwise execute sequentially.
- `npx skills` target ID: `github-copilot`; current Skills CLI uses portable `.agents/skills/` at project scope and `~/.copilot/skills/` globally.
- **Fallback:** generic capability contract.
