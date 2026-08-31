# Workspace and concurrency safety

PlanOnce treats the developer's working tree as user data.

## Preflight

Before edits record, when available:

- Git baseline revision;
- current branch/detached state;
- whether relevant code is already dirty;
- selected workspace mode: current tree / worktree / provider sandbox;
- known pre-existing user changes.

Never run destructive reset/checkout/clean operations merely to make the workspace convenient for an agent.

## Isolation

- Small: current worktree is acceptable when the scope is narrow and user changes are preserved.
- Normal: isolated worktree/fresh worker is preferred when parallelism or risky overlap exists.
- Large: prefer an isolated worktree/sandbox when the runtime supports it.

Provider limitations may change the isolation mechanism, not accepted requirements or verification rigor.

## Cooperative scope locks

Parallel workers may acquire repository-relative file-scope locks under `.planonce/locks/`. Each path is normalized and stored as an atomic JSON lock with owner and expiry.

```bash
python scripts/reliability.py lock-acquire --repo . --owner worker-1 --scope src/auth.py --scope tests/test_auth.py
python scripts/reliability.py lock-release --repo . --owner worker-1 --scope src/auth.py --scope tests/test_auth.py
```

A live conflicting lock means **do not edit that scope**. Expired locks can be recovered. Partial multi-scope acquisition rolls back so workers do not strand accidental locks.

Locks are cooperative coordination, not a security boundary.
