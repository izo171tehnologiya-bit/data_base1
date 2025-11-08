import sqlite3

from data_base.src.models.models import item, Shelve, User


class Repository:
    def __init__(self, db_file: str = "library.db"):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
        self.cursor = self.conn.cursor()

    def authorisation(self):
        self.cursor.execute("SELECT Name, Password, IS_SELLER FROM Users")
        rows = self.cursor.fetchall()
        return [User(name=row["Name"], password=row["Password"], is_seller=row["IS_SELLER"]) for row in rows]

    def check_recipe(self):
        inp_name = input("Введите название товара:  ")
        self.cursor.execute("SELECT Need_approve FROM items WHERE Name = ?", (inp_name,))
        rows = self.cursor.fetchall()
        return [item(it_id=row["Item_ID"], name=row["Name"], need_approve=row["Need_approve"], size=row["Size"], item_type=row["Item_type"]) for row in rows]

    def get_all_items(self):
            self.cursor.execute("SELECT Item_ID, Name, Need_approve, Size, Item_type FROM items")
            rows = self.cursor.fetchall()
            return [item(it_id=row["Item_ID"], name=row["Name"], need_approve=row["Need_approve"], size=row["Size"], item_type=row["Item_type"]) for row in rows]

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
