import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from swagger_theme_toggle import add_dark_mode_toggle


def test_docs_route_returns_html_with_toggle(app: FastAPI) -> None:
    add_dark_mode_toggle(app)
    client = TestClient(app)

    response = client.get("/docs")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "stt-toggle" in response.text
    assert "swagger-theme-toggle:theme" in response.text


def test_docs_route_embeds_theme_css_and_js(app: FastAPI) -> None:
    add_dark_mode_toggle(app)
    client = TestClient(app)

    html = client.get("/docs").text

    assert 'data-theme="dark"' in html
    assert "localStorage" in html
    assert "SwaggerUIBundle" in html


def test_default_docs_route_is_replaced_exactly_once(app: FastAPI) -> None:
    add_dark_mode_toggle(app)

    docs_routes = [r for r in app.router.routes if getattr(r, "path", None) == "/docs"]
    assert len(docs_routes) == 1


def test_default_theme_is_configurable(app: FastAPI) -> None:
    add_dark_mode_toggle(app, default_theme="dark")
    client = TestClient(app)

    html = client.get("/docs").text

    assert '|| "dark"' in html


@pytest.mark.parametrize("docs_url", ["/api-docs", "/documentation"])
def test_custom_docs_url(app: FastAPI, docs_url: str) -> None:
    add_dark_mode_toggle(app, docs_url=docs_url)
    client = TestClient(app)

    response = client.get(docs_url)

    assert response.status_code == 200
    assert client.get("/docs").status_code == 404


def test_raises_without_openapi_url() -> None:
    app = FastAPI(openapi_url=None)

    with pytest.raises(ValueError, match="openapi_url"):
        add_dark_mode_toggle(app)


def test_existing_routes_are_preserved(app: FastAPI, client: TestClient) -> None:
    add_dark_mode_toggle(app)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
