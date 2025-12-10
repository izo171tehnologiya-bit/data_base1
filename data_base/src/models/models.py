# models/models.py

class item:
    """
    Модель для таблицы Items
    Поля:
    - id: уникальный идентификатор товара
    - name: название товара
    - need_approve: необходимость рецепта от врача
    - size: размер товара
    - item_type: тип товара
    - shelve_placement: расположение товара на полке
    """
    def __init__(self, it_id, name, need_approve, size, item_type, shelve_placement, price):
        self.it_id = it_id
        self.name = name
        self.need_approve = need_approve
        self.size = size
        self.item_type = item_type
        self.shelve_placement = shelve_placement
        self.price = price

class Shelve:
    """
    Модель для таблицы Shelves
    Поля:
    - id: уникальный идентификатор полки
    - capacity: вместимость полки
    - cab_id: в каком шкафу находится полка
    - item_type: какой тип товара содержит полка
    """
    def __init__(self, sh_id, capacity, cab_id, item_type):
        self.sh_id = sh_id
        self.capacity = capacity
        self.cab_id = cab_id
        self.item_type = item_type

class User:
    """
    Модель для таблицы Users
    Поля:
    - name: логин пользователя
    - password: пароль пользователя
    - is_seller: является ли пользователь продавцом
    """
    def __init__(self, name, password, is_seller):
        self.name = name
        self.password = password
        self.is_seller = is_seller

