from logging import getLogger
from os import getenv
from typing import Any, Dict

import pymysql

logger = getLogger(__name__)


class MySQLClient:
    def __init__(self, db_config: Dict[str, Any]) -> None:
        self.__db_config = db_config
        self.__is_connection_alive = False

    def execute_fetch_query(self, query: str) -> Any:
        self.__make_connection_to_db()
        try:
            logger.info("Executing query...")
            with self.__db_connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                logger.info("Successfully getting the result")
                return results
        except Exception as e:
            self.__close_connection()
            logger.error(f"Error occurred while executing query: {e}")
            raise e

    def execute_commit_query(self, query: str) -> Any:
        self.__make_connection_to_db()
        try:
            logger.info("Executing query...")
            with self.__db_connection.cursor() as cursor:
                cursor.execute(query)
                self.__commit()
                logger.info("Successfully committed")
                return
        except Exception as e:
            self.__close_connection()
            logger.error(f"Error occurred while commting query: {e}")
            raise e

    def ping(self) -> None:
        self.__make_connection_to_db()

    def __make_connection_to_db(self) -> None:
        if self.__is_connection_alive:
            logger.info("Connection is alive")
            return
        else:
            logger.info("Create a new connection")
            try:
                self.__db_connection = pymysql.connect(**self.__db_config)
                self.__is_connection_alive = True
                logger.info("The connection is successfully established")
                return
            except Exception as e:
                logger.error(f"Error occurred while executing query: {e}")
                raise e

    def __commit(self) -> None:
        self.__db_connection.commit()

    def __close_connection(self) -> None:
        self.__db_connection.close()
        self.__is_connection_alive = False
        logger.info("Close the connection")


db_config = {
    "host": getenv("MYSQL_HOST"),
    "user": getenv("MYSQL_USER"),
    "db": getenv("MYSQL_DATABASE"),
    "password": getenv("MYSQL_PASSWORD"),
    "charset": "utf8mb4",
    "connect_timeout": int(getenv("MYSQL_CONNECT_TIMEOUT", 86400)),
}

mysql = MySQLClient(db_config)
