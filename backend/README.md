# Phylax backend

Run with Python 3.11+ after copying the project `.env.example` to `.env`:

```powershell
python -m pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload
```

Apply `app.db.queries.PGVECTOR_SCHEMA` in the Supabase SQL editor before using Supabase persistence. It creates `documents`, `clauses`, `law_chunks`, `document_analyses`, and the `match_law_chunks` cosine-similarity RPC. The service runs with an explicitly in-memory repository while Supabase credentials are absent; that is intended for local development only and is not durable.

Set `ADMIN_API_KEY` and send it as `X-Admin-API-Key` to `POST /api/v1/laws/ingest`. The ingestion endpoint is disabled when no key is configured.
