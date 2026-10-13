# Upstream-based Hermes with reviewed mission intake

Base: official NousResearch Hermes Agent v0.21.7, commit
`71d34bad1045610252eda02ee79549436896e784`, under its unchanged MIT LICENSE.
This user-owned fork is the application base. The optional private native
extension is versioned separately in `roberttop101/hermes-execution-control`.
Its immutable pin is in `execution-control.json`; install only in an explicitly
chosen profile with upstream's plugin installer. The private repository's README
documents review, limits, tests, rollback and the full custom-to-upstream matrix.

The extension adds bounded reviewed mission plans, offline business draft packs,
verification contracts and recoverable handoff as blocked native Kanban cards.
It reuses native CLI/skills/dashboard and task APIs. It does not start workers or
grant permission to perform external actions. Native execution, providers,
fallback, sessions, search, memory, approvals and Kanban remain the base runtime.

Existing custom product repositories and the installed dirty app are retained.
This is a tested first phase, not complete hosted multi-tenant parity. Account/
workspace RBAC, custom scored model routing and production supervision require
separate work. No production deployment is performed.

The fork also patches inherited npm dependencies against these advisories:
[brace-expansion](https://github.com/advisories/GHSA-q2hr-2g5m-vwhr),
[source-map-js](https://github.com/advisories/GHSA-68fv-2mgg-jv7q),
[yaml](https://github.com/advisories/GHSA-48c2-rrv3-qjmp).
The Linux/systemd-specific native test now carries upstream's platform marker.
No agent-loop or runtime-core code is changed.

Fork CI is intentionally limited to `native-base.yml`; inherited upstream
release/deploy workflows remain disabled. Native-extension CI in the private
repository validates its real browser and native API behavior on the pinned
official release. No images/packages are published by these new workflows.

Rollback the fork patches through a normal revert PR; disable the extension and
retain its ledger and native board. Do not rewrite the original custom checkout
or erase native task history.
