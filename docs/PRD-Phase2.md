# Tax Advisor Application – Phase 2: PDF Upload, Data Extraction, and Review

## Overview
This document outlines the requirements and deliverables for **Phase 2** of the Tax Advisor Application, as described in the master PRD. The goal of this phase is to enable users to upload a Pay Slip or Form 16 (PDF), extract relevant data, and review/edit the extracted information in a form.

---

## Phase 2 Scope
- **PDF upload** (Pay Slip or Form 16)
- **Data extraction** using PyPDF2, pytesseract (OCR), pdf2image, and Gemini LLM
- **Pre-filled review form** for user to verify and edit extracted data
- **Tax regime selection** (Old/New) via radio button

### Acceptance Criteria
- User can upload a PDF (Pay Slip or Form 16).
- The backend extracts relevant data and structures it.
- The user is presented with a form pre-filled with the extracted data for review and editing.
- The user can select their preferred tax regime (Old/New).

---

## Technical Details

### PDF Processing Stack
- **PyPDF2**: For extracting text from digital PDFs
- **pytesseract**: For OCR on scanned PDFs
- **pdf2image**: For converting PDF pages to images (for OCR)
- **Gemini LLM**: For structuring and validating extracted data

### Backend
- Python (FastAPI)
- Endpoint: `/api/upload-pdf` (accepts PDF, returns extracted data)
- Temporary file storage (ephemeral disk)
- Data validation and error handling

### Frontend
- PDF upload UI (drag-and-drop or file picker)
- Progress indicator during extraction
- Review/edit form with all extracted fields (as per UserFinancials schema)
- Tax regime selection (radio button)
- Submit button to proceed to next phase

---

## UI/UX Requirements
- Clean, modern upload interface
- Clear instructions for supported PDF types
- Responsive review form with all relevant fields pre-filled
- Error messages for unsupported files or extraction failures
- Consistent with overall app branding and style

---

## Out of Scope for Phase 2
- Tax calculation and comparison
- AI-powered advisor (Gemini Q&A)
- Database save (handled in next phase)
- Any user flow beyond upload and review

---

## Next Steps (for future phases)
- Tax calculation and regime comparison (Phase 3)
- AI-powered advisor and suggestions (Phase 4) 