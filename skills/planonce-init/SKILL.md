---
name: planonce-init
description: "Initialize PlanOnce project context by discovering durable repository standards, exact verification commands, architecture boundaries, and provider capabilities with human confirmation."
---

# PlanOnce Init

Use once when adopting PlanOnce, and refresh only when durable project conventions materially change.

Read `references/UPSTREAM_GUIDANCE.md` before discovery.
Read `references/PROVIDER_GUIDANCE.md` only when runtime-specific adaptation or fallback is needed.
Use `assets/PROJECT.template.md`, `assets/STANDARDS_INDEX.template.yml`, and `assets/POLICY.template.yml` as the artifact skeletons; adapt content to the repository rather than copying placeholders blindly.

## Goal

Create a lean `.planonce/` context future workflows can trust without installing Agent OS or GSD.

## Steps

1. Read repository instructions (`AGENTS.md` or equivalent), README, architecture docs, build/test configuration, and **representative** code/tests.
2. Determine whether the project is Greenfield or Brownfield and identify the main verification commands actually supported by the repo.
3. For Brownfield, inspect existing patterns before writing any standards; never replace reality with generic best practice.
4. Discover only durable, recurring, **non-obvious** standards: unusual/opinionated/tribal patterns, architecture boundaries, error/API/data conventions, testing rules, security constraints.
5. Ask the **human** to confirm each proposed standard and its important exception/why.
6. Create `.planonce/PROJECT.md` with purpose, stack, architecture boundaries, exact **verification commands**, Definition of Done, and detected provider capability/fallback notes.
7. Create `.planonce/POLICY.yml` with the smallest explicit review/security/network/human-gate policy that matches repository or company requirements. Never weaken an existing higher-authority policy.
8. Create concise `.planonce/standards/*.md` and `.planonce/standards/index.yml`; the **index** must describe each standard well enough for selective loading.
9. Report what was created and what remains unknown. Never mark uncertain assumptions as standards.

## Token discipline

Do not document generic framework knowledge or obvious code. One concept per standard; lead with the rule; load standards selectively later.
