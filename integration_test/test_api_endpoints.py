import json

import requests

BASE_ENDPOINT = "http://localhost:8000"
normal_status = 200
note_id = 1


def test_GET_ping():
    path = "/ping"

    expect_content = {"ping": "pong!"}
    r = requests.get(BASE_ENDPOINT + path)

    assert r.status_code == normal_status
    assert r.json() == expect_content


def test_GET_note_by_id():
    path = f"/notes/{note_id}/"

    expect_content = {
        "id": 1,
        "title": "Beyond the legacy code",
        "description": "Awesome book!",
    }
    r = requests.get(BASE_ENDPOINT + path)

    assert r.status_code == normal_status
    assert r.json() == expect_content


def test_POST_note():
    payload = {
        "title": "Engineering Organization Theory",
        "description": "Interasting book!",
    }
    expect_body = {"message": "The new note is created successfully"}

    response = requests.post(f"{BASE_ENDPOINT}/notes", data=json.dumps(payload))

    assert response.status_code == normal_status
    assert response.json() == expect_body


def test_DELETE_note():
    path = f"/notes/{note_id}"

    expect_body = {"message": f"The note is deleted by id = {note_id}"}
    response = requests.delete(BASE_ENDPOINT + path)

    assert response.status_code == normal_status
    assert response.json() == expect_body
