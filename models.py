from pydantic import BaseModel


class Bookmark(BaseModel):
    title: str
    url: str
    description: str | None = None


class BookmarkOut(Bookmark):
    id: int


class BookmarkPatch(BaseModel):
    title: str | None = None
    url: str | None = None
    description: str | None = None
