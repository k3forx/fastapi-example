import json
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from pymysql import InternalError

from app.main import app
from fastapi import status

client = TestClient(app)


class TestNotesAPI(unittest.TestCase):
    @patch("app.api.healthcheck.mysql")
    def test_health(self, mock_mysql):
        response = client.get("/health")

        mock_mysql.ping.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"is_healthy": "true"})

    @patch("app.api.healthcheck.mysql")
    def test_health_with_error(self, mock_mysql):
        mock_mysql.ping.side_effect = InternalError

        response = client.get("/health")

        mock_mysql.ping.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"is_healthy": "false"})
