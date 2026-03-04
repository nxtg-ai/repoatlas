# nxtg-atlas — Go-To-Market & Revenue Plan

## Product

**nxtg-atlas** — Portfolio intelligence CLI for AI engineering teams.
Scan repos, score health, find cross-project patterns nobody else sees.

- **PyPI**: https://pypi.org/project/nxtg-atlas/
- **GitHub**: https://github.com/nxtg-ai/repoatlas
- **Install**: `pip install nxtg-atlas`

## Market Position

**Blue ocean.** Zero direct competitors in multi-project AI portfolio intelligence.

- Every tool (Cursor, Copilot, Claude Code) operates inside ONE repo
- Nobody sees cross-project patterns — shared deps, version mismatches, health gaps
- 72% of enterprises use multi-agent architectures (Gartner 2026)
- Market: $8.5B dev tools (2026) → $35B (2030)

## Revenue Model — Sponsorware

**100% free. No tiers, no limits, no feature gates.** Everything ships to everyone.

Sustainability through voluntary sponsorship via [Polar.sh](https://polar.sh/nxtg-ai/repoatlas).

**Why sponsorware (not open core)**:
- Developer trust — no friction, no "you need Pro for that" moments
- Viral loop — maximum adoption → word of mouth → organic sponsors
- Comparable: LazyGit, Helix, Zoxide — free tools with sponsor pages that work
- Every user gets the full product. Sponsors get gratitude, not gated features.

**Sponsor tiers** (Polar.sh):
| Tier | Amount | Perks |
|------|--------|-------|
| Supporter | $5/mo or $25 one-time | Name in SPONSORS.md, Discord role |
| Backer | $15/mo or $99 one-time | Logo in README, priority issue triage |
| Sponsor | $49/mo or $249 one-time | Logo on GitHub + docs site, direct feedback channel |

## Sustainability Targets

| Month | Sponsors | Monthly Recurring | Notes |
|-------|----------|-------------------|-------|
| 1 | 5 | ~$50 | Seed — early adopters |
| 3 | 25 | ~$200 | Post-launch momentum |
| 6 | 75 | ~$500 | Sustaining contributions |
| 12 | 200 | ~$1,500 | Community maturity |

Goal: cover infrastructure and development time. Growth comes from adoption, not revenue pressure.

## Sponsorship Platform

**Polar.sh** (primary) — developer-native, GitHub integration, subscription + one-time support.
- Backup: GitHub Sponsors (if Polar.sh reach is insufficient)
- NOT Gumroad, NOT Stripe direct — unnecessary complexity for donation-based model

## Launch Sequence

### Phase 1: Seed (Week 1) — NOW

1. **Show HN post** — "I built a CLI that scans all your repos and finds cross-project patterns"
   - Title format: "Show HN: Atlas – Portfolio intelligence for AI engineering teams"
   - Post between 8-10am ET Tuesday or Wednesday
   - Include real dashboard screenshot from 8-project scan
   - Key hook: "1.25M lines of code, 8 repos, 31 seconds"

2. **Reddit** (same day as HN)
   - r/Python — "I built a CLI tool that scans your repos and grades them A-F"
   - r/commandline — "atlas status — portfolio dashboard in your terminal"
   - r/devops — "Managing 10+ repos? Here's what nobody is tracking"

3. **Dev.to articles** (3 articles, days 1-5)
   - Article 1: "Why Your Multi-Repo Setup Is a Ticking Time Bomb" (problem awareness)
   - Article 2: "I Scanned 8 Repos in 31 Seconds — Here's What I Found" (product story)
   - Article 3: "Building a CLI Health Dashboard with Rich and Typer" (technical, builder credibility)

4. **Twitter/X thread** — "I manage 14 repos. Here's what I learned nobody is tracking:"
   - Thread format: problem → discovery → solution → demo GIF → link

### Phase 2: Amplify (Week 2-3)

5. **Product Hunt launch** — day 2-3 after HN (ride the wave)
   - Category: Developer Tools
   - Tagline: "Know your repos before they bite you"

6. **LinkedIn post** — "As someone managing 14+ production repos, I realized something terrifying..."
   - Professional angle: portfolio governance, team health, tech debt visibility

7. **YouTube** — 2-min terminal demo recording
   - Show: init → add 3 projects → scan → status → inspect → connections

### Phase 3: Sustain (Month 2+)

8. Weekly content: "Atlas Portfolio Report" series
   - Scan a public org (popular OSS projects) → share findings
   - "I scanned the top 10 Python projects on GitHub — here's their health scores"

9. Integration blog posts
   - "Using atlas in CI/CD to track portfolio health"
   - "atlas + Claude Code: the multi-repo workflow"

## Content Assets Needed

| Asset | Format | Purpose | Priority |
|-------|--------|---------|----------|
| Show HN post | Markdown | Launch day | P0 |
| Reddit posts (3) | Markdown | Launch day | P0 |
| Dev.to Article 1 | Long-form blog | Problem awareness | P0 |
| Dev.to Article 2 | Long-form blog | Product story | P1 |
| Dev.to Article 3 | Long-form blog | Technical credibility | P1 |
| Twitter/X thread | Thread (8-10 tweets) | Social proof | P0 |
| LinkedIn post | Professional post | B2B reach | P1 |
| Terminal demo GIF | asciinema/GIF | README + all posts | P0 |

## Content Team Directive

The nxtg-content-engine (P-14) should generate:
1. **Query focus**: "multi-repo management developer tools portfolio health 2026"
2. **Platform targets**: Dev.to (primary), LinkedIn, X/Twitter, Reddit
3. **Voice**: Builder sharing real experience, not marketing speak
4. **Data points to weave in**:
   - 1,251,303 LOC scanned across 8 repos in 31 seconds
   - 609 test files detected
   - 8 version mismatches found automatically
   - 5 shared dependencies identified
   - Zero network calls — fully local, no telemetry
   - 100% free — no tiers, no limits, no feature gates

## Key Differentiators (for all content)

1. **No cloud, no telemetry** — everything runs locally
2. **Real data, not AI hallucinations** — parses actual config files, counts real test files
3. **Cross-project patterns** — the thing nobody else does
4. **30 seconds** — not a 20-minute setup, not a SaaS dashboard
5. **Open source (MIT)** — 100% free, sponsorware model

## Metrics to Track

- PyPI downloads (weekly)
- GitHub stars
- Show HN upvotes + comments
- Polar.sh sponsors (count + MRR)
- Dev.to article views + reactions
