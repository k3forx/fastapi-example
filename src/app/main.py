from fastapi import FastAPI

from os import getenv
from app.db import MySQL
from app.api import ping

app = FastAPI()

db_config = {
    "host": getenv("MYSQL_HOST"),
    "user": getenv("MYSQL_USER"),
    "db": getenv("MYSQL_DATABASE"),
    "password": getenv("MYSQL_PASSWORD"),
    "charset": "utf8mb4",
}
mysql = MySQL(db_config)


@app.on_event("startup")
def startup():
    print(db_config)
    mysql.make_connection()


@app.on_event("shutdown")
def shutdown():
    mysql.close_connection()


app.include_router(ping.router)
