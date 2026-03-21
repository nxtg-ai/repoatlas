# Atlas Launch Day Checklist

## Pre-Launch (day before)

- [ ] PyPI published and `pip install nxtg-atlas` works (N-06)
- [ ] README GIF renders correctly on GitHub (N-07)
- [ ] `atlas --help` shows clean output
- [ ] `atlas init && atlas add . && atlas scan && atlas status` works end-to-end
- [ ] GitHub repo description and topics set
- [ ] GitHub social preview image uploaded (terminal screenshot)
- [ ] All launch posts reviewed and finalized

## Launch Day (T+0)

### Morning (9-10am ET)
- [ ] Post Show HN (see `show-hn.md`)
- [ ] Post to r/Python with "I Made This" flair (see `reddit.md`)
- [ ] Post Twitter/X thread (see `twitter.md`)
- [ ] Post to r/commandline (see `reddit.md`)

### First 2 Hours (critical)
- [ ] Reply to every HN comment
- [ ] Reply to every Reddit comment
- [ ] Engage with Twitter replies
- [ ] Monitor GitHub issues for new user problems
- [ ] Check PyPI download count

### Afternoon
- [ ] Cross-post to Dev.to (adapted from HN text)
- [ ] Share in relevant Discord servers (Python, DevOps, CLI tools)
- [ ] LinkedIn post (shorter, more professional tone)

## Day 2-3
- [ ] Submit to Product Hunt (see `product-hunt.md`)
- [ ] Reply to any late HN/Reddit comments
- [ ] Write up learnings

## Metrics to Track
- GitHub stars (target: 50 day 1, 200 week 1)
- PyPI installs (target: 100 day 1)
- HN points (target: 50+)
- GitHub issues opened (engagement signal)

## Emergency Playbook
- **Bug reported**: Fix within 1 hour, release patch, reply with fix link
- **Install fails**: Check PyPI, test on clean venv, update README
- **Negative feedback**: Thank them, ask what they'd improve, log for roadmap
