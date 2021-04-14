import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestPingAPI(unittest.TestCase):
    def test_get_ping(self):
        response = client.get("/ping")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ping": "pong!"})


if __name__ == "__main__":
    unittest.main()
