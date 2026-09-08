import json

import uvicorn
from fastapi import FastAPI, HTTPException

from models import Bookmark

app = FastAPI()

notes: dict[int, dict] = {}
next_id = 1


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/notes")
def create_bookmark(bookmark: Bookmark):
    global next_id
    combined_dict = {"id": next_id} | bookmark.model_dump()
    notes[next_id] = combined_dict
    new_id = next_id
    next_id = next_id + 1
    save_notes()
    return notes[new_id]


@app.get("/notes")
def get_bookmarks():
    return list(notes.values())


@app.get("/notes/{note_id}")
def get_by_id(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    return notes[note_id]


@app.put("/notes/{note_id}")
def update_by_id(note_id: int, bookmark: Bookmark):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    combined_dict = {"id": note_id} | bookmark.model_dump()
    notes[note_id] = combined_dict
    save_notes()
    return notes[note_id]


@app.delete("/notes/{note_id}")
def delete_by_id(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    del notes[note_id]
    save_notes()
    return {"message": "Note deleted successfully"}


def save_notes():
    data = {"next_id": next_id, "notes": notes}
    with open("notes.json", "w") as f:
        json.dump(data, f)


def load_notes():
    global next_id
    global notes
    try:
        with open("notes.json", "r") as f:
            data = json.load(f)
        next_id = data["next_id"]
        notes = {int(key): value for key, value in data["notes"].items()}
    except FileNotFoundError:
        pass


load_notes()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
