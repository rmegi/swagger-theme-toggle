# swagger-theme-toggle

Adds a Light / Dark / Auto theme toggle to FastAPI's Swagger UI docs page.

## Install

```bash
uv add swagger-theme-toggle
```

## Usage

```python
from fastapi import FastAPI
from swagger_theme_toggle import add_dark_mode_toggle

app = FastAPI()

# ... register your routes ...

add_dark_mode_toggle(app)
```

Call `add_dark_mode_toggle` last, after your routes and app settings (title,
`openapi_url`) are finalized — it snapshots them to build the replacement
`/docs` route.

### Options

```python
add_dark_mode_toggle(
    app,
    docs_url="/docs",       # where to mount the docs page
    default_theme="system", # "light" | "dark" | "system"
)
```

The chosen theme is persisted in the browser's `localStorage`, so it survives
reloads. "system" follows the OS `prefers-color-scheme`.

## Development

```bash
uv sync
uv run pytest
```
