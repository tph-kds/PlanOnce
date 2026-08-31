# Evidence contract

PlanOnce follows **evidence before completion**.

Every verification item in `VERIFY.md` should record:

- requirement or risk being verified;
- exact **command** or manual/UAT procedure;
- **scope** of the check (targeted test, package, full repo, migration, API, etc.);
- fresh result and **exit code** when a command is used;
- failures/warnings and whether they are introduced by this change;
- requirement coverage status: PASS / FAIL / BLOCKED / NOT_APPLICABLE;
- any **unverified** area and why it could not be verified.

A previous run, model confidence, lint success, or an executor's success message is not a substitute for the required fresh check.

Before ship, compare the accepted requirements/non-goals against the final diff and record any residual risk explicitly.

## Revision-bound freshness

`VERIFY.md` uses `schema: planonce.verify/v1` and binds `FRESH` evidence to:

- `revision` — current Git `HEAD` when available;
- `working_tree_digest` — relevant tracked/untracked worktree state excluding `.planonce/` bookkeeping;
- `plan_digest` — accepted plan digest or `NOT_APPLICABLE` for Small.

A relevant code/config/test/migration change invalidates prior `FRESH` evidence. Re-run the affected checks; do not carry a previous PASS forward by assertion.

Repository-level installs can check this with:

```bash
python scripts/reliability.py validate-work .planonce/work/<change> --repo .
```
