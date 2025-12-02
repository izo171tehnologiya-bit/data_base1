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
        CREATE TABLE IF NOT EXISTS Users (
            Name TEXT NOT NULL,
            Password TEXT NOT NULL,
            IS_SELLER INTEGER
            )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            Item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Need_approve BOOL,
            Size INTEGER,
            Item_type TEXT NOT NULL,
            Shelve_placement INTEGER,
            FOREIGN KEY (Shelve_placement) REFERENCES Shelves(Shelve_ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Shelves (
            Shelve_ID INTEGER PRIMARY KEY,
            Capacity INTEGER,
            Cabinet_ID INTEGER,
            Type_of_item TEXT NOT NULL,
            FOREIGN KEY (Cabinet_ID) REFERENCES Cabinets(Shelves_ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cabinets (
            Shelves_ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
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
            ("Капли для глаз", True, 5, "Не антибиотики", 10),
            ("Жаропонижающее", False, 3, "Не антибиотики", 10),
            ("Противовирусное", True, 7, "Антибиотики", 50),
            ("Витамины", False, 4, "Не антибиотики", 40)
        ]
        cursor.executemany("INSERT INTO items (Name, Need_approve, Size, Item_type, Shelve_placement) VALUES (?, ?, ?, ?, ?)", items)
        print("Добавлены товары.")

    # Проверка, есть ли книги
    cursor.execute("SELECT COUNT(*) FROM Shelves")
    if cursor.fetchone()[0] == 0:
        shelve = [
            (10, 10, 200, "Не антибиотики"),
            (20, 7, 200, "Не антибиотики"),
            (30, 6, 100, "Антибиотики"),
            (40, 10, 200, "Не антибиотики"),
            (50, 15, 100, "Антибиотики")
        ]
        cursor.executemany("INSERT INTO Shelves (Shelve_ID, Capacity, Cabinet_ID ,Type_of_item) VALUES (?, ?, ?, ?)", shelve)
        print("Добавлены полки.")

    # Проверка, есть ли шкафы
    cursor.execute("SELECT COUNT(*) FROM Cabinets")
    if cursor.fetchone()[0] == 0:
        cabinets = [
            (100, "Шкаф для антибиотиков", "Не антибиотики"),
            (200, "Шкаф для не антибиотиков", "Не антибиотики"),
        ]
        cursor.executemany("INSERT INTO Cabinets (Shelves_ID, Name, Type_of_item) VALUES (?, ?, ?)", cabinets)
        print("Добавлены шкафы.")

    # Проверка, есть ли шкафы
    cursor.execute("SELECT COUNT(*) FROM Users")
    if cursor.fetchone()[0] == 0:
        users = [
            ("User1", "1234", 0),
            ("User2", "123456", 0),
            ("Seller1", "qwert", 1),
            ("Seller2", "qwerty", 1),
        ]
        cursor.executemany("INSERT INTO Users (Name, Password, IS_SELLER) VALUES (?, ?, ?)", users)
        print("Добавлены пользователи.")
    conn.commit()
    conn.close()