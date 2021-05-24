from logging import getLogger
from typing import Optional

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from mysql_client import mysql
from pydantic import BaseModel

router = APIRouter()
logger = getLogger(__name__)


class Note(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


@router.get("")
def get_note_by_id(id: str):
    logger.info(f"Get note by id: id = {id}")
    query = f"SELECT * FROM notes WHERE id = {id};"
    try:
        result = mysql.execute_fetch_query(query)[0]
        response = {"id": result[0], "title": result[1], "description": result[2]}
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
    except Exception as e:
        logger.error(f"Error happened: {e}")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Note not found"})


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
            status_code=status.HTTP_200_OK,
            content={"message": "The new note is created successfully"},
        )
    except Exception as e:
        logger.error(f"Error occurred while creating a note: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to be created"},
        )


@router.delete("/{note_id}")
def delete_note_by_note_id(note_id: int):
    logger.info(f"Delete note by id: id = {note_id}")
    query = f"DELETE FROM notes WHERE id = {note_id};"
    try:
        mysql.execute_commit_query(query)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"The note is deleted by id = {note_id}"},
        )
    except Exception as e:
        logger.error(f"{e}: failed to delete note by id = {note_id}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to delete"},
        )
