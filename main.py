import json

import uvicorn
from fastapi import FastAPI, HTTPException

from models import Bookmark, BookmarkOut, BookmarkPatch

app = FastAPI()

bookmarks: dict[int, dict] = {}
next_id = 1


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/bookmarks", response_model=BookmarkOut)
def create_bookmark(bookmark: Bookmark):
    global next_id
    combined_dict = {"id": next_id} | bookmark.model_dump()
    bookmarks[next_id] = combined_dict
    new_id = next_id
    next_id = next_id + 1
    save_bookmarks()
    return bookmarks[new_id]


@app.get("/bookmarks", response_model=list[BookmarkOut])
def get_bookmarks():
    return list(bookmarks.values())


@app.get("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def get_by_id(bookmark_id: int):
    raise_exception(bookmark_id)
    return bookmarks[bookmark_id]


@app.put("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def update_by_id(bookmark_id: int, bookmark: Bookmark):
    raise_exception(bookmark_id)
    combined_dict = {"id": bookmark_id} | bookmark.model_dump()
    bookmarks[bookmark_id] = combined_dict
    save_bookmarks()
    return bookmarks[bookmark_id]


@app.patch("/bookmarks/{bookmark_id}", response_model=BookmarkOut)
def patch_by_id(bookmark_id: int, bookmark: BookmarkPatch):
    raise_exception(bookmark_id)
    existing_bookmark = bookmarks[bookmark_id]
    updated_data = bookmark.model_dump(exclude_unset=True)
    combined_dict = existing_bookmark | updated_data
    bookmarks[bookmark_id] = combined_dict
    save_bookmarks()
    return bookmarks[bookmark_id]


@app.delete("/bookmarks/{bookmark_id}")
def delete_by_id(bookmark_id: int):
    raise_exception(bookmark_id)
    del bookmarks[bookmark_id]
    save_bookmarks()
    return {"message": "Bookmark deleted successfully"}


def save_bookmarks():
    data = {"next_id": next_id, "bookmarks": bookmarks}
    with open("bookmarks.json", "w") as f:
        json.dump(data, f)


def load_bookmarks():
    global next_id
    global bookmarks
    try:
        with open("bookmarks.json", "r") as f:
            data = json.load(f)
        next_id = data["next_id"]
        bookmarks = {int(key): value for key, value in data["bookmarks"].items()}
    except FileNotFoundError:
        pass


def raise_exception(bookmark_id: int):
    if bookmark_id not in bookmarks:
        raise HTTPException(status_code=404, detail="Bookmark not found")


load_bookmarks()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
