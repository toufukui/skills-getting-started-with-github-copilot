import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture: Test client for FastAPI application"""
    return TestClient(app)
