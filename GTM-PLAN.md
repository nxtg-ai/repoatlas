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

## Revenue Model — Open Core

| Tier | Price | What You Get |
|------|-------|-------------|
| **Free** | $0 | 3 projects, health scoring, tech detection, git health, inspect |
| **Pro** | $49 one-time | Unlimited projects, cross-project intelligence, batch-add, export |

**Why $49 one-time (not SaaS)**:
- Developer trust — no subscription fatigue, no lock-in
- Viral loop — low barrier → word of mouth → Pro conversions
- Comparable: LazyGit ($0 → sponsors), Atuin ($0/$8/mo), Warp (free → enterprise)
- One-time payment removes friction, builds goodwill

## Revenue Targets

| Month | Pro Licenses | Monthly Revenue | Cumulative |
|-------|-------------|----------------|------------|
| 1 | 10 | $490 | $490 |
| 2 | 25 | $1,225 | $1,715 |
| 3 | 50 | $2,450 | $4,165 |
| 6 | 100 | $4,900 | $17,150 |
| 12 | 200 | $9,800 | $52,150 |

Conservative: 2% conversion rate on free installs.

## Payment Platform

**Polar.sh** (primary) — 4% MoR fees, developer-native, GitHub integration.
- Backup: Lemon Squeezy (5% fees)
- NOT Gumroad (10% — robbery)
- NOT Stripe direct (compliance burden, tax handling)

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
   - $0 free tier is genuinely useful, not crippled

## Key Differentiators (for all content)

1. **No cloud, no telemetry** — everything runs locally
2. **Real data, not AI hallucinations** — parses actual config files, counts real test files
3. **Cross-project patterns** — the thing nobody else does
4. **30 seconds** — not a 20-minute setup, not a SaaS dashboard
5. **Open source (MIT)** — free tier works, Pro is worth it

## Metrics to Track

- PyPI downloads (weekly)
- GitHub stars
- Show HN upvotes + comments
- Pro license purchases (Polar.sh dashboard)
- Dev.to article views + reactions
