import pytest
from flask import json

from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_todos(client):
    rv = client.get("/todos/")
    assert rv.status_code == 200
    assert len(json.loads(rv.data)) == 3


def test_post_todo(client):
    rv = client.post("/todos/", json={"task": "new task"})
    assert rv.status_code == 201
    assert json.loads(rv.data)["task"] == "new task"


def test_get_todo(client):
    rv = client.get("/todos/1")
    assert rv.status_code == 200
    assert json.loads(rv.data)["task"] == "Build an API"


def test_update_todo(client):
    rv = client.put("/todos/1", json={"task": "updated task"})
    assert rv.status_code == 200
    assert json.loads(rv.data)["task"] == "updated task"


def test_delete_todo(client):
    rv = client.delete("/todos/1")
    assert rv.status_code == 204
