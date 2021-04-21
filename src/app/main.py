from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.api import notes, ping
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(
    PrometheusMiddleware, app_name="fastapi", group_paths=True, prefix="fastapi"
)
app.add_route("/metrics", handle_metrics)

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
