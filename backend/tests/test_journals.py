from tests.conftest import JOURNAL


def test_create_journal_returns_201_with_id(client):
    resp = client.post("/api/journals", json=JOURNAL)
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["title"] == JOURNAL["title"]
    assert data["category"] == JOURNAL["category"]


def test_create_journal_missing_title_returns_422(client):
    payload = {k: v for k, v in JOURNAL.items() if k != "title"}
    resp = client.post("/api/journals", json=payload)
    assert resp.status_code == 422


def test_create_journal_invalid_category_returns_422(client):
    resp = client.post("/api/journals", json={**JOURNAL, "category": "invalid"})
    assert resp.status_code == 422


def test_list_journals_returns_list(client):
    client.post("/api/journals", json=JOURNAL)
    resp = client.get("/api/journals")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) == 1


def test_get_journal_returns_single(client):
    created = client.post("/api/journals", json=JOURNAL).json()
    resp = client.get(f"/api/journals/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == created["id"]


def test_get_journal_not_found_returns_404(client):
    resp = client.get("/api/journals/does-not-exist")
    assert resp.status_code == 404


def test_update_journal(client):
    created = client.post("/api/journals", json=JOURNAL).json()
    updated_payload = {**JOURNAL, "title": "Updated Title"}
    resp = client.put(f"/api/journals/{created['id']}", json=updated_payload)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Title"


def test_delete_journal_returns_204(client):
    created = client.post("/api/journals", json=JOURNAL).json()
    resp = client.delete(f"/api/journals/{created['id']}")
    assert resp.status_code == 204


def test_delete_journal_not_found_returns_404(client):
    resp = client.delete("/api/journals/does-not-exist")
    assert resp.status_code == 404
