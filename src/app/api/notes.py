from app.mysql_client import mysql
from app.utils import get_logger
from fastapi import APIRouter, HTTPException

router = APIRouter()
logger = get_logger()


@router.get("/{note_id}/")
def get_note_by_id(note_id: int):
    logger.info(f"Get note by id: id = {note_id}")
    query = f"SELECT * FROM notes WHERE id = {note_id};"
    try:
        result = mysql.execute_fetch_query(query)[0]
        response = {"id": result[0], "title": result[1], "description": result[2]}
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail="Note not found")
