from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/ping")
def pong():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"ping": "pong!"})
