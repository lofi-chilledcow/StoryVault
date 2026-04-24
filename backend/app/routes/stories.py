import json
import uuid
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.database import get_db
from app.models import Story, StoryCreate

router = APIRouter()


@router.get("", response_model=list[Story])
def list_stories(
    category: str | None = Query(default=None),
    themes: str | None = Query(default=None),
):
    try:
        conn = get_db()
        try:
            rows = conn.execute(
                "SELECT * FROM stories ORDER BY created_at DESC"
            ).fetchall()
            results = [_row_to_story(r) for r in rows]
            if category:
                results = [s for s in results if s.category == category]
            if themes:
                filter_themes = {t.strip() for t in themes.split(",")}
                results = [
                    s for s in results if filter_themes.intersection(s.themes)
                ]
            return results
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=Story, status_code=201)
def create_story(body: StoryCreate):
    if not body.created_at:
        raise HTTPException(
            status_code=400,
            detail="created_at is required — send the client's local ISO timestamp",
        )
    try:
        story = Story(id=str(uuid.uuid4()), **body.model_dump())
        conn = get_db()
        try:
            conn.execute(
                """INSERT INTO stories (id, title, content, category, themes, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    story.id,
                    story.title,
                    story.content,
                    story.category,
                    json.dumps(story.themes),
                    story.created_at,
                ),
            )
            conn.commit()
            return story
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{story_id}", response_model=Story)
def get_story(story_id: str):
    try:
        conn = get_db()
        try:
            row = conn.execute(
                "SELECT * FROM stories WHERE id = ?", (story_id,)
            ).fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Story not found")
            return _row_to_story(row)
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{story_id}", response_model=Story)
def update_story(story_id: str, body: StoryCreate):
    if not body.created_at:
        raise HTTPException(
            status_code=400,
            detail="created_at is required — send the client's local ISO timestamp",
        )
    try:
        conn = get_db()
        try:
            row = conn.execute(
                "SELECT * FROM stories WHERE id = ?", (story_id,)
            ).fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Story not found")
            conn.execute(
                """UPDATE stories
                   SET title=?, content=?, category=?, themes=?, created_at=?
                   WHERE id=?""",
                (
                    body.title,
                    body.content,
                    body.category,
                    json.dumps(body.themes),
                    body.created_at,
                    story_id,
                ),
            )
            conn.commit()
            return Story(id=story_id, **body.model_dump())
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{story_id}", status_code=204)
def delete_story(story_id: str):
    try:
        conn = get_db()
        try:
            row = conn.execute(
                "SELECT id FROM stories WHERE id = ?", (story_id,)
            ).fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Story not found")
            conn.execute("DELETE FROM stories WHERE id = ?", (story_id,))
            conn.commit()
            return Response(status_code=204)
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _row_to_story(row) -> Story:
    return Story(
        id=row["id"],
        title=row["title"],
        content=row["content"],
        category=row["category"],
        themes=json.loads(row["themes"] or "[]"),
        created_at=row["created_at"],
    )
