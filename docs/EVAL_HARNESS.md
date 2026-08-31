# Executable evaluation harness

PlanOnce separates deterministic framework evals from provider-dependent coding-agent evals.

## Deterministic runtime evals

`evals/runtime_cases.json` exercises routing, mandatory-Large escalation, failure routing, plan-digest mutation detection, and lock conflicts.

```bash
python scripts/run_evals.py
```

These run in the release gate and require no model/network credentials.

## Cross-agent effectiveness evals

`evals/agent_cases.json` defines provider-neutral scenarios for routing, artifact production, scope discipline and evidence honesty. `scripts/run_agent_evals.py` executes the same cases through an explicit adapter command:

```bash
python scripts/run_agent_evals.py --adapter-command "python path/to/my_codex_adapter.py"
```

The adapter receives `input.json` and must write `result.json`. See `evals/ADAPTER_PROTOCOL.md`.

External agent evals intentionally do **not** run automatically in the release gate because provider credentials, models and network availability are environment-specific. Their purpose is comparative effectiveness testing across Claude Code, Codex, OpenCode, Kilo, Kiro, Gemini CLI and other agents.

## Core metrics

- routing accuracy;
- mandatory-risk escalation correctness;
- required artifact retention;
- plan mutation/amendment honesty;
- scope-creep avoidance;
- verification honesty;
- ship-decision correctness;
- provider parity/fallback behavior.
