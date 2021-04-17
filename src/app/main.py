from starlette_prometheus import PrometheusMiddleware, metrics

from app.api import notes, ping
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
