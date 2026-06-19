# GitHub Publishing Checklist

Use this checklist before pushing the project to a public GitHub repository.

## 1. Do Not Commit Local Runtime Files

Confirm these are not included in the commit:

- `.venv/`
- `.env`
- `models/*.pt`
- `models/easyocr/`
- `outputs/`
- `tmp/`
- uploaded videos
- processed videos
- evidence images
- generated challan PDFs
- personal owner/contact data
- real license plate data

## 2. Remove Already-Tracked Local Owner Data

If `data/mock_owner_registry.json` is already tracked by Git, remove it from tracking while keeping your local copy:

```bash
git rm --cached data/mock_owner_registry.json
```

The file is listed in `.gitignore`, so after this command Git should stop trying to upload it.

## 3. Check What Will Be Committed

Run:

```bash
git status --short
```

Also check ignored files:

```bash
git status --short --ignored
```

Model weights and generated outputs should appear as ignored files, not as files ready to commit.

## 4. Files That Should Be Good To Commit

Typical source/documentation files:

- `app.py`
- `requirements.txt`
- `README.md`
- `readmeV1.md`
- `.env.example`
- `.gitignore`
- `.streamlit/config.toml`
- `models/README.md`
- `docs/`
- `notes/`
- lightweight source files under `src/`

## 5. Final Review

Open `README.md` on GitHub after pushing and confirm that a reviewer can understand:

- what the project does,
- which models are required,
- how to install dependencies,
- how to run the Streamlit app,
- where outputs are generated,
- why model weights and generated files are not included.
