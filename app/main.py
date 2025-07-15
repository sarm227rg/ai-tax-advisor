# NOTE: FastAPI and related imports require the dependencies in requirement.txt to be installed in your environment.
from fastapi import FastAPI, Request, APIRouter, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import shutil
import tempfile
import requests
import json
import uuid
from datetime import datetime
from decimal import Decimal

from .db import init_userfinancials_table, get_connection
from .pdf_extract import extract_pdf_data

from dotenv import load_dotenv
load_dotenv()

import os
print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_userfinancials_table()

# Mount static files
app.mount('/static', StaticFiles(directory=os.path.join(os.path.dirname(__file__), '../static')), name='static')

# Set up Jinja2 templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../template'))

@app.get('/', response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse('landing.html', {"request": request})

@app.get('/upload', response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse('upload.html', {"request": request})

@app.post('/api/upload-pdf')
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        return {"status": "error", "detail": "Only PDF files are supported."}
    # Save to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        extracted = extract_pdf_data(tmp_path)
        return {"status": "ok", "data": extracted}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        try:
            import os
            os.remove(tmp_path)
        except Exception:
            pass

router = APIRouter()

@router.get("/db-health")
def db_health():
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                result = cur.fetchone()
        if result is not None:
            return {"status": "ok", "result": result[0]}
        else:
            return {"status": "error", "detail": "No result from DB."}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key=' + GEMINI_API_KEY if GEMINI_API_KEY else None

@app.post('/api/extract-structured')
async def extract_structured(data: dict):
    if not GEMINI_API_KEY or not GEMINI_API_URL:
        return {"status": "error", "detail": "Gemini API key not configured."}
    text = data.get('text', '')
    if not text:
        return {"status": "error", "detail": "No text provided."}
    prompt = (
        "Extract the following fields from the provided salary slip text. "
        "Return a JSON object with these keys: gross_salary, basic_salary, hra_received, deduction_80c, deduction_80d. "
        "If a value is not found, use an empty string. Only return the JSON object, nothing else.\n\n"
        f"Text: {text}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        resp = requests.post(GEMINI_API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        gemini_response = resp.json()
        # Extract the JSON from the model's response
        model_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
        # Try to parse the JSON from the model's response
        try:
            # Sometimes Gemini returns code block markdown, strip it
            model_text = model_text.strip('`\n ')
            if model_text.startswith('json'):
                model_text = model_text[4:].strip()
            structured = json.loads(model_text)
        except Exception:
            return {"status": "error", "detail": "Could not parse Gemini response.", "raw": model_text}
        return {"status": "ok", "data": structured}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.post('/api/save-user-financials')
async def save_user_financials(data: dict):
    # Extract fields from data
    fields = [
        'gross_salary', 'basic_salary', 'hra_received', 'rent_paid',
        'deduction_80c', 'deduction_80d', 'standard_deduction',
        'professional_tax', 'tds', 'tax_regime'
    ]
    # Convert empty strings to None for DB insert
    values = {k: (data.get(k) if data.get(k) not in [None, ''] else None) for k in fields}
    session_id = str(uuid.uuid4())
    created_at = datetime.utcnow()
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO "UserFinancials" (
                        session_id, gross_salary, basic_salary, hra_received, rent_paid,
                        deduction_80c, deduction_80d, standard_deduction, professional_tax, tds, created_at
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''', [
                    session_id,
                    values['gross_salary'],
                    values['basic_salary'],
                    values['hra_received'],
                    values['rent_paid'],
                    values['deduction_80c'],
                    values['deduction_80d'],
                    values['standard_deduction'],
                    values['professional_tax'],
                    values['tds'],
                    created_at
                ])
        return {"status": "ok", "session_id": session_id}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.post('/api/chat')
async def chat_with_gemini(data: dict):
    session_id = data.get('session_id')
    user_message = data.get('user_message', '').strip()
    history = data.get('history', [])  # List of {role, content}
    if not session_id:
        return {"status": "error", "detail": "session_id is required."}
    # Fetch user financials from Supabase
    def serialize_value(val):
        if isinstance(val, Decimal):
            return float(val)
        if isinstance(val, (datetime, uuid.UUID)):
            return str(val)
        return val
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM "UserFinancials" WHERE session_id = %s', (session_id,))
                row = cur.fetchone()
                if not row:
                    return {"status": "error", "detail": "Session not found."}
                colnames = [desc[0] for desc in cur.description]
                user_data = {k: serialize_value(v) for k, v in zip(colnames, row)}
    except Exception as e:
        return {"status": "error", "detail": f"DB error: {e}"}
    # Build multi-turn transcript for Gemini
    transcript = ""
    for msg in history:
        if msg.get('role') == 'user':
            transcript += f"User: {msg.get('content','')}\n"
        elif msg.get('role') == 'assistant':
            transcript += f"Advisor: {msg.get('content','')}\n"
    if user_message:
        transcript += f"User: {user_message}\n"
    if not history and not user_message:
        # First message: ask a follow-up question
        prompt = (
            "Given the following user financial data, ask a smart, contextual follow-up question to help optimize their taxes or investments. "
            "Be proactive and relevant.\n\nUser Data: " + json.dumps(user_data)
        )
    else:
        prompt = (
            "You are a helpful tax advisor. Here is the user's financial data: " + json.dumps(user_data) +
            "\n\nHere is the conversation so far (alternate User/Advisor turns):\n" + transcript +
            "\nContinue the conversation as the advisor, providing helpful, contextual replies."
        )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        resp = requests.post(GEMINI_API_URL, json=payload, timeout=30)
        resp.raise_for_status()
        gemini_response = resp.json()
        model_text = gemini_response['candidates'][0]['content']['parts'][0]['text']
        return {"status": "ok", "response": model_text}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get('/advisor', response_class=HTMLResponse)
def advisor_page(request: Request):
    return templates.TemplateResponse('advisor.html', {"request": request})

app.include_router(router) 