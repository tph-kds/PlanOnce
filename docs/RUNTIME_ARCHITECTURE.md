# Runtime Architecture

PlanOnce is the **single orchestration authority**. Agent OS and GSD Core are vendored upstream engines whose useful semantics are compiled into PlanOnce Agent Skills.

## Why the active `.claude/` install was removed

The uploaded repository contained an active GSD `core,audit` runtime at repository root with commands, agents, hooks, staging state and a machine-local `settings.local.json`. That is useful for testing GSD directly, but it is the wrong default architecture for a provider-neutral PlanOnce release because it:

- makes Claude-specific hooks run during ordinary repository activity;
- exposes `/gsd:*` and Agent OS commands beside PlanOnce, creating competing workflow entry points;
- bakes host-specific paths into a distributable project;
- makes targeted Agent Skills installs depend on files that the Skills CLI does not copy.

The clean release keeps the upstream material **inert under `upstream/`** and keeps the PlanOnce `skills/` tree self-contained.

## Authority hierarchy

1. Human request and repository instructions.
2. `.planonce/PROJECT.md`, `.planonce/POLICY.yml`, selected standards.
3. Accepted `DESIGN.md` (Large) and one accepted `PLAN.md` / micro-plan.
4. `STATE.md` execution decomposition.
5. Vendored upstream source and runtime implementation details.

Lower layers may not silently override higher layers.

## Agent OS role

Pinned Agent OS v3.0.0 provides source material for:

- standards discovery;
- standards indexing;
- selective standards injection/deployment;
- product context planning;
- spec shaping.

PlanOnce translates those capabilities into `.planonce/` artifacts instead of requiring users to run Agent OS separately.

## GSD Core role

Pinned GSD Core v1.12.0 provides source/runtime material for:

- current-state onboarding and mapping;
- discussion and assumption surfacing;
- plan-quality/reversibility checks;
- bounded execution waves and fresh-context separation;
- verification/UAT/gap closure;
- code/production review;
- phase/state/resume discipline.

The preserved `core,audit` Claude profile is available under `upstream/gsd-core/profiles/claude-core-audit/` for audit and maintenance. PlanOnce does not auto-activate its commands or hooks.

## End-user rule

End users install **PlanOnce only**. They do not need a separate Agent OS or GSD installation for the PlanOnce workflows to operate.

### What is actually installed on a private project

`npx skills add tph-kds/PlanOnce --all --copy -y` copies **only** the `skills/` tree:

```text
your-project/
  .agents/skills/planonce-*/  SKILL.md + references/ + assets/
  # (other agent dirs like .claude/skills/ when --agent '*' is used)
```

`upstream/`, `scripts/`, `docs/` and provider-local paths are **not** copied. This is intentional. Verified by `tests/test_repo.py::test_each_skill_is_self_contained_for_installers_that_copy_only_skill_dirs` and live sandbox audit (`C:\Users\ADMIN\AppData\Local\Temp\opencode\tmp-planonce-enduser-test`): all 12 `SKILL.md` resolve every `references/*.md` and `assets/*.template.*` offline, with 0 absolute paths and 0 hard `upstream/` or `scripts/` requires.

* `references/UPSTREAM_RUNTIME.md` + `UPSTREAM_GUIDANCE.md` **compile** the needed Agent OS v3.0.0 + GSD Core v1.12.0 semantics into the skill; raw sources stay in `upstream/` for PlanOnce maintenance/audit only.
* `references/RELIABILITY_GUIDANCE.md` **replaces** `scripts/reliability.py` when helpers are absent: same `planonce.*/v1` schemas, same normalized SHA-256, same `FIX_REVERIFY`/`BLOCKED_AMEND`/`DIAGNOSE` and revision-bound evidence rules. `scripts/reliability.py` is an optional convenience (`may validate`), never a prerequisite.
* Templates under `assets/` carry the canonical `change_id`/`workflow`/`schema` frontmatter, so `planonce-init` → `planonce-task` → any `planonce-green|brown-*` can create `.planonce/PROJECT.md` and `.planonce/work/<change>/{CONTEXT,PLAN,STATE,VERIFY}.md` without extra dependencies.

### Offline / Git-less fallback (also in `references/RELIABILITY_GUIDANCE.md`)

* **Plan digest** without `scripts/reliability.py` (produces identical `sha256:<hex>`):

  ```bash
  # Python (any OS, no extra deps)
  python -c "import hashlib,pathlib; p=pathlib.Path('.planonce/work/<change>/PLAN.md'); t=p.read_text(encoding='utf-8').replace('\r\n','\n').replace('\r','\n'); n='\n'.join(l.rstrip() for l in t.split('\n')).rstrip('\n')+'\n'; print('sha256:'+hashlib.sha256(n.encode()).hexdigest())"
  # Node
  node -e "const fs=require('fs'),c=require('crypto'); let t=fs.readFileSync('.planonce/work/<change>/PLAN.md','utf8').replace(/\r\n/g,'\n').replace(/\r/g,'\n'); t=t.split('\n').map(l=>l.trimEnd()).join('\n').replace(/\n+$/,'')+'\n'; console.log('sha256:'+c.createHash('sha256').update(t).digest('hex'))"
  # Git Bash / WSL
  python3 -c "import hashlib,pathlib; print('sha256:'+hashlib.sha256(open('.planonce/work/<change>/PLAN.md',encoding='utf-8').read().replace('\r\n','\n').replace('\r','\n').split('\n').__class__(''.join(l.rstrip() for l in open('.planonce/work/<change>/PLAN.md',encoding='utf-8').read().replace('\r\n','\n').replace('\r','\n').split('\n')).rstrip('\n')+'\n'.encode()).hexdigest())"
  ```

* **Revision-bound evidence** without Git: `VERIFY.md` records `revision: unavailable`, `working_tree_digest: unavailable` (see `scripts/reliability.py::workspace_snapshot` / `RELIABILITY_GUIDANCE.md`). The human ship gate still applies; stale-evidence rules simply treat `unavailable` as “re-verify when relevant files change”.
* **No drive-by requirements**: Brownfield workflows forbid unrelated refactors; Small workflows record `approved_plan_digest: NOT_APPLICABLE` and keep the micro-plan in `CONTEXT.md`.
