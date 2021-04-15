import unittest
from unittest.mock import MagicMock, patch

from pymysql import InternalError

from app.mysql_client import MySQLClient


class TestMySQLClient(unittest.TestCase):
    def setUp(self):
        self.db_config = {"host": "host", "port": "port", "hogehoge": "hogahoga"}

    @patch("app.mysql_client.pymysql")
    def test_execute_fetch_query_without_errors(self, mock_pymysql):
        expected_result = [{"client_id": 1}, {"client_id": 5}, {"client_id": 9}]
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_pymysql.connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = expected_result

        mysql = MySQLClient(self.db_config)
        query = "dummy query"

        actual_result = mysql.execute_fetch_query(query)

        mock_cursor.execute.assert_called_once_with(query)
        mock_cursor.fetchall.assert_called_once()
        self.assertEqual(actual_result, expected_result)

    @patch("app.mysql_client.pymysql")
    def test_execute_fetch_query_with_error_of_creating_connection(self, mock_pymysql):
        mock_pymysql.connect.side_effect = InternalError

        mysql = MySQLClient(self.db_config)
        query = "dummy query"

        with self.assertRaises(Exception):
            mysql.execute_fetch_query(query)
        mock_pymysql.connect.assert_called_once_with(**self.db_config)

    @patch("app.mysql_client.pymysql")
    def test_execute_fetch_query_with_error_of_executing_query(self, mock_pymysql):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_pymysql.connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = InternalError

        mysql = MySQLClient(self.db_config)
        query = "dummy query"

        with self.assertRaises(Exception):
            mysql.execute_fetch_query(query)
        mock_cursor.execute.assert_called_once_with(query)
        mock_conn.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
