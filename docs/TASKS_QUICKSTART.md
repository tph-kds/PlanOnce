# PlanOnce task quick start

Use the smallest implementation workflow that safely contains the change, then run the cross-cutting gates that apply.

## Implementation

```text
/planonce-green-small     /planonce-brown-small
/planonce-green-normal    /planonce-brown-normal
/planonce-green-large     /planonce-brown-large
```

If slash commands are not exposed, invoke the exact skill name in natural language.

## Security and review

```text
/planonce-security [diff|codebase|path|commit]
/planonce-security-fix <Finding-ID>
/planonce-review [diff|path|commit]
/planonce-skill-audit <candidate-skill-or-plugin>
```

Recommended normal production flow:

```text
implementation workflow
  → deterministic verification
  → planonce-security when triggered by risk/policy
  → planonce-review
  → fix blockers explicitly
  → re-run affected gates
  → human ship decision
```

Large changes always include security + production-readiness review. Small/Normal changes trigger security when auth/authz, tenant isolation, credentials, payments, destructive data operations, untrusted inputs/actions, public trust boundaries, or AI/MCP/tool authority are involved.

## Recommended v0.7 entry point

When you do not want to choose a workflow manually:

```text
Use planonce-task to implement <your change>.
```

The router returns one `selected_skill` and hands off. It does not plan or execute.

For repository-level diagnostics:

```bash
python scripts/route_task.py --existing --size normal
python scripts/reliability.py snapshot .
python scripts/reliability.py validate-work .planonce/work/<change> --repo .
```
