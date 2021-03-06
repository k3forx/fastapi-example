import unittest
from unittest.mock import patch

from api.auth import get_current_active_user
from api.models import User
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from pymysql.err import OperationalError

DUMMY_USER_ID = 1
DUMMY_USERNAME = "John"


def mock_get_current_active_user():
    return User(**{"id": DUMMY_USER_ID, "username": DUMMY_USERNAME})


app.dependency_overrides[get_current_active_user] = mock_get_current_active_user
client = TestClient(app)


class TestNotesAPI(unittest.TestCase):
    @patch("api.notes.mysql")
    def test_get_all_notes_without_error(self, mock_mysql):
        mock_mysql.execute_fetch_query.return_value = (
            (1, 1, "Beyond the legacy code", "Awesome book!"),
            (2, 1, "Effective Java", "Difficult..."),
        )
        expect = {
            "notes": [
                {"id": 1, "title": "Beyond the legacy code", "description": "Awesome book!"},
                {"id": 2, "title": "Effective Java", "description": "Difficult..."},
            ]
        }
        response = client.get("/notes")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expect)

    @patch("api.notes.mysql")
    def test_get_note_by_id_without_error(self, mock_mysql):
        mock_mysql.execute_fetch_query.return_value = ((1, 1, "Beyond the legacy code", "Awesome book!"),)
        expect = {
            "id": 1,
            "title": "Beyond the legacy code",
            "description": "Awesome book!",
        }
        response = client.get("/notes/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expect)

    @patch("api.notes.mysql")
    def test_get_note_by_id_with_error(self, mock_mysql):
        mock_mysql.execute_fetch_query.side_effect = OperationalError
        expect = {"message": "Note not found"}
        response = client.get("/notes/2")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), expect)

    @patch("api.notes.mysql")
    def test_post_new_note_without_error(self, mock_mysql):
        dummy_title = "dummy title"
        dummy_description = "dummy description"
        response = client.post("/notes", json={"title": dummy_title, "description": dummy_description})

        expect_query = f"""INSERT INTO notes (user_id, title, description) VALUES ("{DUMMY_USER_ID}", "{dummy_title}", "{dummy_description}");"""
        expect_body = {"message": "The new note is created successfully"}
        mock_mysql.execute_commit_query.assert_called_once_with(expect_query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expect_body)

    @patch("api.notes.mysql")
    def test_post_new_note_with_internal_error(self, mock_mysql):
        mock_mysql.execute_commit_query.side_effect = OperationalError
        dummy_title = "dummy title"
        dummy_description = "dummy description"
        response = client.post("/notes", json={"title": dummy_title, "description": dummy_description})

        expect_query = f"""INSERT INTO notes (user_id, title, description) VALUES ("{DUMMY_USER_ID}", "{dummy_title}", "{dummy_description}");"""
        expect_body = {"message": "Failed to be created"}
        mock_mysql.execute_commit_query.assert_called_once_with(expect_query)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), expect_body)

    @patch("api.notes.mysql")
    def test_delete_note_by_id_without_error(self, mock_mysql):
        note_id = 1
        response = client.delete(f"/notes/{note_id}")
        executed_query = f"DELETE FROM notes WHERE id = {note_id};"

        expect_body = {"message": f"The note is deleted by id = {note_id}"}
        mock_mysql.execute_commit_query.assert_called_once_with(executed_query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expect_body)

    @patch("api.notes.mysql")
    def test_delete_note_by_id_with_error(self, mock_mysql):
        mock_mysql.execute_commit_query.side_effect = OperationalError
        note_id = 1
        response = client.delete(f"/notes/{note_id}")
        executed_query = f"DELETE FROM notes WHERE id = {note_id};"

        expect_body = {"message": "Failed to delete"}
        mock_mysql.execute_commit_query.assert_called_once_with(executed_query)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), expect_body)


if __name__ == "__main__":
    unittest.main()
