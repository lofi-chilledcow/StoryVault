# StoryVault — Backend

Python + FastAPI + SQLite REST API.

## Stack

- **FastAPI** — web framework
- **SQLite** + WAL mode — embedded database
- **Pydantic** — request/response validation
- **uvicorn** — ASGI server

## Project structure

```
backend/
├── app/
│   ├── main.py        FastAPI app, CORS, startup
│   ├── database.py    SQLite connection, schema, init_db()
│   ├── models.py      Pydantic models (Journal, Story, Stats)
│   └── routes/
│       ├── journals.py  CRUD /api/journals
│       ├── stories.py   CRUD /api/stories
│       └── stats.py     GET  /api/stats
├── data/              SQLite database file (gitignored)
├── tests/             pytest integration tests
└── requirements.txt
```

## Setup

```bash
python -m venv venv && venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8001
```

## API endpoints

| Method | Path                  | Description            |
|--------|-----------------------|------------------------|
| GET    | /health               | Health check           |
| GET    | /api/journals         | List journals          |
| POST   | /api/journals         | Create journal         |
| GET    | /api/journals/{id}    | Get journal            |
| PUT    | /api/journals/{id}    | Update journal         |
| DELETE | /api/journals/{id}    | Delete journal         |
| GET    | /api/stories          | List stories           |
| POST   | /api/stories          | Create story           |
| GET    | /api/stories/{id}     | Get story              |
| PUT    | /api/stories/{id}     | Update story           |
| DELETE | /api/stories/{id}     | Delete story           |
| GET    | /api/stats            | Writing stats          |

Interactive docs: http://localhost:8001/docs

## Environment variables

```
DATABASE_PATH=./data/storyvault.db
FRONTEND_URL=http://localhost:5173
PORT=8001
```

## Tests

```bash
pytest -v
```
