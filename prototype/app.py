from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import sqlite3
import csv
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'records.db')
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB per file


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        uploaded_at TEXT,
        patient_id TEXT,
        procedure_code TEXT,
        amount_claimed REAL,
        date_of_service TEXT,
        extraction_confidence REAL,
        consent INTEGER,
        notes TEXT
    )
    ''')
    conn.commit()
    conn.close()


def simulate_extraction(filepath):
    """
    Placeholder for OCR/NLP extraction. In a real pipeline this would call
    OCR, then an LLM/NLP extractor that returns structured fields and a confidence score.
    Here we return simulated values based on filename and a deterministic pseudo-randomness.
    """
    fname = os.path.basename(filepath)
    # create simple deterministic pseudo-values
    patient_id = 'PAT-' + fname.split('.')[0][-4:]
    procedure_code = 'PROC-' + fname.split('.')[0][:3].upper()
    amount_claimed = round(1000 + (len(fname) * 12.5), 2)
    date_of_service = datetime.now().strftime('%Y-%m-%d')
    confidence = round(0.7 + ((len(fname) % 30) / 100.0), 2)
    return {
        'patient_id': patient_id,
        'procedure_code': procedure_code,
        'amount_claimed': amount_claimed,
        'date_of_service': date_of_service,
        'extraction_confidence': confidence
    }


def insert_record(rec):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO records (filename, uploaded_at, patient_id, procedure_code, amount_claimed, date_of_service, extraction_confidence, consent, notes)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        rec.get('filename'),
        rec.get('uploaded_at'),
        rec.get('patient_id'),
        rec.get('procedure_code'),
        rec.get('amount_claimed'),
        rec.get('date_of_service'),
        rec.get('extraction_confidence'),
        1 if rec.get('consent') else 0,
        rec.get('notes')
    ))
    conn.commit()
    conn.close()


def query_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, filename, uploaded_at, patient_id, procedure_code, amount_claimed, date_of_service, extraction_confidence, consent, notes FROM records')
    rows = c.fetchall()
    conn.close()
    keys = ['id', 'filename', 'uploaded_at', 'patient_id', 'procedure_code', 'amount_claimed', 'date_of_service', 'extraction_confidence', 'consent', 'notes']
    return [dict(zip(keys, r)) for r in rows]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # basic validation and consent check
    consent = request.form.get('consent') == 'on'
    if not consent:
        return 'Consent required to submit data', 400

    notes = request.form.get('notes', '')
    file = request.files.get('document')
    if not file:
        return 'No file uploaded', 400

    # ensure filename is present (file.filename may be None)
    if not file.filename:
        return 'Uploaded file has no filename', 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_DIR, filename)
    file.save(save_path)

    # Simulate extraction
    extracted = simulate_extraction(save_path)

    record = {
        'filename': filename,
        'uploaded_at': datetime.utcnow().isoformat(),
        'patient_id': extracted['patient_id'],
        'procedure_code': extracted['procedure_code'],
        'amount_claimed': extracted['amount_claimed'],
        'date_of_service': extracted['date_of_service'],
        'extraction_confidence': extracted['extraction_confidence'],
        'consent': consent,
        'notes': notes
    }

    insert_record(record)

    return redirect(url_for('records'))


@app.route('/records')
def records():
    recs = query_all()
    return render_template('records.html', records=recs)


@app.route('/api/records')
def api_records():
    recs = query_all()
    return jsonify(recs)


@app.route('/export/csv')
def export_csv():
    recs = query_all()
    csv_path = os.path.join(BASE_DIR, 'export.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id','filename','uploaded_at','patient_id','procedure_code','amount_claimed','date_of_service','extraction_confidence','consent','notes'])
        for r in recs:
            writer.writerow([r.get(k) for k in ['id','filename','uploaded_at','patient_id','procedure_code','amount_claimed','date_of_service','extraction_confidence','consent','notes']])
    return send_file(csv_path, as_attachment=True)


@app.route('/export/json')
def export_json():
    recs = query_all()
    json_path = os.path.join(BASE_DIR, 'export.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(recs, f, indent=2)
    return send_file(json_path, as_attachment=True)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
