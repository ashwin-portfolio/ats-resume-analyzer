# Backend Tests

All backend tests live in this folder. Run them from the **backend/** directory (with venv activated).

## Prerequisites

- **API / integration tests** (`test_all_phases.py`, `test_edge_cases.py`): backend server must be running in another terminal.
- **Database tests** (`test_database.py`): database (e.g. PostgreSQL) configured in `backend/.env`.

## Run from backend/

```bash
cd backend
source venv/bin/activate   # or: venv\Scripts\activate on Windows

# Start the server in another terminal first, then:
python tests/test_all_phases.py    # Phases 1–4: skeleton, DB via API, ML, frontend integration
python tests/test_edge_cases.py    # Edge cases: file upload, job description, network

# Database CRUD tests (no server needed; uses .env DB)
python tests/test_database.py
```

## Test files

| File | Description |
|------|-------------|
| `test_all_phases.py` | Phases 1–4: backend skeleton, database (via API), ML pipeline, frontend integration. Requires backend server. |
| `test_edge_cases.py` | Edge cases: file upload, job description, network (report ID, pagination). Requires backend server. |
| `test_database.py` | Direct DB CRUD: connection, create/read/update/delete report and keywords. Requires DB in .env. |
