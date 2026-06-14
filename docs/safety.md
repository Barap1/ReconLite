# Safety

Only scan systems and networks you own or have explicit permission to test.

ReconLite is designed for local labs, home labs, internal authorized environments, and portfolio demonstrations. It should not be framed or used as a tool for scanning the public internet without explicit written authorization and scope.

## Safe Defaults

- Public scanning is disabled by default through `ALLOW_PUBLIC_SCAN=false`.
- Private and local scopes are the default accepted inputs.
- Demo mode is recommended for reviewers.
- Docker Compose is intended for dashboard/demo use and does not enable real Masscan scanning by default.

## Masscan Care

Masscan can generate high traffic. Use conservative rates, confirm scope, and coordinate with network owners before scanning.

Recommended safe testing targets:

- `localhost`
- A lab VM
- A private home lab subnet
- Intentionally vulnerable lab machines you own

## Public Scopes

Set `ALLOW_PUBLIC_SCAN=true` only for explicitly authorized scopes. That setting removes ReconLite's default public-scope guardrail, so the operator is responsible for confirming authorization, rate limits, and scan windows.

## Suggested Future Control

Add authorization/scope controls for approved test environments before using ReconLite in a shared team setting.
