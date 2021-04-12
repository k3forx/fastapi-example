"""Functions related to manipulating MySQL database."""
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
            with self.__db_connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return results
        except Exception as e:
            logger.error(e)

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
        is_connection_established = self.__db_connection.open()
        if is_connection_established:
            return
        else:
            try:
                self.__db_connection.ping(reconnect=True)
                return
            except Exception as e:
                logger.error(f"Failed to reconnect {e}")
