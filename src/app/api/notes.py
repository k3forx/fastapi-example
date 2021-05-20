from typing import Optional

from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.mysql_client import mysql
from app.utils import get_logger
from fastapi import APIRouter, HTTPException

router = APIRouter()
logger = get_logger()


class Note(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


@router.get("/{note_id}")
def get_note_by_id(note_id: int):
    logger.info(f"Get note by id: id = {note_id}")
    query = f"SELECT * FROM notes WHERE id = {note_id};"
    try:
        result = mysql.execute_fetch_query(query)[0]
        response = {"id": result[0], "title": result[1], "description": result[2]}
        return response
    except Exception as e:
        logger.error(f"Error happened {e}")
        raise HTTPException(status_code=404, detail="Note not found")


@router.post("")
def post_new_note(note: Note):
    note_dict = note.dict()
    logger.info(f"Create a new note: {note_dict}")
    try:
        title = note_dict["title"]
        description = note_dict["description"]
        query = f"""INSERT INTO notes (title, description) VALUES ("{title}", "{description}");"""
        mysql.execute_commit_query(query)
        return JSONResponse(
            status_code=200, content={"message": "The new note is created successfully"}
        )
    except Exception as e:
        logger.error(f"Error occurred while creating a note: {e}")
        raise HTTPException(status_code=500, detail="Failed to be created")


@router.delete("/{note_id}")
def delete_note_by_note_id(note_id: int):
    logger.info(f"Delete note by id: id = {note_id}")
    query = f"DELETE FROM notes WHERE id = {note_id};"
    try:
        mysql.execute_commit_query(query)
        return JSONResponse(
            status_code=200,
            content={"message": f"The note is deleted by id = {note_id}"},
        )
    except Exception as e:
        logger.error(f"{e}: failed to delete note by id = {note_id}")
        raise HTTPException(status_code=500, detail="Failed to delete")
