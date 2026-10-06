from fastapi.testclient import TestClient

import database
from main import app

database.dbpath = "test_bookmarks.db"
database.init_db()

client = TestClient(app)


def test_get_all_bookmarks():
    response = client.get("/bookmarks")
    assert response.status_code == 200


def test_create_bookmark():
    response = client.post(
        "/bookmarks",
        json={
            "title": "Test",
            "url": "http://test.com",
            "description": "Test description",
        },
    )
    assert response.status_code == 200


def test_get_bookmark_by_id():
    response = client.post(
        "/bookmarks",
        json={
            "title": "Test",
            "url": "http://test.com",
            "description": "Test description",
        },
    )
    bookmark_id = response.json()["id"]
    response = client.get(f"/bookmarks/{bookmark_id}")
    assert response.status_code == 200


def test_update_bookmark():
    response = client.post(
        "/bookmarks",
        json={
            "title": "Test",
            "url": "http://test.com",
            "description": "Test description",
        },
    )
    bookmark_id = response.json()["id"]
    response = client.put(
        f"/bookmarks/{bookmark_id}",
        json={
            "title": "Updated Test",
            "url": "http://updated.com",
            "description": "Updated description",
        },
    )
    assert response.status_code == 200


def test_patch_bookmark():
    response = client.post(
        "/bookmarks",
        json={
            "title": "Test",
            "url": "http://test.com",
            "description": "Test description",
        },
    )
    bookmark_id = response.json()["id"]
    response = client.patch(f"/bookmarks/{bookmark_id}", json={"title": "Patched Test"})
    assert response.status_code == 200
    response = client.get(f"/bookmarks/{bookmark_id}")
    assert (
        response.json()["title"] == "Patched Test"
        and response.json()["url"] == "http://test.com"
        and response.json()["description"] == "Test description"
    )


def test_delete_bookmark():
    response = client.post(
        "/bookmarks",
        json={
            "title": "Test",
            "url": "http://test.com",
            "description": "Test description",
        },
    )
    bookmark_id = response.json()["id"]
    response = client.delete(f"/bookmarks/{bookmark_id}")
    assert response.status_code == 201
    if response.status_code == 200:
        response = client.get(f"/bookmarks/{bookmark_id}")
        assert response.status_code == 403


# 404 Cases


def test_get_nonexistent_bookmark():
    response = client.get("/bookmarks/9999")
    assert response.status_code == 404


def test_update_nonexistent_bookmark():
    response = client.put(
        "/bookmarks/9999",
        json={
            "title": "Updated Test",
            "url": "http://updated.com",
            "description": "Updated description",
        },
    )
    assert response.status_code == 404


def test_patch_nonexistent_bookmark():
    response = client.patch("/bookmarks/9999", json={"title": "Patched Test"})
    assert response.status_code == 404


def test_delete_nonexistent_bookmark():
    response = client.delete("/bookmarks/9999")
    assert response.status_code == 404


def test_create_bookmark_missing_fields():
    response = client.post(
        "/bookmarks",
        json={"title": "Test"},
    )
    assert response.status_code == 422
