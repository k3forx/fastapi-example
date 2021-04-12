from fastapi import FastAPI
from app.db import mysql
from app.api import ping, notes
from app.utils import get_logger

logger = get_logger()

app = FastAPI()


@app.on_event("startup")
def startup():
    logger.info("Make connection to database")
    mysql.make_connection()


@app.on_event("shutdown")
def shutdown():
    mysql.close_connection()
    logger.info("Close connection to database")


app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
