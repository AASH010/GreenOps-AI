"""Application factory with the health and metadata endpoints (skeleton for task PLT-01)."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__
from .config import Settings, load_settings
from .provenance import Provenance

PROTOTYPE_NOTICE = (
    "GreenOps AI is a competition prototype. Inputs are synthetic, replayed, estimated or simulated and "
    "are labelled as such; no production control is performed and no measured savings are claimed."
)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or load_settings()
    app = FastAPI(title="GreenOps AI backend", version=__version__)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/v1/meta")
    def meta() -> dict[str, object]:
        return {
            "name": "GreenOps AI",
            "version": __version__,
            "environment": settings.env,
            "provenance_labels": [label.value for label in Provenance],
            "prototype_notice": PROTOTYPE_NOTICE,
        }

    return app


app = create_app()
