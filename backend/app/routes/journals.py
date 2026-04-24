import json
import uuid
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.database import get_db
from app.models import Journal, JournalCreate

router = APIRouter()


@router.get("", response_model=list[Journal])
def list_journals(
    category: str | None = Query(default=None),
    limit: int = Query(default=20),
):
    try:
        conn = get_db()
        try:
            if category:
                rows = conn.execute(
                    "SELECT * FROM journals WHERE category = ? ORDER BY created_at DESC LIMIT ?",
                    (category, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM journals ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            return [_row_to_journal(r) for r in rows]
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=Journal, status_code=201)
def create_journal(body: JournalCreate):
    if not body.created_at:
        raise HTTPException(
            status_code=400,
            detail="created_at is required — send the client's local ISO timestamp",
        )
    try:
        journal = Journal(id=str(uuid.uuid4()), **body.model_dump())
        conn = get_db()
        try:
            conn.execute(
                """INSERT INTO journals (id, title, content, category, vocab_words, score, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    journal.id,
                    journal.title,
                    journal.content,
                    journal.category,
                    json.dumps(journal.vocab_words),
                    journal.score,
                    journal.created_at,
                ),
            )
            conn.commit()
            return journal
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{journal_id}", response_model=Journal)
def get_journal(journal_id: str):
    try:
        conn = get_db()
        try:
            row = conn.execute(
                "SELECT * FROM journals WHERE id = ?", (journal_id,)
            ).fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Journal not found")
            return _row_to_journal(row)
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{journal_id}", response_model=Journal)
def update_journal(journal_id: str, body: JournalCreate):
    if not body.created_at:
        raise HTTPException(
            status_code=400,
            detail="created_at is required — send the client's local ISO timestamp",
        )
    try:
        conn = get_db()
        try:
            row = conn.execute(
                "SELECT * FROM journals WHERE id = ?", (journal_id,)
            ).fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Journal not found")
            conn.execute(
                """UPDATE journals
                   SET title=?, content=?, category=?, vocab_words=?, score=?, created_at=?
                   WHERE id=?""",
                (
                    body.title,
                    body.content,
                    body.category,
                    json.dumps(body.vocab_words),
                    body.score,
                    body.created_at,
                    journal_id,
                ),
            )
            conn.commit()
            return Journal(id=journal_id, **body.model_dump())
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{journal_id}", status_code=204)
def delete_journal(journal_id: str):
    try:
        conn = get_db()
        try:
            row = conn.execute(
                "SELECT id FROM journals WHERE id = ?", (journal_id,)
            ).fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Journal not found")
            conn.execute("DELETE FROM journals WHERE id = ?", (journal_id,))
            conn.commit()
            return Response(status_code=204)
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _row_to_journal(row) -> Journal:
    return Journal(
        id=row["id"],
        title=row["title"],
        content=row["content"],
        category=row["category"],
        vocab_words=json.loads(row["vocab_words"] or "[]"),
        score=row["score"],
        created_at=row["created_at"],
    )
