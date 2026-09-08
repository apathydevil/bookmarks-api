from pydantic import BaseModel


class Bookmark(BaseModel):
    title: str
    description: str | None = None
