from fastapi import FastAPI
from app.mysql_client import mysql
from app.api import ping, notes

app = FastAPI()

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
