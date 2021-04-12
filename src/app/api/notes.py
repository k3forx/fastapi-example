from fastapi import APIRouter
from app.db import mysql

router = APIRouter()


@router.get("/{note_id}/")
def get_note_by_id(note_id: int):
    query = f"SELECT * FROM notes WHERE id = {note_id};"
    result = mysql.execute_fetch_query(query)
    return result
