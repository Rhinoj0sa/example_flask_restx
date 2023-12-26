import pytest
from flask import json
import app


def test_get_fruits(client):
    rv = client.get("/fruits/")
    assert rv.status_code == 200
    assert len(json.loads(rv.data)) == 3


def test_post_fruit(client):
    rv = client.post("/fruits/", json={"name": "new fruit", "qty": 5, "price": 1.2})
    assert rv.status_code == 201
    data = json.loads(rv.data)
    assert data["name"] == "new fruit"
    assert data["qty"] == 5
    assert data["price"] == 1.2


def test_get_fruit(client):
    fruit_id = app.FruitDAO.fruits[0]["id"]
    rv = client.get(f"/fruits/{fruit_id}")
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data["name"] == "Apple"
    assert data["qty"] == 10
    assert data["price"] == 0.5


def test_update_fruit(client):
    fruit_id = FruitDAO.fruits[0]["id"]
    rv = client.put(
        f"/fruits/{fruit_id}", json={"name": "updated fruit", "qty": 7, "price": 1.5}
    )
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data["name"] == "updated fruit"
    assert data["qty"] == 7
    assert data["price"] == 1.5


def test_delete_fruit(client):
    fruit_id = FruitDAO.fruits[0]["id"]
    rv = client.delete(f"/fruits/{fruit_id}")
    assert rv.status_code == 204
