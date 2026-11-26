"""Tests for the backend skeleton: settings and the health and metadata endpoints."""

from __future__ import annotations

import pytest
from app import __version__
from app.config import Settings, load_settings
from app.main import PROTOTYPE_NOTICE, create_app
from fastapi.testclient import TestClient


def client(**overrides) -> TestClient:
    base = {
        "env": "test",
        "host": "127.0.0.1",
        "port": 8000,
        "cors_origins": ("http://localhost:5173",),
        "database_url": "",
    }
    return TestClient(create_app(Settings(**{**base, **overrides})))


def test_health_reports_ok():
    response = client().get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_meta_exposes_labels_environment_and_the_prototype_notice():
    body = client(env="test").get("/api/v1/meta").json()
    assert body["name"] == "GreenOps AI"
    assert body["version"] == __version__
    assert body["environment"] == "test"
    assert body["provenance_labels"] == ["MEASURED", "REPLAYED", "ESTIMATED", "SIMULATED"]
    assert body["prototype_notice"] == PROTOTYPE_NOTICE


def test_defaults_when_the_environment_is_empty():
    settings = load_settings({})
    assert (settings.env, settings.host, settings.port) == ("development", "127.0.0.1", 8000)
    assert settings.cors_origins == ("http://localhost:5173",)
    assert settings.database_url == ""


def test_environment_overrides_are_applied():
    settings = load_settings(
        {
            "GREENOPS_ENV": "production",
            "GREENOPS_API_HOST": "0.0.0.0",
            "GREENOPS_API_PORT": "9000",
            "GREENOPS_CORS_ORIGINS": "https://a.example, https://b.example",
            "GREENOPS_DATABASE_URL": "postgresql://placeholder",
        }
    )
    assert settings.env == "production" and settings.port == 9000
    assert settings.cors_origins == ("https://a.example", "https://b.example")
    assert settings.database_url == "postgresql://placeholder"


@pytest.mark.parametrize("value", ["abc", "0", "70000", ""])
def test_invalid_port_is_rejected(value):
    with pytest.raises(ValueError):
        load_settings({"GREENOPS_API_PORT": value})
