from fastapi import FastAPI

from swagger_theme_toggle import add_dark_mode_toggle

app = FastAPI(title="Demo API")


@app.get("/items/{item_id}", tags=["items"])
def read_item(item_id: int, q: str | None = None) -> dict:
    """Fetch a single item by its ID."""
    return {"item_id": item_id, "q": q}


@app.post("/items", tags=["items"])
def create_item(name: str) -> dict:
    """Create a new item."""
    return {"name": name}


@app.put("/items/{item_id}", tags=["items"])
def update_item(item_id: int, name: str) -> dict:
    """Replace an existing item."""
    return {"item_id": item_id, "name": name}


@app.delete("/items/{item_id}", tags=["items"])
def delete_item(item_id: int) -> dict:
    """Delete an item."""
    return {"item_id": item_id}


@app.patch("/items/{item_id}", tags=["items"])
def patch_item(item_id: int, name: str | None = None) -> dict:
    """Partially update an item."""
    return {"item_id": item_id, "name": name}


@app.get("/users/{user_id}", tags=["users"])
def read_user(user_id: int) -> dict:
    """Fetch a single user by ID."""
    return {"user_id": user_id}


add_dark_mode_toggle(app)
