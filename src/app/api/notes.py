from fastapi import APIRouter, HTTPException
from app.db import mysql

router = APIRouter()


@router.get("/{note_id}/")
def get_note_by_id(note_id: int):
    query = f"SELECT * FROM notes WHERE id = {note_id};"
    try:
        result = mysql.execute_fetch_query(query)[0]
        response = {"id": result[0],
                    "title": result[1], "description": result[2]}
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail="Note not found")
