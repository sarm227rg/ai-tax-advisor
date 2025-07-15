# Tax Advisor Application – Phase 1

## Overview
A web-based platform for salaried individuals in India to analyze tax liabilities and receive personalized, AI-powered tax-saving strategies. This phase covers project setup, database schema, and a modern landing page.

## Tech Stack
- Backend: Python (FastAPI)
- Database: Supabase (PostgreSQL, psycopg2)
- Frontend: HTML, CSS (Aptos Display font), JavaScript

## Project Structure
- `app/` – Main application code (FastAPI, business logic, DB connection)
- `static/` – Static assets (CSS, JS, images, fonts)
- `template/` – HTML templates (for landing page, etc.)
- `tax_advisor/` – Python virtual environment (venv)
- `requirement.txt` – Python dependencies
- `docs/` – Documentation

## Setup Instructions
1. **Create and activate a virtual environment**
   ```bash
   python -m venv tax_advisor
   # On Windows:
   .\tax_advisor\Scripts\activate
   # On macOS/Linux:
   source tax_advisor/bin/activate
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```
3. **Run the FastAPI app**
   ```bash
   uvicorn app.main:app --reload
   ```
4. **Access the landing page**
   - Open your browser at `http://localhost:8000`

## Notes
- Place all static files (CSS, JS, images) in the `static/` folder.
- Place all HTML templates in the `template/` folder.
- The `tax_advisor` folder is only for the Python virtual environment. 