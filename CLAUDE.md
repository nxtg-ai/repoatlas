# CLAUDE.md — Atlas

Atlas is a public portfolio-intelligence CLI for scanning multiple repositories, scoring project health, and surfacing cross-project engineering patterns.

## Development Rules

- Preserve the public CLI contract documented in `README.md`.
- Keep scans local-first and deterministic where possible.
- Do not add telemetry or network calls without an explicit product decision and documentation update.
- Run tests, linting, and package checks before release changes.
- Keep version metadata, changelog entries, tags, and published package versions aligned.

## Public / Private Boundary

This is a public repository. Do not commit organization-internal operating context, private portfolio state, machine topology, local absolute paths, cross-project memory configuration, internal agent hooks, credentials, or generated private reports.

Use synthetic project names and synthetic fixture data in examples and tests. Public documentation should describe Atlas product behavior only.

## Release Discipline

When changing the published package version:
1. update version metadata and changelog together;
2. run the full test suite;
3. create the corresponding git tag and GitHub release;
4. publish through the supported package-release flow;
5. verify the published version after release.
