# Tax Advisor Application – Phase 4: AI-Powered Advisor (Gemini Q&A and Suggestions)

## Overview
This document outlines the requirements and deliverables for **Phase 4** of the Tax Advisor Application, as described in the master PRD. The goal of this phase is to provide users with a conversational, AI-powered advisor that asks smart follow-up questions and delivers personalized, actionable tax-saving suggestions using Gemini.

---

## Phase 4 Scope
- AI-powered Q&A: Gemini proactively asks a contextual follow-up question based on the user's financial data.
- User answers the question in a conversational UI.
- Gemini provides personalized, actionable investment and tax-saving suggestions in a modern, readable card format.
- Suggestions are tailored to the user's data and selected tax regime.

### Acceptance Criteria
- After tax calculation, Gemini asks a relevant follow-up question based on the user's data.
- User can answer the question in a chat-like interface.
- Gemini returns personalized, actionable suggestions (e.g., investment options, tax-saving tips).
- Suggestions are displayed in a visually appealing, card-based UI.

---

## Technical Details
- **Backend:**
  - Endpoint: `/api/chat` for Q&A and suggestions
  - Integrate Gemini API for generating questions and suggestions
  - Use session_id to retrieve user data from Supabase
- **Frontend:**
  - Conversational UI for Q&A (chat bubbles, input box)
  - Card-based display for AI suggestions
  - Loading indicators and error handling

---

## UI/UX Requirements
- Modern, conversational interface for Q&A
- Clear, actionable suggestions in card format
- Consistent with overall app branding and style
- Responsive and accessible design

---

## Out of Scope for Phase 4
- Admin analytics or session retrieval
- Manual override of AI suggestions
- Download/export of suggestions (future phase)

---

## Next Steps (for future phases)
- Session retrieval and admin analytics
- Download/export of AI suggestions 