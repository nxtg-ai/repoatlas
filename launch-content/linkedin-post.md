# nxtg-atlas Launch Post — LinkedIn

---

How many of your repos have zero tests?

Not low coverage. Zero. No test runner configured. No CI gate. Nothing.

I asked myself that question last month and realized I couldn't answer it. I manage 14 repositories across a portfolio of projects — Python, Rust, TypeScript, React. Each repo has its own CI, its own dependencies, its own tech stack. Every tool I use works inside a single repo at a time. VS Code opens one. GitHub shows one. AI coding assistants see one.

Nobody sees the full picture.

When I finally went looking, here's what I found across just 8 production repos:

- 3 had zero test files
- 8 shared dependency version mismatches (same library, different versions, different repos)
- 2 were missing CI entirely
- 5 shared dependencies had quietly drifted apart

None of this was visible from inside any single repo. Every repo looked fine on its own. The problems only exist at the portfolio level — and nobody was looking there.

So I built a tool. It's called **nxtg-atlas** and it's deliberately simple: a Python CLI that scans a directory of repos and scores each one across four dimensions — code quality, test coverage, dependency health, and project hygiene. Each dimension gets an A-through-F grade. You get a single dashboard showing every repo side by side.

First real scan: 1,251,303 lines of code across 8 repos. 609 test files detected. 31 seconds. Zero network calls — your code never leaves your machine. No telemetry. No cloud account. MIT licensed.

This isn't enterprise software. It's a diagnostic tool for engineers and team leads who work across multiple repos and want to know where the gaps are before they become incidents.

```
pip install nxtg-atlas
atlas scan ~/projects --format table
```

Free for up to 3 projects. $49 one-time unlock for unlimited — no subscription.

GitHub: github.com/nxtg-ai/repoatlas

If you lead a team that ships from more than one repo, give it a scan. I'd genuinely like to know what it finds.

---

#OpenSource #DeveloperTools #Python #CLI #CodeQuality #SoftwareEngineering #DevOps #MultiRepo #PortfolioIntelligence #NXTGAI
