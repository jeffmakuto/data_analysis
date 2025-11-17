# Prototype: Preauthorization Data Collector

This prototype demonstrates a minimal data collection tool for the proposed research on AI-driven preauthorization automation. It focuses on secure document upload, simulated extraction, storage, and export.

How it works
- Flask app (`app.py`) accepts a document upload and `notes`, requires user consent, simulates OCR/NLP extraction, and stores the results in a local SQLite database (`prototype/records.db`).
- UI is a simple accessible HTML form at `/` and a records view at `/records`.
- Export endpoints: `/export/csv` and `/export/json`.

Run locally (PowerShell)

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; python prototype\app.py
```

Ethics & privacy notes
- This prototype stores uploaded files and simulated extracted fields locally.
- Always obtain explicit consent (the form requires a consent checkbox).
- For real deployments: encrypt data at rest, limit PII exposure, obtain IRB/ethics approval, and implement secure deletion/retention policies.

Next steps for the research project
- Integrate real OCR (Tesseract or cloud OCR) and an NLP/LLM extraction service with deterministic prompts and verification.
- Add a rules engine and RPA connectors for SLADE integration and downstream actions.
- Implement auditing, access control, logging, and explainability metadata for each automated decision.

Deploying a static frontend to GitHub Pages
- The server-side prototype (Flask) cannot run on GitHub Pages (Pages is static-only). However, you can host the static frontend on GitHub Pages and host the backend API separately (Render, Railway, Heroku, Azure, etc.). The static frontend is in `docs/` and includes `index.html` and `records.html`.

Steps to publish the frontend on GitHub Pages:
1. Push your changes to GitHub (master/main). The `docs/` folder is used by Pages when enabled for the repository.
2. In the repository Settings → Pages, set the source to the `docs/` folder on the default branch and save. GitHub will publish the site at `https://<your-user>.github.io/<repo>/`.
3. Edit `docs/index.html` and `docs/records.html` to set the `API_BASE` variable to your deployed backend URL (for example, `https://my-backend.onrender.com`). The frontend will POST uploads to `API_BASE + '/upload'` and fetch records from `API_BASE + '/api/records'`.

Recommended backend hosting options (simple and free tiers available):
- Render: easy GitHub integration; supports Docker or Python/Flask services.
- Railway: simple deployments, shareable URLs.
- Fly.io: good for small services.

Example: deploy backend to Render and frontend to GitHub Pages
1. Create a Render web service from this repo (or a subfolder `prototype/`) and set the start command `python prototype/app.py` and port `5001`.
2. After Render deployment completes, note the service URL (e.g., `https://preauth-backend.onrender.com`).
3. Edit `docs/index.html` and `docs/records.html` and set: `const API_BASE = 'https://preauth-backend.onrender.com';` and commit.
4. Enable GitHub Pages from `docs/` and visit the published site.

Security & CORS
- If hosting the backend elsewhere, enable CORS on the backend (e.g., `flask-cors`) so the static frontend on GitHub Pages can POST to the API.

If you'd like, I can:
- Create the `docs/` static files (already done) and a short `pages-deploy.md` with exact steps.
- Deploy the backend to Render for you (I can prepare a simple `render.yaml` or Provide commands). Let me know which you prefer.

