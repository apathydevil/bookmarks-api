# bookmarks-api

A small REST API for storing bookmarks, built with FastAPI and SQLite, with a
full pytest suite covering every endpoint.

## Stack

- **FastAPI** + **Pydantic** — routing and request/response validation, with
  separate input, output (`response_model`), and partial-update models
- **SQLite** via Python's built-in `sqlite3` — hand-written, parameterized SQL
  (no ORM); `bookmarks.db` is created automatically on first run
- **pytest** + FastAPI's `TestClient` — tests run against a separate
  `test_bookmarks.db`, so they never touch real data
- **uv** — dependency management

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

## Test

```bash
uv run pytest
```

The suite covers:

- the happy path of every endpoint (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`)
- `PATCH` only changing the fields that were sent, leaving the rest intact
- `DELETE` actually removing the record (a follow-up `GET` returns `404`)
- `404` responses for every id-based route when the bookmark doesn't exist
- `422` validation errors when required fields are missing

## Endpoints

| Method | Path               | Description                       |
|--------|--------------------|-----------------------------------|
| GET    | `/bookmarks`       | List all bookmarks                |
| POST   | `/bookmarks`       | Create a bookmark                 |
| GET    | `/bookmarks/{id}`  | Get a bookmark by id              |
| PUT    | `/bookmarks/{id}`  | Replace a bookmark by id          |
| PATCH  | `/bookmarks/{id}`  | Partially update a bookmark by id |
| DELETE | `/bookmarks/{id}`  | Delete a bookmark by id           |

A bookmark has a `title` (required), `url` (required), and `description`
(optional).

`PUT` requires the full object (`title` and `url` must both be sent). `PATCH`
only requires the field(s) you want to change — anything left out keeps its
current value.

### Example requests

```json
POST /bookmarks
Content-Type: application/json

{
  "title": "FastAPI docs",
  "url": "https://fastapi.tiangolo.com",
  "description": "Official documentation"
}
```

```json
PATCH /bookmarks/1
Content-Type: application/json

{
  "description": "Updated description only"
}
```
