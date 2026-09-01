# Workflow Reliability Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade PlanOnce from a semantic workflow pack into a machine-verifiable production engineering control layer while preserving its simple provider-neutral UX.

**Architecture:** Keep PlanOnce as the only orchestration authority. Add standard-library reliability tooling around existing Markdown artifacts: schema/version frontmatter, plan digests, Git-bound evidence freshness, cooperative file-scope locks, deterministic routing helpers, and executable evaluation protocols. Targeted Agent Skills remain self-contained and do not depend on root scripts at runtime.

**Tech Stack:** Markdown Agent Skills, Python 3 standard library, JSON, Git CLI when available, unittest.

**Spec:** `docs/RUNTIME_ARCHITECTURE.md`, `docs/WORKFLOW_ENGINE.md`, `docs/STATE_CONTRACT.md`, `docs/EVIDENCE_CONTRACT.md`, and the v1.0 requirements approved in chat.

## Global Constraints

- No daemon, database, Docker, MCP server, or mandatory third-party Python dependency.
- Preserve the six Greenfield/Brownfield implementation workflows and existing security/review skills.
- PlanOnce remains the only planning/orchestration authority; Agent OS/GSD remain pinned upstream engines/reference sources.
- Targeted skill installation must stay self-contained.
- Human approval remains required for accepted plans/designs and final ship decisions.
- Deterministic checks override agent confidence.

---

### Task 1: Reliability contracts and versioned artifacts

**Files:**
- Create: `scripts/reliability.py`
- Create: `docs/ARTIFACT_SCHEMA.md`
- Modify: implementation workflow artifact templates under `skills/*/assets/`
- Test: `tests/test_reliability.py`

**Interfaces:**
- Produces `parse_frontmatter`, `plan_digest`, `workspace_snapshot`, `working_tree_digest`, `validate_work_artifacts`, and `failure_route`.

- [ ] Add failing tests for schema parsing, normalized plan digest, stale plan detection, revision-bound verification, and FIX_REVERIFY vs BLOCKED_AMEND routing.
- [ ] Run the focused tests and confirm RED failures due to missing reliability module/metadata.
- [ ] Implement standard-library reliability primitives.
- [ ] Add schema/version frontmatter to templates without making the human-readable body noisy.
- [ ] Re-run focused tests to GREEN.

### Task 2: Automatic workflow router

**Files:**
- Create: `skills/planonce-task/SKILL.md`
- Create: `skills/planonce-task/references/PROVIDER_GUIDANCE.md`
- Create: `skills/planonce-task/references/UPSTREAM_GUIDANCE.md`
- Create: `skills/planonce-task/references/UPSTREAM_RUNTIME.md`
- Create: `skills/planonce-task/assets/ROUTING_DECISION.template.md`
- Create: `scripts/route_task.py`
- Modify: `tests/test_repo.py`
- Test: `tests/test_reliability.py`

**Interfaces:**
- Produces a route-only skill and deterministic helper returning `selected_skill`, `size`, and rationale.

- [ ] Add failing route tests for green/brown, small/normal/large, and mandatory Large triggers.
- [ ] Implement deterministic route helper.
- [ ] Implement `planonce-task` as CLASSIFY-only; it must never become a second planning authority.
- [ ] Update repository contracts for the twelfth user-facing skill.
- [ ] Verify routing tests GREEN.

### Task 3: Workspace and concurrency safety

**Files:**
- Create: `docs/WORKSPACE_SAFETY.md`
- Extend: `scripts/reliability.py`
- Test: `tests/test_reliability.py`

**Interfaces:**
- Produces `acquire_scope_locks` / `release_scope_locks`, stored under `.planonce/locks/` as atomic per-path JSON lock files.

- [ ] Add failing tests for overlapping scope rejection, expired lock recovery, partial-acquire rollback, and lock release.
- [ ] Implement atomic cooperative locks with TTL and normalized repository-relative scopes.
- [ ] Document dirty-worktree and user-change protection rules.
- [ ] Verify focused tests GREEN.

### Task 4: Executable evaluation harness

**Files:**
- Create: `evals/runtime_cases.json`
- Create: `evals/agent_cases.json`
- Create: `evals/ADAPTER_PROTOCOL.md`
- Create: `scripts/run_evals.py`
- Create: `scripts/run_agent_evals.py`
- Create: `tests/fixtures/mock_agent_adapter.py`
- Test: `tests/test_evals.py`

**Interfaces:**
- `run_evals.py` executes deterministic routing/failure/freshness cases in CI.
- `run_agent_evals.py` invokes an explicitly supplied adapter command and scores structured `result.json` output, allowing the same cases across providers without coupling PlanOnce to one CLI.

- [ ] Add failing tests for deterministic case execution and mock adapter scoring.
- [ ] Implement deterministic eval runner.
- [ ] Implement provider-neutral external-agent adapter protocol and runner.
- [ ] Verify tests GREEN.

### Task 5: Integrate reliability semantics into all workflows

**Files:**
- Modify: six implementation `SKILL.md` files
- Modify: `docs/WORKFLOW_ENGINE.md`
- Modify: `docs/STATE_CONTRACT.md`
- Modify: `docs/EVIDENCE_CONTRACT.md`
- Modify: `docs/WORKFLOW_MATRIX.md`
- Modify: `docs/TASKS_QUICKSTART.md`

**Interfaces:**
- All workflows use schema/versioned artifacts, accepted-plan digest, revision-bound evidence, explicit FIX_REVERIFY vs BLOCKED_AMEND branching, and workspace safety.

- [ ] Add repository contract tests requiring these semantics in each implementation workflow.
- [ ] Update Small/Normal/Large workflows with risk-scaled use of the reliability layer.
- [ ] Keep Small lightweight: no unnecessary PLAN.md/DESIGN.md.
- [ ] Verify contract tests GREEN.

### Task 6: Release, compatibility, and durability

**Files:**
- Modify: `VERSION`, `CHANGELOG.md`, `README.md`, `AGENTS.md`, `docs/ROADMAP.md`, `docs/RELEASE_GATE.md`
- Modify: plugin manifests/version metadata as applicable
- Modify: `scripts/release_gate.py`
- Modify: `RELEASE_MANIFEST.json`

**Interfaces:**
- Release gate runs deterministic runtime evals and all unit/contract tests.

- [ ] Bump to `0.7.0` and document migration/additive compatibility.
- [ ] Add deterministic eval runner to release gate.
- [ ] Run full validation, upstream integrity, runtime profile, release manifest, static audit, deterministic evals, and all tests.
- [ ] Package a cache-free deterministic ZIP.
- [ ] Extract the ZIP to a clean directory and run the release gate again from the extracted artifact.
