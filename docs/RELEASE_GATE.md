# Release gate

A PlanOnce release is complete only when deterministic evidence from the final distributable tree passes.

## Mandatory gates

1. `python scripts/validate.py` — repository/skill/provider structure.
2. `python scripts/verify_upstreams.py` — pinned upstream integrity.
3. `python scripts/verify_runtime_profile.py` — inert GSD `core,audit` profile/runtime contract.
4. `python scripts/verify_release_manifest.py` — release-tree count/hash integrity.
5. `python scripts/audit_skill_pack.py` — static skill-pack safety/provenance audit.
6. `python scripts/run_evals.py` — executable deterministic workflow reliability cases.
7. `python -m unittest discover -s tests -p 'test_*.py' -v` — all repository, reliability, and eval-harness tests.
8. `python scripts/release_gate.py` — the combined command above.
9. Package without `.git`, active root `.claude`, caches, machine-local paths, or runtime installer state.
10. Extract the final ZIP into a clean directory and run `python scripts/release_gate.py` again from the extracted artifact.

## External coding-agent evals

Real-agent effectiveness evals are valuable but environment-specific and therefore are not a deterministic release blocker by default:

```bash
python scripts/run_agent_evals.py --adapter-command "<explicit adapter command>"
```

Record provider/model/version and results when publishing benchmark claims. Never claim cross-agent effectiveness from deterministic framework tests alone.
