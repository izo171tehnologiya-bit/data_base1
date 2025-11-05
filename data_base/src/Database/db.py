import sqlite3
from sqlite3 import Connection

def get_connection(db_name: str = "library.db") -> Connection:
    return sqlite3.connect(db_name)


def create_tables(db_name: str = "library.db"):
    """
    Создает таблицы Authors и Books, если их еще нет.
    """
    conn = get_connection(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            Item_ID INTEGER,
            Name TEXT NOT NULL,
            Need_approve BOOL,
            Size INTEGER,
            Item_type TEXT NOT NULL,
            Shelve_placement INTEGER
            FOREIGN KEY (Shelve_placement) REFERENCES Shelve(Shelve_ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shelves (
            Shelve_ID INTEGER PRIMARY KEY,
            Capacity INTEGER,
            Cabinet_ID INTEGER,
            Type_of_item TEXT NOT NULL
            FOREIGN KEY (Cabinet_ID) REFERENCES Cabinet(Shelves_ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cabinet (
            Shelves_ID INTEGER PRIMARY KEY,
            Type_of_item TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def insert_sample_data(db_name: str = "library.db"):
    """
    Вставляет тестовые записи в таблицы Authors и Books,
    если они еще не добавлены
    """
    conn = get_connection(db_name)
    cursor = conn.cursor()

    # Проверка, есть ли авторы
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        items = [
            (1, "Капли для глаз", True, 5, "Не антибиотики"),
            (2, "Жаропонижающее", False, 3, "Не антибиотики"),
            (3, "Противовирусное", True, 7, "Антибиотики"),
            (4, "Витамины", False, 4, "Не антибиотики")
        ]
        cursor.executemany("INSERT INTO items (Item_ID, Name, Need_approve, Size, Item_type) VALUES (?, ?, ?, ?, ?)", items)
        print("Добавлены товары.")

    # Проверка, есть ли книги
    cursor.execute("SELECT COUNT(*) FROM Shelves")
    if cursor.fetchone()[0] == 0:
        shelve = [
            (10, 10, "Не антибиотики"),
            (20, 7, "Не антибиотики"),
            (30, 6, "Антибиотики"),
            (40, 10, "Не антибиотики"),
            (50, 15, "Антибиотики")
        ]
        cursor.executemany("INSERT INTO Shelves (Shelve_ID, Capacity, Type_of_item) VALUES (?, ?, ?)", shelve)
        print("Добавлены полки.")

    conn.commit()
    conn.close()