# PlanOnce External Agent Eval Adapter Protocol

`run_agent_evals.py` lets the same scenario suite exercise Claude Code, Codex, OpenCode, Kilo, Kiro, Gemini CLI, or any other coding agent without coupling PlanOnce to one vendor CLI.

## Invocation

```text
<adapter command> <input.json> <result.json>
```

PlanOnce appends the two JSON paths to the explicitly supplied `--adapter-command`; it never shells the string through a shell.

## Input JSON

```json
{
  "schema": "planonce.agent-eval-input/v1",
  "case_id": "agent-route-brown-normal",
  "prompt": "...",
  "fixture_path": "/absolute/path/to/copied/fixture"
}
```

The adapter is responsible for invoking the chosen coding agent in an isolated fixture copy and writing the result file.

## Result JSON

```json
{
  "schema": "planonce.agent-eval-result/v1",
  "selected_skill": "planonce-brown-normal",
  "artifacts": ["CONTEXT.md", "PLAN.md", "STATE.md", "VERIFY.md"],
  "ship_decision": "READY_WITH_BACKLOG",
  "claims": ["integration tests passed"]
}
```

The result is scored against provider-neutral expectations. An adapter may include extra fields; PlanOnce ignores unknown fields.

## Safety

- The adapter command is executed only when a human explicitly supplies it.
- Use disposable fixture/worktree copies; never point an eval adapter at an important repository.
- Do not expose secrets to eval agents.
- External agent evals are separate from deterministic release gates because provider credentials/network availability are environment-specific.
