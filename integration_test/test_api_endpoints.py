import requests

BASE_ENDPOINT = "http://localhost:8002"


def test_GET_ping():
    path = "/ping"

    expect_status_code = 200
    expect_content = {"ping": "pong!"}
    r = requests.get(BASE_ENDPOINT + path)

    assert r.status_code == expect_status_code
    assert r.json() == expect_content


def test_GET_note_by_id():
    note_id = 1
    path = f"/notes/{note_id}/"

    expect_status_code = 200
    expect_content = {"id": 1, "title": "Beyond the legacy code", "description": "Awesome book!"}
    r = requests.get(BASE_ENDPOINT + path)

    assert r.status_code == expect_status_code
    assert r.json() == expect_content
