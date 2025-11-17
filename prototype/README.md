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
