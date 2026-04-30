# CLAUDE.md — Atlas

## ASIF Governance

This project is **P-15** in the ASIF portfolio (Portfolio Intelligence vertical). On every session:
1. Read `.asif/NEXUS.md` — check for `## CoS Directives` section
2. Execute any PENDING directives before other work (unless Asif overrides)
3. Write your response inline under each directive
4. Update initiative statuses in NEXUS if your work changes them
5. If you have questions for the CoS, add them under `## Team Questions` in NEXUS


## Release Protocol Enforcement (ASIF Standard, ADR-036)

When you bump the version in `pyproject.toml` (the published `atlas-portfolio` package):
1. **Tag**: `git tag vX.Y.Z && git push origin vX.Y.Z`
2. **GH Release**: `gh release create vX.Y.Z --notes-from-tag`
3. **Publish**: `python -m build && twine upload dist/*` (or via release CI)
4. **CHANGELOG**: roll `[Unreleased]` → `[vX.Y.Z] — YYYY-MM-DD` in CHANGELOG.md
5. **Docs**: update any pinned version references in README.md / docs

Pre-push hook (Layer 1, `.git/hooks/pre-push`) chains CI Gate then runs the release-protocol gate — blocks pushes with a version bump but no git tag or dated CHANGELOG section. The daily `release-protocol-check.yml` workflow (Layer 2) opens a `release-drift` issue and auto-closes on resolve. Wolf's nightly sense pass surfaces drift portfolio-wide via `===SECTION:RELEASE_DRIFT===`.

**Bypass (EMERGENCY ONLY)**: `git push --no-verify` — and document the bypass in NEXUS or HANDOFF.
## Dx3 Brain Integration
On every session start, recall relevant context from Dx3 before starting work:
- Use recall() to check for prior decisions, lessons, and patterns related to your current task
- After shipping work, use remember() to store what you learned
- The brain at dx3-cognitive MCP has context from ALL projects — use it

This is how the portfolio compounds intelligence. Your work benefits from every other team's learning.
