from tests.conftest import JOURNAL, STORY


def test_stats_correct_totals(client):
    client.post("/api/journals", json=JOURNAL)
    client.post("/api/stories", json=STORY)
    resp = client.get("/api/stats?date=2026-04-19")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_journals"] == 1
    assert data["total_stories"] == 1


def test_stats_requires_date_param(client):
    resp = client.get("/api/stats")
    assert resp.status_code == 422


def test_stats_streak_consecutive_days(client):
    # Two journals on consecutive days → streak of 2 from 2026-04-19
    client.post("/api/journals", json={**JOURNAL, "created_at": "2026-04-19 10:00:00"})
    client.post("/api/journals", json={**JOURNAL, "created_at": "2026-04-18 10:00:00"})
    resp = client.get("/api/stats?date=2026-04-19")
    assert resp.json()["streak_days"] == 2


def test_stats_streak_gap_breaks_streak(client):
    # Entries on day 19 and 17 (gap on 18) → streak of 1 from 2026-04-19
    client.post("/api/journals", json={**JOURNAL, "created_at": "2026-04-19 10:00:00"})
    client.post("/api/journals", json={**JOURNAL, "created_at": "2026-04-17 10:00:00"})
    resp = client.get("/api/stats?date=2026-04-19")
    assert resp.json()["streak_days"] == 1


def test_stats_words_used_deduplicated(client):
    # Two journals share "resilient" → appears only once
    client.post("/api/journals", json={**JOURNAL, "vocab_words": ["resilient", "deliberate"]})
    client.post("/api/journals", json={**JOURNAL, "vocab_words": ["resilient", "focus"]})
    resp = client.get("/api/stats?date=2026-04-19")
    words = resp.json()["words_used"]
    assert set(words) == {"resilient", "deliberate", "focus"}
    assert words.count("resilient") == 1  # no duplicates
