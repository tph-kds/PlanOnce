# Production quality model

PlanOnce treats the coding agent as an execution engine inside an engineering control system.

## Required behaviors

- inspect before modify, especially brownfield;
- explicit requirements/non-goals and architecture boundaries;
- smallest coherent diff and no unrelated refactor;
- tests first for behavior changes when practical; exceptions must be explicit;
- deterministic checks override confidence;
- security, migration, compatibility, observability and rollback scaled to risk;
- fresh-context execution where it improves reliability, with sequential fallback;
- no completion claim without fresh evidence;
- human approval at planning/one-way/ship boundaries.

## Anti-slop signals

Stop or escalate when the agent is guessing repository behavior, creating parallel abstractions without evidence, broadening scope, rewriting tests to fit implementation, skipping verification, or claiming success from static inspection alone.
