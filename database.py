import sqlite3

dbpath = "bookmarks.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(dbpath)
    connection.row_factory = sqlite3.Row
    return connection


def get_cursor() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = get_connection()
    cursor = connection.cursor()
    return connection, cursor


def init_db() -> None:
    connection, cursor = get_cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookmarks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, url TEXT NOT NULL, description TEXT)
    """)
    connection.commit()
    connection.close()


def create_bookmark(title: str, url: str, description: str | None) -> int | None:
    connection, cursor = get_cursor()
    cursor.execute(
        """
    INSERT INTO bookmarks (title, url, description) VALUES (?, ?, ?)
    """,
        (title, url, description),
    )
    connection.commit()
    lastrowid = cursor.lastrowid
    connection.close()
    return lastrowid


def get_all_bookmarks() -> list:
    connection, cursor = get_cursor()
    cursor.execute("""
    SELECT * FROM bookmarks
    """)
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]


def get_bookmark(bookmark_id: int) -> dict | None:
    connection, cursor = get_cursor()
    cursor.execute(
        """
    SELECT * FROM bookmarks WHERE id = ?
    """,
        (bookmark_id,),
    )
    rows = cursor.fetchone()
    connection.close()
    if rows is None:
        return None
    return dict(rows)


def delete_bookmark(bookmark_id: int) -> None:
    connection, cursor = get_cursor()
    cursor.execute(
        """
    DELETE FROM bookmarks WHERE id = ?
    """,
        (bookmark_id,),
    )
    connection.commit()
    connection.close()


def update_bookmark(bookmark_id: int, title: str, url: str, description: str | None):
    connection, cursor = get_cursor()
    cursor.execute(
        """
    UPDATE bookmarks SET title = ?, url = ?, description = ? WHERE id = ?

    """,
        (
            title,
            url,
            description,
            bookmark_id,
        ),
    )
    connection.commit()
    connection.close()
