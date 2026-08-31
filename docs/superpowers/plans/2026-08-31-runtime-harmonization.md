# PlanOnce Runtime Harmonization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a clean PlanOnce release with vendored Agent OS v3.0.0 and GSD Core v1.12.0 core/audit runtime sources while keeping PlanOnce as the single workflow authority.

**Architecture:** Remove the active provider-specific `.claude` installation from the distributable root, preserve it as inert audited upstream material, and update each PlanOnce skill to compile only the upstream capabilities it needs. Add deterministic validation for source pins, profile coverage, portability and workflow contracts.

**Tech Stack:** Markdown Agent Skills, Python validation/tests, JSON manifests, vendored shell/Node runtime source.

**Spec:** `docs/superpowers/specs/2026-08-31-runtime-harmonization-design.md`

## Global Constraints

- End users install PlanOnce only; Agent OS/GSD are not prerequisite installs.
- PlanOnce remains provider-neutral.
- No root active GSD hooks or machine-local paths in the release.
- Agent OS is pinned to v3.0.0 commit `809fb4e3e20451e3dd9ad9b253111776db373518`.
- GSD Core is pinned to v1.12.0 release commit `ceed559` and preserved from the installed v1.12.0 runtime.
- One PlanOnce planning authority per change.

---

### Task 1: Add failing runtime-cleanliness contracts
- [ ] Add tests that require no root `.claude`, exact upstream pins, v1.12.0 GSD runtime, core/audit profile coverage, no machine paths and per-skill runtime contracts.
- [ ] Run focused tests and confirm failure against the current copied repository.

### Task 2: Rebuild vendored upstream layout
- [ ] Export exact Agent OS v3.0.0 source from the uploaded local clone with `git archive`.
- [ ] Copy the installed GSD v1.12.0 runtime payload and core/audit surface into inert upstream directories.
- [ ] Generate recursive SHA-256 manifests and provenance documents.

### Task 3: Unify the PlanOnce workflow engine
- [ ] Add root runtime/workflow architecture documentation.
- [ ] Add self-contained `UPSTREAM_RUNTIME.md` contracts to all implementation skills.
- [ ] Update workflow instructions so PlanOnce owns shaping, execution, verification and ship gates.

### Task 4: Update release metadata and upstream tooling
- [ ] Bump version to 0.6.0 and update upstream lock to GSD v1.12.0.
- [ ] Harden `verify_upstreams.py`, `validate.py` and release manifest generation around the new layout.
- [ ] Remove stale references to GSD v1.11.0 and misleading runtime-dependency wording.

### Task 5: Verify and package
- [ ] Run unit/contract tests, validator, upstream integrity verification and static skill audit.
- [ ] Scan the release tree for `.git`, `.claude`, caches, staging directories and absolute machine paths.
- [ ] Build deterministic ZIP, extract it cleanly and rerun the full release gate from extracted contents.
