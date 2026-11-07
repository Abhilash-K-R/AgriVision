"""Integration tests for AgriVision backend."""

import pytest
from backend.main import app
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_health_check():
    """Verify that the health endpoint returns a healthy response."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_predict_endpoint_missing_file():
    """Verify that prediction requests without an image are rejected."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/predict")
    assert response.status_code == 422
