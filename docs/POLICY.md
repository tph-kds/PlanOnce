# Project policy

`planonce-init` may create `.planonce/POLICY.yml` from the bundled template. The policy is a small project-owned override for **when** PlanOnce requires review/security gates; it does not replace repository instructions, accepted requirements, or verification commands.

Recommended defaults:

- human plan/ship gates remain enabled;
- Normal/Large changes require `planonce-review`;
- Large changes require `planonce-security`;
- Small/Normal security review is risk-triggered;
- external scanners are never auto-installed;
- a new networked scanner asks before sending repository/dependency metadata;
- untrusted repositories or agent components are sandbox-first.

Repository policy may make gates stricter. A workflow must not silently weaken a policy just to save time/tokens. If `.planonce/POLICY.yml` conflicts with higher-authority repository/company policy, the higher-authority policy wins and the conflict is reported.

## Reliability defaults

The v0.7 template also keeps reliability behavior explicit: Normal/Large plans use an approved digest, verification is revision-bound, pre-existing user changes are preserved, Large work prefers isolation, and cooperative scope locks are used when parallel workers can overlap. Project policy may make these stricter but should not disable integrity/freshness checks merely to reduce ceremony.
