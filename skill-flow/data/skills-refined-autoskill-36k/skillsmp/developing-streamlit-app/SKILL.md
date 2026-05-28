---
name: developing-streamlit-app
description: Develops or modifies the Streamlit frontend in the @[streamlit_app] directory. Use when the user requests changes to the UI, dashboards, visualizations, or new tools in the streamlit app.
---

# Developing Streamlit App

## When to use this skill

- Adding a new page or tool to the dashboard.
- Modifying existing visualizations.
- connecting frontend components to the backend API.
- Updating the main layout or sidebar.

## Structure

- Root: `streamlit_app/`
- Entry Point: `streamlit_app/app.py`
- Pages: `streamlit_app/pages/` (Files named `1_Name.py`, `2_Name.py`, etc.)

## Workflow rules

### 1. Creating New Pages

- Create a new python file in `streamlit_app/pages/`.
- Use the numbering naming convention to control order (e.g. `4_New_Tool.py`).
- Add a title with `st.title("Tool Name")`.

### 2. Layout & Style

- Use `st.set_page_config` in `app.py` for global settings, but individual pages can set their own titles.
- Use `st.sidebar` for navigation or global controls/status.
- Keep the UI clean; use `st.expander` for advanced options.

### 3. Backend Integration

- Do NOT implement core business logic in the Streamlit files.
- Call the FastAPI backend for data processing/storage.
- Determine the backend API URL (usually `http://localhost:8000/api/v1/...`).
- **CRITICAL**: Use `requests` to call the backend. NEVER implement direct calls to external APIs (Gemini, LiteLLM, Vectors, etc.) in Streamlit. ALWAYS go through the backend.
- Handle connection errors gracefully (e.g. if backend is down).

### 4. Running Locally

- Run with `streamlit run streamlit_app/app.py`.

## Checklist for Changes

1. [ ] Created/Modified file in `streamlit_app/pages/`.
2. [ ] Verified naming convention.
3. [ ] Connected to Backend (if data driven).
4. [ ] Tested interactivty (buttons, inputs).
