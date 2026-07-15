from __future__ import annotations

from importlib import resources
from typing import Literal

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse

Theme = Literal["light", "dark", "system"]

_ASSETS = resources.files("swagger_theme_toggle.assets")


def _read_asset(name: str) -> str:
    return _ASSETS.joinpath(name).read_text(encoding="utf-8")


def _inject_theme(html: str, default_theme: Theme) -> str:
    css = _read_asset("theme.css")
    js = _read_asset("theme.js")
    injected = (
        f'<script>document.documentElement.dataset.theme = '
        f'localStorage.getItem("swagger-theme-toggle:theme") || "{default_theme}";</script>\n'
        f"<style>{css}</style>\n"
        f"<script>{js}</script>\n"
    )
    if "</head>" in html:
        return html.replace("</head>", injected + "</head>", 1)
    return html + injected


def add_dark_mode_toggle(
    app: FastAPI,
    *,
    docs_url: str = "/docs",
    default_theme: Theme = "system",
) -> None:
    """Replace the app's Swagger UI route with one that has a light/dark/system theme toggle.

    Must be called after all of the app's own routes and settings (title, openapi_url) are
    finalized, since it snapshots them to build the replacement docs route.
    """
    openapi_url = app.openapi_url
    if openapi_url is None:
        raise ValueError(
            "The FastAPI app must have an openapi_url configured to add Swagger UI docs."
        )

    title = f"{app.title} - Swagger UI"
    oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url
    swagger_ui_parameters = app.swagger_ui_parameters

    stale_paths = {app.docs_url, docs_url}
    app.router.routes = [
        route for route in app.router.routes if getattr(route, "path", None) not in stale_paths
    ]
    app.docs_url = None

    @app.get(docs_url, include_in_schema=False)
    async def custom_swagger_ui_html() -> HTMLResponse:
        response = get_swagger_ui_html(
            openapi_url=openapi_url,
            title=title,
            oauth2_redirect_url=oauth2_redirect_url,
            swagger_ui_parameters=swagger_ui_parameters,
        )
        html = response.body.decode("utf-8")
        return HTMLResponse(_inject_theme(html, default_theme))
