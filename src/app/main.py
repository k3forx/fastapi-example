from app.api import notes, ping
from app.mysql_client import mysql
from fastapi import FastAPI

app = FastAPI()

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
