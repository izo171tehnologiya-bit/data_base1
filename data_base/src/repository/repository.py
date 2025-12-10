import sqlite3
from data_base.src.Database.db import get_connection
from data_base.src.models.models import item, User


def new_item():
    conn = get_connection("library.db")
    cursor = conn.cursor()

    while True:
        in_itname = input("Введите название:")
        if in_itname.isalpha():
            break
        else:
            print("Неверно, попробуйте ещё раз")

    while True:
        in_itaprov = input("Введите необходимость рецепта:")
        if in_itaprov == "True" or in_itaprov == "False":
            break
        else:
            print("Неверно, попробуйте ещё раз")

    while True:
        in_itsize = input("Введите объём:")
        if in_itsize.isdigit():
            break
        else:
            print("Неверно, попробуйте ещё раз")

    while True:
        in_ittype = input("Введите тип товара:")
        if in_ittype == "Антибиотики" or in_ittype == "Не антибиотики":
            break
        else:
            print("Неверно, попробуйте ещё раз")

    while True:
        in_itprice = input("Введите цену товара:")
        if in_itprice.isdigit():
            break
        else:
            print("Неверно, попробуйте ещё раз")

    try:
        cursor.execute(f"SELECT Shelve_ID, Cabinet_ID FROM Shelves WHERE Capacity > ? AND Type_of_item = ?", (in_itsize, in_ittype))
        rows = cursor.fetchone()

        new_items = [
            (in_itname, in_itaprov, in_itsize, in_ittype, rows[0], in_itprice)
        ]
        cursor.executemany("INSERT INTO items (Name, Need_approve, Size, Item_type, Shelve_placement, Price) VALUES (?, ?, ?, ?, ?, ?)", new_items)
        print(f"Товар добавлен. Поместите его на {rows[1]} шкаф {rows[0]} полку")
        cursor.execute(f"UPDATE Shelves SET Capacity = Capacity - ? WHERE Shelve_ID = ?",  (in_itsize, rows[0]))
    except:
        print("Свободных полок нет")
    conn.commit()
    conn.close()
    return None


def del_item():
    conn = get_connection("library.db")
    cursor = conn.cursor()

    while True:
        in_itname = input("Введите название:")
        if in_itname.isalpha():
            break
        else:
            print("Неверно, попробуйте ещё раз")

    cursor.execute("SELECT Item_ID, Size, Shelve_placement FROM items WHERE Name = ?", (in_itname,))
    rows = cursor.fetchone()
    cursor.executemany("DELETE FROM items WHERE Item_ID = ?", str(rows[0]))
    print("Товар удалён.")
    cursor.execute(f"UPDATE Shelves SET Capacity = Capacity + ? WHERE Shelve_ID = ?",  (rows[1], rows[2]))
    conn.commit()
    conn.close()
    return None

class Repository:
    def __init__(self, db_file: str = "library.db"):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def authorisation(self):
        self.cursor.execute("SELECT Name, Password, IS_SELLER FROM Users")
        rows = self.cursor.fetchall()
        return [User(name=row["Name"], password=row["Password"], is_seller=row["IS_SELLER"]) for row in rows]

    def check_recipe(self):
        while True:
            inp_name = input("Введите название товара:  ")
            if inp_name.isalpha():
                break
            else:
                print("Неверно, попробуйте ещё раз")
        self.cursor.execute("SELECT Need_approve FROM items WHERE Name = ?", (inp_name,))
        rows = self.cursor.fetchall()
        return [item(it_id=row["Item_ID"], name=row["Name"], need_approve=row["Need_approve"], size=row["Size"], item_type=row["Item_type"], shelve_placement=row["Shelve_placement"], price=row["Price"]) for row in rows]

    def get_all_items(self):
            self.cursor.execute("SELECT Item_ID, Name, Need_approve, Size, Item_type, Shelve_placement, Price FROM items")
            rows = self.cursor.fetchall()
            return [item(it_id=row["Item_ID"], name=row["Name"], need_approve=row["Need_approve"], size=row["Size"], item_type=row["Item_type"], shelve_placement=row["Shelve_placement"], price=row["Price"]) for row in rows]


