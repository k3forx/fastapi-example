import json
from logging.config import dictConfig

from api import healthcheck, notes, ping
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

with open("log_config.json", "r", encoding="utf-8") as f:
    dictConfig(json.load(f))

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PrometheusMiddleware, app_name="fastapi", group_paths=True, prefix="fastapi")
app.add_route("/metrics", handle_metrics)

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(healthcheck.router)
