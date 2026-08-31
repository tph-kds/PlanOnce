# Artifact schema and integrity contract

PlanOnce artifacts remain Markdown for humans and coding agents, with intentionally small scalar frontmatter for deterministic tooling.

## Schema IDs

| Artifact | Schema | Required for |
|---|---|---|
| `CONTEXT.md` | `planonce.context/v1` | all implementation workflows |
| `DESIGN.md` | `planonce.design/v1` | Large |
| `PLAN.md` | `planonce.plan/v1` | Normal/Large |
| `STATE.md` | `planonce.state/v1` | all |
| `VERIFY.md` | `planonce.verify/v1` | all |
| scope lock JSON | `planonce.lock/v1` | optional parallel execution |

Schema IDs are versioned so future PlanOnce releases can migrate artifacts explicitly instead of silently changing meaning.

## Identity

Every work artifact carries the same `change_id` and workflow family/size. `STATE.md` is the resumable machine/human checkpoint, not chat history.

## Plan integrity

After a Normal/Large plan is explicitly approved, compute a normalized SHA-256 of `PLAN.md` and write it to `STATE.md` as `approved_plan_digest`.

Normalization is deterministic:

1. normalize CRLF/CR to LF;
2. remove trailing whitespace from each line;
3. remove trailing blank lines;
4. end with exactly one LF;
5. SHA-256 the resulting UTF-8 bytes and prefix `sha256:`.

Before execution/resume, a digest mismatch means the accepted planning authority changed. Execution must stop until the change is explained and, when semantic, approved through the amendment protocol.

Small workflows do not create `PLAN.md`; they record `approved_plan_digest: NOT_APPLICABLE` and keep the approved micro-plan in `CONTEXT.md`.

## Compatibility

A future schema version must provide an explicit migration or continue reading the prior version. Unknown schema versions are not silently interpreted as current.

## Helper

Repository-level installs can run:

```bash
python scripts/reliability.py plan-digest .planonce/work/<change>/PLAN.md
python scripts/reliability.py validate-work .planonce/work/<change> --repo .
```

Targeted skill installs use the same algorithm from their bundled `references/RELIABILITY_GUIDANCE.md`.
