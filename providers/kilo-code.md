# Kilo Code adapter

- **Ask human:** use Kilo Code's interactive chat/approval surface; if no dedicated question UI is available, ask in the normal turn and stop until answered.
- **Read/write:** use the active Kilo repository/file editing capabilities.
- **Run command:** use the shell/terminal capability exposed by the active Kilo environment.
- Fresh context: use an isolated worker/mode only when the runtime supports it safely; otherwise use PlanOnce sequential waves with compact `STATE.md` handoffs.
- Skill discovery: current Kilo docs prefer `.kilo/skills/` and also load the portable `.agents/skills/` compatibility directory.
- `npx skills` target ID: `kilo`. The current Skills CLI source still contains a legacy `.kilocode/skills` mapping, so keep the portable `.agents/skills` copy available and verify skill discovery after install.
- **Fallback:** generic capability contract; provider path differences never weaken human gates or verification.
