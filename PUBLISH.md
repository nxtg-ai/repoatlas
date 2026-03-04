# Publishing repoatlas to PyPI

## Option 1: Trusted Publisher (Recommended — One-Time Setup)

1. Go to https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name**: `repoatlas`
   - **Owner**: `nxtg-ai`
   - **Repository**: `repoatlas`
   - **Workflow name**: `ci.yml`
   - **Environment name**: (leave blank)
4. Click "Add"

After this, any commit starting with `release:` on main will auto-publish:
```bash
git commit -m "release: v0.1.0"
git push origin main
```

## Option 2: Manual with API Token

1. Go to https://pypi.org/manage/account/token/
2. Create a token scoped to `repoatlas` (or all projects for first upload)
3. Run:
```bash
cd ~/projects/atlas
python3 -m build
python3 -m twine upload dist/* -u __token__ -p pypi-YOUR-TOKEN-HERE
```

## Verify Installation

```bash
pip install repoatlas
atlas --help
```
