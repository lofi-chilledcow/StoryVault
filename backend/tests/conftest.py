import sqlite3
import pytest
from fastapi.testclient import TestClient

import app.database as db_module
import app.routes.journals as journals_mod
import app.routes.stories as stories_mod
import app.routes.stats as stats_mod
from app.main import app


class _NoClose:
    """Wraps a sqlite3.Connection but ignores close() so the in-memory DB survives."""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def close(self):
        pass  # intentionally a no-op — closing would destroy the :memory: DB

    def __getattr__(self, name):
        return getattr(self._conn, name)


@pytest.fixture
def client():
    # Fresh in-memory DB per test — automatic isolation, no cleanup needed
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")

    def _get_db():
        return _NoClose(conn)

    # Patch get_db everywhere it's referenced.
    # Route files do `from app.database import get_db` which creates a local
    # binding at import time — patching db_module alone is not enough.
    _targets = [db_module, journals_mod, stories_mod, stats_mod]
    _originals = [(m, m.get_db) for m in _targets]
    for mod, _ in _originals:
        mod.get_db = _get_db

    # TestClient as context manager triggers FastAPI startup (init_db)
    with TestClient(app) as c:
        yield c

    for mod, original in _originals:
        mod.get_db = original
    conn.close()


# ---------------------------------------------------------------------------
# Shared payloads reused across test modules
# ---------------------------------------------------------------------------

JOURNAL = {
    "title": "Test Journal",
    "content": "Today was a resilient day of work",
    "category": "tech",
    "vocab_words": ["resilient"],
    "score": 80,
    "created_at": "2026-04-19 10:00:00",
}

STORY = {
    "title": "Test Story",
    "content": "A deliberate push through adversity",
    "category": "life",
    "themes": ["challenge", "growth"],
    "created_at": "2026-04-19 11:00:00",
}
