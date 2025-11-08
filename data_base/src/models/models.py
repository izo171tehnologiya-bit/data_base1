# models/models.py

class item:
    """
    Модель для таблицы Authors
    Поля:
    - id: уникальный идентификатор автора (PK)
    - name: имя автора
    """
    def __init__(self, it_id, name, need_approve, size, item_type):
        self.it_id = it_id
        self.name = name
        self.need_approve = need_approve
        self.size = size
        self.item_type = item_type

class Shelve:
    """
    Модель для таблицы Books
    Поля:
    - id: уникальный идентификатор книги (PK)
    - title: название книги
    - author_id: идентификатор автора (FK -> Authors.id)
    """
    def __init__(self, sh_id, capacity, cab_id, item_type):
        self.sh_id = sh_id
        self.capacity = capacity
        self.cab_id = cab_id
        self.item_type = item_type

class User:
    """
    Модель для таблицы Books
    Поля:
    - id: уникальный идентификатор книги (PK)
    - title: название книги
    - author_id: идентификатор автора (FK -> Authors.id)
    """
    def __init__(self, name, password, is_seller):
        self.name = name
        self.password = password
        self.is_seller = is_seller

