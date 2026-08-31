---
name: planonce-security-fix
description: "Fix one explicit, evidence-backed security finding with the smallest repository-native change, preserving legitimate behavior and compatibility, then prove closure with a reproducer, regression test, security re-scan, and fresh verification."
argument-hint: "<Finding-ID>"
---

# PlanOnce Security Fix

Use only after the user explicitly asks to fix a named security issue or **Finding ID** from a current review. This is intentionally separate from `planonce-security` so scans cannot silently mutate code.

Read `references/SECURITY_FIX_METHOD.md` and provider guidance when needed. Use `assets/SECURITY_FIX.template.md` for evidence.

## Hard rules

- The request must identify an **explicit** finding. Do not turn a general security scan into automatic remediation.
- Revalidate the finding against the current revision. If the report is **stale**, re-scan/reproduce before editing.
- Make the **minimal** repository-native change that closes the security boundary. **No drive-by** cleanup.
- Do not weaken authentication, authorization, tenant isolation, validation, sandboxing, logging, or tests to obtain a green result.
- Create a focused **reproducer** or **regression test** when feasible and observe the vulnerable behavior/failure before the fix.
- Prove **legitimate behavior** still works after the fix; security by breaking intended behavior is not success.
- If the fix changes a **security boundary**, public contract, migration, or other one-way door, stop at a **human gate** before the irreversible portion.
- If required **fresh verification** cannot run, status is `BLOCKED` or `IMPLEMENTED_NOT_VERIFIED`, never fixed/complete.

## Workflow

1. Resolve the Finding ID, scope, baseline revision, current revision, and evidence.
2. Reproduce/validate the issue. If evidence no longer matches current code, mark `STALE` and return to `planonce-security`.
3. Write the smallest fix approach and expected compatibility/security invariants. This is a micro **Plan once** step, not a redesign.
4. **Human gate** only when the change introduces a one-way-door/security-contract decision; otherwise the user's explicit fix request authorizes the bounded edit.
5. Add or strengthen the regression test/reproducer first where feasible; observe it fail for the vulnerability or missing control.
6. Implement the minimal fix.
7. Run the focused reproducer/regression test, then nearby tests and repository checks.
8. Re-run the relevant security scan or semantic attack-path review. Verify both closure and legitimate behavior.
9. Use **fresh context**/independent review where supported for Critical/High findings. **Provider fallback:** perform a second pass with only the finding, patch, and evidence.
10. Record exact commands, exit codes, and remaining uncertainty in `SECURITY_FIX.md` under `.planonce/work/<change>/`.
11. Stop before commit/push/ship unless the user's surrounding workflow already authorizes those actions.

## Completion

A finding is fixed only when its original attack path/reproducer no longer succeeds, intended behavior remains valid, relevant checks pass, and evidence is fresh. Otherwise report `BLOCKED` or `IMPLEMENTED_NOT_VERIFIED`.
