import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from api.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    OAuth2PasswordRequestForm,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_current_user,
    get_password_hash,
    get_user,
    verify_password,
)
from api.models import UserInDB
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from main import app
from pydantic import BaseModel
from pymysql.err import InternalError


class FormData(BaseModel):
    username: str
    password: str


def mock_oauth_password_request_form():
    form_data = {"username": "test_user", "password": "test_pass"}
    return FormData(**form_data)


def mock_get_current_user():
    dummy_user_name = "user_A"
    datetime_now = datetime.now()
    user_info = {
        "id": 1,
        "username": dummy_user_name,
        "hashed_password": "hashed_pass",
        "disabled": False,
        "created_at": datetime_now,
    }
    return UserInDB(**user_info)


app.dependency_overrides[OAuth2PasswordRequestForm] = mock_oauth_password_request_form
app.dependency_overrides[get_current_user] = mock_get_current_user
client = TestClient(app)


class TestAuthAPI(unittest.TestCase):
    @patch("api.auth.pwd_context")
    def test_verify_password(self, mock_pwd_context):
        dummy_raw_password = "dummy_raw_password"
        dummy_hashed_password = "dummy_hashed_password"
        verify_password(dummy_raw_password, dummy_hashed_password)
        mock_pwd_context.verify.assert_called_once()

    @patch("api.auth.pwd_context")
    def test_get_password_hash(self, mock_pwd_context):
        dummy_password = "dummy_password"
        get_password_hash(dummy_password)
        mock_pwd_context.hash.assert_called_once_with(dummy_password)

    @patch("api.auth.mysql")
    def test_get_not_existing_user(self, mock_mysql):
        mock_mysql.execute_fetch_query.return_value = ([],)
        dummy_user_name = "dummy_user_name"
        response = get_user(dummy_user_name)
        self.assertIsNone(response)

    @patch("api.auth.mysql")
    def test_get_existing_user(self, mock_mysql):
        dummy_user_name = "user_A"
        datetime_now = datetime.now()
        query_result = {
            "id": 1,
            "username": dummy_user_name,
            "hashed_password": "hashed_pass",
            "disabled": False,
            "created_at": datetime_now,
        }
        mock_mysql.execute_fetch_query.return_value = (list(query_result.values()),)
        response = get_user(dummy_user_name)
        self.assertEqual(response, UserInDB(**query_result))

    @patch("api.auth.verify_password")
    @patch("api.auth.get_user")
    def test_authenticate_user_with_success(self, mock_get_user, mock_verify_password):
        datetime_now = datetime.now()
        dummy_username = "dummy_username"
        dummy_password = "dummy_password"
        user_info = {
            "id": 1,
            "username": dummy_username,
            "hashed_password": "hashed_pass",
            "disabled": False,
            "created_at": datetime_now,
        }

        dummy_user = UserInDB(**user_info)
        mock_get_user.return_value = dummy_user
        mock_verify_password.return_value = True

        response = authenticate_user(dummy_username, dummy_password)

        mock_get_user.assert_called_once_with(dummy_username)
        mock_verify_password.assert_called_once_with(dummy_password, dummy_user.hashed_password)
        self.assertEqual(response, dummy_user)

    @patch("api.auth.verify_password")
    @patch("api.auth.get_user")
    def test_authenticate_not_existing_user(self, mock_get_user, mock_verify_password):
        dummy_username = "dummy_username"
        dummy_password = "dummy_password"
        mock_get_user.return_value = None

        response = authenticate_user(dummy_username, dummy_password)

        mock_get_user.assert_called_once_with(dummy_username)
        mock_verify_password.assert_not_called()
        self.assertFalse(response)

    @patch("api.auth.verify_password")
    @patch("api.auth.get_user")
    def test_authenticate_user_with_wrong_password(self, mock_get_user, mock_verify_password):
        datetime_now = datetime.now()
        dummy_username = "dummy_username"
        dummy_password = "dummy_password"
        user_info = {
            "id": 1,
            "username": dummy_username,
            "hashed_password": "hashed_pass",
            "disabled": False,
            "created_at": datetime_now,
        }

        dummy_user = UserInDB(**user_info)
        mock_get_user.return_value = dummy_user
        mock_verify_password.return_value = False

        response = authenticate_user(dummy_username, dummy_password)

        mock_get_user.assert_called_once_with(dummy_username)
        mock_verify_password.assert_called_once_with(dummy_password, dummy_user.hashed_password)
        self.assertFalse(response)

    @patch("api.auth.jwt")
    def test_create_access_token_with_expires_delta(self, mock_jwt):
        data = {"sub": "test"}
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expected_value = "dummy_token"
        mock_jwt.encode.return_value = expected_value

        response = create_access_token(data, expires_delta)

        mock_jwt.encode.assert_called_once()
        self.assertEqual(response, expected_value)

    @patch("api.auth.jwt")
    def test_create_access_token_without_expires_delta(self, mock_jwt):
        data = {"sub": "test"}
        expected_value = "dummy_token"
        mock_jwt.encode.return_value = expected_value

        response = create_access_token(data)

        mock_jwt.encode.assert_called_once()
        self.assertEqual(response, expected_value)

    async def test_get_current_active_user_without_HTTP_400_BAD_REQUEST(self):
        datetime_now = datetime.now()
        dummy_username = "dummy_username"
        user_info = {
            "id": 1,
            "username": dummy_username,
            "hashed_password": "hashed_pass",
            "disabled": False,
            "created_at": datetime_now,
        }
        dummy_user = UserInDB(**user_info)
        response = await get_current_active_user()
        self.assertEqual(response, dummy_user)

    async def test_get_current_active_user_with_HTTP_400_BAD_REQUEST(self):
        datetime_now = datetime.now()
        dummy_username = "dummy_username"
        user_info = {
            "id": 1,
            "username": dummy_username,
            "hashed_password": "hashed_pass",
            "disabled": True,
            "created_at": datetime_now,
        }
        dummy_user = UserInDB(**user_info)
        with self.assertRaises(HTTPException):
            response = await get_current_active_user(dummy_user)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.json(), {"detail": "Inactive user"})

    @patch("api.auth.authenticate_user")
    def test_login_for_access_token_without_HTTPException(self, mock_authenticate_user):
        mock_authenticate_user.return_value = UserInDB(
            **{
                "id": 1,
                "username": "test_user",
                "hashed_password": "hashed_pass",
                "created_at": datetime.now(),
                "disabled": False,
            }
        )
        response = client.post("/token")
        response_body = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_body.keys()), ["access_token", "token_type"])
        self.assertEqual(response_body["token_type"], "bearer")

    @patch("api.auth.authenticate_user")
    def test_login_for_token_with_HTTPException(self, mock_authenticate_user):
        mock_authenticate_user.return_value = None
        response = client.post("/token")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "Incorrect username or password"})

    @patch("api.auth.mysql")
    def test_register_new_user_without_exception(self, mock_mysql):
        response = client.post("/register", json={"username": "test_user", "raw_password": "raw_test_pass"})
        mock_mysql.execute_commit_query.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "The user is successfully created"})

    @patch("api.auth.mysql")
    def test_register_new_user_with_exception(self, mock_mysql):
        mock_mysql.execute_commit_query.side_effect = InternalError
        response = client.post("/register", json={"username": "test_user", "raw_password": "raw_test_pass"})
        mock_mysql.execute_commit_query.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {"detail": "Failed to register a new user"})


if __name__ == "__main__":
    unittest.main()
