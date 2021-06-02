from logging import getLogger

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from mysql_client import mysql

from .auth import get_current_active_user
from .models import Note, User

router = APIRouter()
logger = getLogger(__name__)


@router.get("")
def get_all_notes(current_user: User = Depends(get_current_active_user)):
    print(current_user)
    logger.info(f"Current use is {current_user.username}")
    logger.info("Get all notes")
    query = f"SELECT * FROM notes WHERE user_id = {current_user.id};"
    try:
        results = mysql.execute_fetch_query(query)
        response_content = [{"id": result[0], "title": result[2], "description": result[3]} for result in results]
        return JSONResponse(status_code=status.HTTP_200_OK, content={"notes": response_content})
    except Exception as e:
        logger.error(f"Failed to get all notes: {e}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{note_id}")
def get_note_by_id(note_id: int):
    logger.info(f"Get note by id: id = {note_id}")
    query = f"SELECT * FROM notes WHERE id = {note_id};"
    try:
        result = mysql.execute_fetch_query(query)[0]
        response = {"id": result[0], "title": result[2], "description": result[3]}
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
    except Exception as e:
        logger.error(f"Error happened: {e}")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Note not found"})


@router.post("")
def post_new_note(note: Note, current_user: User = Depends(get_current_active_user)):
    note_dict = note.dict()
    logger.info(f"Create a new note: {note_dict}")
    try:
        user_id = current_user.id
        title = note_dict["title"]
        description = note_dict["description"]
        query = f"""INSERT INTO notes (user_id, title, description) VALUES ("{user_id}", "{title}", "{description}");"""
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


@router.put("/{note_id}")
def put_note_by_note_id(note_id: str, note: Note):
    note_dict = note.dict()
    logger.info(f"Update note by id: id = {note_id}")
    try:
        title = note_dict["title"]
        description = note_dict["description"]
        query = f"""UPDATE notes SET title="{title}", description="{description}" WHERE id = {note_id};"""
        mysql.execute_commit_query(query)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "The note is updated successfully"})
    except Exception as e:
        logger.error(f"Error occurred while updating a note: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Failed to be updated"},
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
