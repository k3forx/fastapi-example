# from app.main import app
# from fastapi.testclient import TestClient
# import unittest
# from unittest.mock import patch
# from pymysql.err import OperationalError
# from datetime import datetime

# client = TestClient(app)


# class TestNotesAPI(unittest.TestCase):
#     @patch("app.api.notes.mysql")
#     def test_get_note_by_id_without_error(self, mock_mysql):
#         mock_mysql.execute_fetch_query.return_value = [[1, 'Beyond the legacy code',
#                                                         'Awesome book!', datetime(2021, 4, 14, 0, 14, 14)]]
#         expect = {"id": 1, "title": "Beyond the legacy code",
#                   "description": "Awesome book!"}
#         response = client.get("/notes/1/")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), expect)

#     @ patch("app.api.notes.mysql")
#     def test_get_note_by_id_with_error(self, mock_mysql):
#         mock_mysql.execute_fetch_query.side_effect = OperationalError
#         expect = {"detail": "Note not found"}
#         response = client.get("/notes/1/")
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json(), expect)


# if __name__ == "__main__":
#     unittest.main()
