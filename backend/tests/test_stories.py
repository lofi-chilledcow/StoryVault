from tests.conftest import STORY


def test_create_story_returns_201_with_id(client):
    resp = client.post("/api/stories", json=STORY)
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["title"] == STORY["title"]
    assert data["themes"] == STORY["themes"]


def test_create_story_missing_title_returns_422(client):
    payload = {k: v for k, v in STORY.items() if k != "title"}
    resp = client.post("/api/stories", json=payload)
    assert resp.status_code == 422


def test_list_stories_returns_list(client):
    client.post("/api/stories", json=STORY)
    resp = client.get("/api/stories")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) == 1


def test_get_story_not_found_returns_404(client):
    resp = client.get("/api/stories/does-not-exist")
    assert resp.status_code == 404


def test_delete_story_returns_204(client):
    created = client.post("/api/stories", json=STORY).json()
    resp = client.delete(f"/api/stories/{created['id']}")
    assert resp.status_code == 204
