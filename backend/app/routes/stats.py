import json
from datetime import date, timedelta
from fastapi import APIRouter, HTTPException, Query

from app.database import get_db
from app.models import Stats

router = APIRouter()


@router.get("", response_model=Stats)
def get_stats(date: str = Query(..., description="Client local date as YYYY-MM-DD")):
    # date param is required — we never use the server date
    try:
        client_date = _parse_date(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="date must be YYYY-MM-DD")

    try:
        conn = get_db()
        try:
            total_journals = conn.execute(
                "SELECT COUNT(*) FROM journals"
            ).fetchone()[0]

            total_stories = conn.execute(
                "SELECT COUNT(*) FROM stories"
            ).fetchone()[0]

            # Collect all distinct writing dates (YYYY-MM-DD prefix of created_at)
            journal_dates = {
                row[0][:10]
                for row in conn.execute(
                    "SELECT created_at FROM journals"
                ).fetchall()
                if row[0]
            }
            story_dates = {
                row[0][:10]
                for row in conn.execute(
                    "SELECT created_at FROM stories"
                ).fetchall()
                if row[0]
            }
            all_dates = journal_dates | story_dates

            # Count consecutive days going back from client date
            streak = 0
            cursor = client_date
            while str(cursor) in all_dates:
                streak += 1
                cursor -= timedelta(days=1)

            # Flatten all vocab_words across journals
            rows = conn.execute("SELECT vocab_words FROM journals").fetchall()
            words_used: list[str] = []
            seen: set[str] = set()
            for row in rows:
                for word in json.loads(row[0] or "[]"):
                    if word not in seen:
                        seen.add(word)
                        words_used.append(word)

            return Stats(
                total_journals=total_journals,
                total_stories=total_stories,
                streak_days=streak,
                words_used=words_used,
            )
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _parse_date(value: str) -> date:
    from datetime import date as date_type
    parts = value.split("-")
    if len(parts) != 3:
        raise ValueError
    return date_type(int(parts[0]), int(parts[1]), int(parts[2]))
