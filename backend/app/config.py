"""Settings read from the process environment. See .env.example for the variable names."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    env: str
    host: str
    port: int
    cors_origins: tuple[str, ...]
    database_url: str


def load_settings(environ: Mapping[str, str] | None = None) -> Settings:
    """Build settings from the environment; invalid values raise ValueError."""
    source = os.environ if environ is None else environ
    port_text = source.get("GREENOPS_API_PORT", "8000")
    try:
        port = int(port_text)
    except ValueError as error:
        raise ValueError(f"GREENOPS_API_PORT must be an integer, got {port_text!r}") from error
    if not 1 <= port <= 65535:
        raise ValueError(f"GREENOPS_API_PORT must be between 1 and 65535, got {port}")
    raw_origins = source.get("GREENOPS_CORS_ORIGINS", "http://localhost:5173")
    return Settings(
        env=source.get("GREENOPS_ENV", "development"),
        host=source.get("GREENOPS_API_HOST", "127.0.0.1"),
        port=port,
        cors_origins=tuple(o.strip() for o in raw_origins.split(",") if o.strip()),
        database_url=source.get("GREENOPS_DATABASE_URL", ""),
    )
