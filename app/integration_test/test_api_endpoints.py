import json
from os import access, environ

import requests

BASE_ENDPOINT = "http://localhost:8000"
normal_status = 200
note_id = 1


def get_access_token():
    path = "/token"
    data = {"username": "test", "password": "test"}
    r = requests.post(BASE_ENDPOINT + path, data=data)
    access_token = r.json()["access_token"]
    return access_token


def test_health():
    expected_result = {"is_healthy": "true"}
    response = requests.get(BASE_ENDPOINT + "/health")

    assert response.status_code == normal_status
    assert response.json() == expected_result


def test_GET_all_notes():
    access_token = get_access_token()
    path = "/notes"
    expected_body = {
        "notes": [
            {"id": 1, "title": "Beyond the legacy code", "description": "Awesome book!"},
            {"id": 2, "title": "Effective Java", "description": "Difficult..."},
        ]
    }

    headers = {"accept": "application/json", "Authorization": f"Bearer {access_token}"}
    r = requests.get(BASE_ENDPOINT + path, headers=headers)

    assert r.status_code == normal_status
    assert r.json() == expected_body


def test_GET_note_by_id():
    path = f"/notes/1"

    expect_content = {
        "id": 1,
        "title": "Beyond the legacy code",
        "description": "Awesome book!",
    }
    r = requests.get(BASE_ENDPOINT + path)

    assert r.status_code == normal_status
    assert r.json() == expect_content


def test_POST_note():
    access_token = get_access_token()
    payload = {
        "title": "Engineering Organization Theory",
        "description": "興味深い本ですね",
    }
    expect_body = {"message": "The new note is created successfully"}

    headers = {"accept": "application/json", "Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_ENDPOINT}/notes", headers=headers, data=json.dumps(payload))

    assert response.status_code == normal_status
    assert response.json() == expect_body


def test_DELETE_note():
    path = f"/notes/{note_id}"

    expect_body = {"message": f"The note is deleted by id = {note_id}"}
    response = requests.delete(BASE_ENDPOINT + path)

    assert response.status_code == normal_status
    assert response.json() == expect_body
