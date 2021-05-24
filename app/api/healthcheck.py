from logging import getLogger

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from mysql_client import mysql

router = APIRouter()
logger = getLogger(__name__)


@router.get("/health")
def health_check():
    try:
        mysql.ping()
        logger.info("Application is healthy")
        return JSONResponse(status_code=status.HTTP_200_OK, content={"is_healthy": "true"})
    except Exception as e:
        logger.error(f"Application is not healthy: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"is_healthy": "false"},
        )
