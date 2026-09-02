# PlanOnce Reliability Guidance

This skill remains self-contained even when installed without repository-level helper scripts. Apply these contracts directly.

## Artifact schemas

Use the frontmatter shipped in this skill's templates. Preserve the `planonce.*/v1` schema identifiers and `change_id`/`workflow` identity across the change.

## Approved plan digest

Normal/Large: after the human approves `PLAN.md`, normalize CRLF/CR to LF, remove trailing whitespace from every line, remove trailing blank lines, add one final newline, then compute SHA-256. Record it as `sha256:<hex>` in `STATE.md` under `approved_plan_digest`. Before each execution wave, confirm the current plan has the same digest.

Small: do not create `PLAN.md`; set `approved_plan_digest: NOT_APPLICABLE` and keep the approved micro-plan in `CONTEXT.md`.

## Revision-bound evidence

A `FRESH` `VERIFY.md` records:

- `revision`: Git `HEAD` when Git is available;
- `working_tree_digest`: digest of relevant tracked/untracked worktree changes excluding `.planonce/`;
- `plan_digest`: accepted plan digest, or `NOT_APPLICABLE` for Small.

If code, tests, configuration, migrations, or another relevant worktree input changes, previous verification becomes stale. Re-run affected checks before claiming `VERIFIED` or `COMPLETE`.

## Failure route

- `FIX_REVERIFY`: implementation/test defect; accepted scope/design still valid. Fix the implementation and re-run affected evidence without a plan amendment.
- `BLOCKED_AMEND`: repository evidence proves the accepted micro-plan/plan/design is invalid or unsafe. Set `BLOCKED`, record evidence, propose the smallest amendment, obtain human approval, update the same artifact, then resume.
- `DIAGNOSE`: failure cause is not yet known. Gather evidence before choosing either path.

## Offline fallback commands (no scripts/ required)

Identical to `scripts/reliability.py` — use when helper scripts were not copied with `npx skills add`.

```bash
# Python (any OS) — normalized SHA-256 of PLAN.md
python -c "import hashlib,pathlib; t=pathlib.Path('.planonce/work/<change>/PLAN.md').read_text(encoding='utf-8'); t=t.replace(chr(13)+chr(10),chr(10)).replace(chr(13),chr(10)); n=chr(10).join(l.rstrip() for l in t.split(chr(10))).rstrip(chr(10))+chr(10); print('sha256:'+hashlib.sha256(n.encode('utf-8')).hexdigest())"
# Node (any OS)
node -e "const fs=require('fs'),c=require('crypto'); let t=fs.readFileSync('.planonce/work/<change>/PLAN.md','utf8').replace(/\r\n/g,'\n').replace(/\r/g,'\n'); t=t.split('\n').map(l=>l.trimEnd()).join('\n').replace(/\n+$/,'')+'\n'; console.log('sha256:'+c.createHash('sha256').update(t).digest('hex'))"
```

For revision-bound evidence without Git, record `revision: unavailable` and `working_tree_digest: unavailable` in `VERIFY.md` and re-verify when relevant files change.

## Workspace safety

Record baseline revision/branch/dirty state. Never reset or overwrite pre-existing user changes. For parallel workers, use repository-relative cooperative scope locks under `.planonce/locks/` when available; conflicting ownership is a blocker, not permission to overwrite. Prefer isolated worktrees for Large/risky work when supported.
