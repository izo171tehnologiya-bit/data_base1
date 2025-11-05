import sqlite3

from data_base.src.models.models import item, Shelve


class Repository:
    def __init__(self, db_file: str = "library.db"):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
        self.cursor = self.conn.cursor()

    def get_all_books(self):
        self.cursor.execute("SELECT ID, Title, Author_ID FROM Books")
        rows = self.cursor.fetchall()
        return [Book(id=row["ID"], title=row["Title"], author_id=row["Author_ID"]) for row in rows]

    def get_author(self, author_id: int):
        self.cursor.execute("SELECT ID, Name FROM Authors WHERE ID = ?", (author_id,))
        row = self.cursor.fetchone()
        if row:
            return Author(id=row["ID"], name=row["Name"])
        return None

    def authors_with_more_than_n_books(self, n: int):
        query = """
            SELECT Authors.ID, Authors.Name
            FROM Authors
            JOIN Books ON Authors.ID = Books.Author_ID
            GROUP BY Authors.ID
            HAVING COUNT(Books.ID) > ?
        """
        self.cursor.execute(query, (n,))
        rows = self.cursor.fetchall()
        return [Author(id=row["ID"], name=row["Name"]) for row in rows]

    def close(self):
        self.conn.close()
