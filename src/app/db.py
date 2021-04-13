from os import getenv
from app.utils import get_logger
import pymysql

logger = get_logger()


class MySQL:
    def __init__(self, db_config):
        self.__db_config = db_config

    def make_connection(self):
        try:
            self.__db_connection = pymysql.connect(
                **self.__db_config)
        except Exception as e:
            logger.error("Cannot connect to mysql")
            raise e

    def execute_fetch_query(self, query):
        self.__reconnect_to_db()
        try:
            logger.info("Executing query...")
            with self.__db_connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                logger.info("Successfully getting the results")
                return results
        except Exception as e:
            logger.error(f"Error occur while executing query: {e}")

    def execute_commit_query(self, query):
        self.__reconnect_to_db()
        try:
            with self.__db_connection.cursor() as cursor:
                cursor.execute(query)
                self.__commit_query()
        except Exception as e:
            logger.error(e)

    def close_connection(self):
        self.__db_connection.close()
        logger.info("Close the connection")

    def __commit_query(self):
        self.__db_connection.commit()

    def __reconnect_to_db(self):
        is_connection_established = self.__db_connection.open
        if is_connection_established:
            logger.info("Connection is already established")
            return
        else:
            try:
                logger.info("Reconnecting to the database...")
                self.__db_connection.ping(reconnect=True)
                return
            except Exception as e:
                logger.error(f"Failed to reconnect {e}")


db_config = {
    "host": getenv("MYSQL_HOST"),
    "user": getenv("MYSQL_USER"),
    "db": getenv("MYSQL_DATABASE"),
    "password": getenv("MYSQL_PASSWORD"),
    "charset": "utf8mb4",
}
mysql = MySQL(db_config)
