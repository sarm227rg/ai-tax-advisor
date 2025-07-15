# Tax Advisor Application – Phase 1: Project Setup, DB Schema, and Landing Page

## Overview
This document outlines the requirements and deliverables for **Phase 1** of the Tax Advisor Application, as described in the master PRD. The goal of this phase is to establish the project foundation, set up the database schema, and implement a modern landing page.

---

## Phase 1 Scope
- **Project setup** (frontend and backend scaffolding)
- **Database schema creation** (Supabase: `UserFinancials` table)
- **Landing page UI** (modern, branded, with "Start" button)

### Acceptance Criteria
- User sees the landing page.
- The `UserFinancials` table exists in Supabase.

---

## Technical Details

### Tech Stack
| Component | Technology |
|---|---|
| Frontend | Vanilla HTML, CSS (Aptos Display font), JavaScript |
| Backend | Python (FastAPI) |
| Database | Supabase (Cloud PostgreSQL, direct psycopg2 connection) |
| Deployment | Render (from GitHub) |

### Database Schema
**Table: `UserFinancials`**
| Column Name         | Data Type         | Description                        |
|--------------------|------------------|------------------------------------|
| `session_id`       | `UUID`           | Primary Key, unique session ID      |
| `gross_salary`     | `NUMERIC(15, 2)` | Total gross salary                 |
| `basic_salary`     | `NUMERIC(15, 2)` | Basic salary component             |
| `hra_received`     | `NUMERIC(15, 2)` | HRA received                       |
| `rent_paid`        | `NUMERIC(15, 2)` | Annual rent paid                   |
| `deduction_80c`    | `NUMERIC(15, 2)` | 80C investments                    |
| `deduction_80d`    | `NUMERIC(15, 2)` | 80D medical insurance              |
| `standard_deduction` | `NUMERIC(15, 2)` | Standard deduction                |
| `professional_tax` | `NUMERIC(15, 2)` | Professional tax paid              |
| `tds`              | `NUMERIC(15, 2)` | Tax Deducted at Source             |
| `created_at`       | `TIMESTAMPTZ`    | Record creation timestamp          |

---

## Project Structure
The recommended directory structure for Phase 1 is as follows:

```
project-root/
│
├── app/                # Main application code (FastAPI, business logic, DB connection)
├── static/             # Static assets (CSS, JS, images, fonts)
├── template/           # HTML templates (e.g., Jinja2 or plain HTML for landing page)
├── README.md           # Project overview and setup instructions
├── requirement.txt     # Python dependencies for the backend
├── tax_advisor/        # Python virtual environment (venv) and related files
│
├── docs/
│   ├── PRD.md          # Master product requirements document
│   └── PRD-Phase1.md   # This phase-specific requirements file
```

- All application and static files are outside the `tax_advisor` venv directory.
- The `tax_advisor` folder is reserved for the Python virtual environment and should not contain app code.
- Adjust as needed for your workflow or deployment platform.

---

## UI/UX Requirements
- Modern, light-themed landing page with blue highlights.
- Typography: Use "Aptos Display" font.
- Prominent "Start" button to begin the process.
- Responsive and visually appealing design.

---

## Out of Scope for Phase 1
- PDF upload and data extraction
- Tax calculation and comparison
- AI-powered advisor
- Any user flow beyond the landing page

---

## Next Steps (for future phases)
- Implement PDF upload and data extraction (Phase 2)
- Tax calculation and regime comparison (Phase 3)
- AI-powered advisor and suggestions (Phase 4) 