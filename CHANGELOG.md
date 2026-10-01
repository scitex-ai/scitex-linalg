# Changelog

All notable changes to `scitex-linalg` are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/).

## [0.1.6] - 2026-10-02

- Verify real optional CPU tensor statistics and pandas/NumPy/list/tensor conversion workflows; document NaN propagation and the actual geometric-median signature.
- Run native org CPU matrix controls through the same digest-verified SIF as releases; document CUDA auto-selection and the unvalidated GPU boundary.

- Declare pandas for the real core converter while retaining Torch and geometric median as optional extras; use current org runners without renaming required matrix checks.
- Preserve trusted-main license and CLA policy, and run strict complete release tests in the digest-verified, job-owned CI SIF before normal OIDC publishing.

## [Unreleased]

## [0.1.4] — 2026-05

- fix(workflows): resync integrated release pipeline from scitex-dev v0.11.20
- fix(workflows): standardize to scitex-dev canonical workflow set

## [0.1.3] — 2026-04

- feat: try_import_optional lazy-load for geometric_median ([torch] extra)
- fix(tests): clear PA-306 + PA-307 test-quality violations
- fix(deps): expand [dev] to include torch (audit-project PS210)
- fix(vendor_decorators): make torch import optional in to_numpy
- fix(api): `from __future__ import annotations`, `__version__` in `__all__`
- docs(readme): Architecture + Demo sections (PS141/PS142), uv install hint
- docs(skills): canonical installation/quick-start/python-api leaf pages
- docs: add CHANGELOG.md + CONTRIBUTING.md (PS134/PS135)
- test(audit): integrate audit-all into the test suite
- test(structure): move tests to tests/scitex_linalg/ mirror (PS302)
- chore(version): `__version__` via importlib.metadata (prevent drift)
- ci: sync-main auto-FF, docs.yml, doc-quality workflow, canonical publish-pypi

## [0.1.2] — 2026-03

- feat(skills): add SKILL.md (audit §E1); ship _skills via package-data

## [0.1.1]

- Initial CHANGELOG entry — see git log for prior history.
