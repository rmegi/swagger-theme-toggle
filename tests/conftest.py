import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI(title="Test App")

    @app.get("/ping")
    def ping() -> dict[str, str]:
        return {"status": "ok"}

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
