# Gemini CLI adapter

- **Ask human:** use Gemini CLI's interactive turn surface; otherwise ask normally and stop for approval.
- **Read/write:** use available workspace/file editing tools.
- **Run command:** use shell/terminal execution when available.
- Fresh context: use worker/subagent facilities only when supported; otherwise use sequential PlanOnce waves with state handoffs.
- `npx skills` target ID: `gemini-cli`; current Skills CLI uses portable `.agents/skills/` at project scope and `~/.gemini/skills/` globally.
- **Fallback:** generic capability contract.
