import uvicorn
from fastapi import FastAPI, HTTPException

import database
from models import Bookmark, BookmarkOut, BookmarkPatch

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/bookmarks", response_model=BookmarkOut)
def create_bookmark(bookmark: Bookmark):
    new_id = database.create_bookmark(
        bookmark.title, bookmark.url, bookmark.description
    )
    if new_id is None:
        raise HTTPException(status_code=500, detail="Failed to create bookmark")
    return database.get_bookmark(new_id)


@app.get("/bookmarks", response_model=list[BookmarkOut])
def get_bookmarks():
    return database.get_all_bookmarks()


@app.get("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def get_by_id(bookmark_id: int):
    raise_exception(bookmark_id)
    return database.get_bookmark(bookmark_id)


@app.put("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def update_by_id(bookmark_id: int, bookmark: Bookmark):
    raise_exception(bookmark_id)
    database.update_bookmark(
        bookmark_id, bookmark.title, bookmark.url, bookmark.description
    )
    return database.get_bookmark(bookmark_id)


@app.patch("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def patch_by_id(bookmark_id: int, bookmark: BookmarkPatch):
    raise_exception(bookmark_id)
    existing_bookmark = database.get_bookmark(bookmark_id)
    if existing_bookmark is None:
        raise HTTPException(status_code=500, detail="Bookmark unexpectedly not found")
    updated_data = bookmark.model_dump(exclude_unset=True)
    combined_dict = existing_bookmark | updated_data
    database.update_bookmark(
        bookmark_id,
        combined_dict["title"],
        combined_dict["url"],
        combined_dict["description"],
    )
    return database.get_bookmark(bookmark_id)


@app.delete("/bookmarks/{bookmark_id}")
def delete_by_id(bookmark_id: int):
    raise_exception(bookmark_id)
    database.delete_bookmark(bookmark_id)
    return {"message": "Bookmark deleted successfully"}


def raise_exception(bookmark_id: int):
    if database.get_bookmark(bookmark_id) is None:
        raise HTTPException(status_code=404, detail="Bookmark not found")


database.init_db()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
