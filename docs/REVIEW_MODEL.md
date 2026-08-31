# Code review and ship-readiness model

`planonce-review` is the final engineering review layer. It does **not** replace tests, security scanners, CI, or human approval; it integrates their evidence into a high-signal ship decision.

## Finding taxonomy

- `P0 BLOCKER` — critical correctness/security/data-loss/reliability failure.
- `P1 MUST_FIX` — must be resolved before ship.
- `P2 SHOULD_FIX` — important residual issue; can ship only when explicitly accepted.
- `P3 BACKLOG` — non-blocking debt/improvement.

Every finding must also record origin: `INTRODUCED`, `PRE-EXISTING`, or `UNKNOWN`.

## Ship decisions

- `READY` — no P0/P1 and all required verification evidence is fresh/pass.
- `READY_WITH_BACKLOG` — no P0/P1; P2/P3 is documented and explicitly accepted.
- `NOT_READY` — blockers or failed required checks remain.
- `BLOCKED` — necessary evidence could not be obtained.

Brownfield rule: a pre-existing problem unrelated to the change should not become a surprise blocker unless the change worsens it, depends on it, or repository release policy requires a clean baseline.

## Review independence

Prefer a reviewer with fresh context and only the accepted requirements, diff, and evidence. If the provider cannot create a fresh worker/subagent, do a deliberate second pass that does not trust the implementer's summary.
