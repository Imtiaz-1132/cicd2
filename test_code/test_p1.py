# test_p1.py
import pytest
from fastapi.testclient import TestClient

# Import your FastAPI app
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src_code')))

from p1 import api  # import the FastAPI instance

client = TestClient(api)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Book Management System"}


def test_add_book():
    book_data = {
        "id": 1,
        "name": "Python Basics",
        "description": "Intro to Python",
        "isAvailable": True
    }
    response = client.post("/book", json=book_data)
    assert response.status_code == 200
    assert any(book["id"] == 1 for book in response.json())


def test_get_books():
    response = client.get("/book")
    assert response.status_code == 200
    books = response.json()
    assert isinstance(books, list)
    assert len(books) >= 1  # At least one book should exist after adding


def test_update_book():
    updated_data = {
        "id": 1,
        "name": "Python Advanced",
        "description": "Advanced Python Topics",
        "isAvailable": False
    }
    response = client.put("/book/1", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Python Advanced"
    assert data["isAvailable"] is False


def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    # After deletion, the book should not exist
    response = client.get("/book")
    books = response.json()
    assert all(book["id"] != 1 for book in books)
