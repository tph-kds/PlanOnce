# Security fix method

Order priorities as follows:

1. Correctly classify vulnerable / already safe / unproven.
2. Close the broken security boundary completely.
3. Preserve legitimate behavior and compatibility.
4. Pass relevant deterministic checks.
5. Follow repository conventions.
6. Keep the patch narrowly scoped.

If an earlier property conflicts with a later one, the earlier property wins. A tiny patch that leaves an attack path open is not minimal; it is incomplete.

For high-severity issues, prefer a reviewer independent from the implementer. When no subagent is available, reset context and re-review only the finding, patch, attack path, and test evidence.
