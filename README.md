# bookmarks-api

A small FastAPI CRUD service for storing bookmarks, built as a `uv` learning project.

## Stack

- FastAPI + Pydantic for the API and request/response validation
- In-memory storage, persisted to `bookmarks.json` on every change (no database)
- `uv` for dependency management

## Setup

```bash
uv sync
```

## Run

```bash
uv run main.py
```

Server starts at `http://127.0.0.1:8000`. Interactive docs (Swagger UI) at
`http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Path               | Description              |
|--------|--------------------|--------------------------|
| GET    | `/bookmarks`       | List all bookmarks       |
| POST   | `/bookmarks`       | Create a bookmark        |
| GET    | `/bookmarks/{id}`  | Get a bookmark by id     |
| PUT    | `/bookmarks/{id}`  | Update a bookmark by id  |
| DELETE | `/bookmarks/{id}`  | Delete a bookmark by id  |

A bookmark has a `title` (required), `url` (required), and `description`
(optional).

### Example request

```json
POST /bookmarks
Content-Type: application/json

{
  "title": "FastAPI docs",
  "url": "https://fastapi.tiangolo.com",
  "description": "Official documentation"
}
```
