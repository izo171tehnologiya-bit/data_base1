import sqlite3
import json
import csv
import yaml
import xml.etree.ElementTree as ET
from data_base.src.Database.db import get_connection
from data_base.src.models.models import item, Shelve, User


def new_item():
    conn = get_connection("library.db")
    cursor = conn.cursor()
    in_itId = input("Введите ID:")
    in_itname = input("Введите название:")
    in_itaprov = input("Введите необходимость рецепта:")
    in_itsize = input("Введите объём:")
    in_ittype = input("Введите тип товара:")
    try:
        cursor.execute(f"SELECT Shelve_ID, Cabinet_ID FROM Shelves WHERE Capacity > ? AND Type_of_item = ?", (in_itsize, in_ittype))
        rows = cursor.fetchone()

        new_items = [
            (in_itId, in_itname, in_itaprov, in_itsize, in_ittype, rows[0])
        ]
        cursor.executemany("INSERT INTO items (Item_ID, Name, Need_approve, Size, Item_type, Shelve_placement) VALUES (?, ?, ?, ?, ?, ?)", new_items)
        print(f"Товар добавлен. Поместите его на {rows[1]} шкаф {rows[0]} полку")
    except:
        print("Свободных полок нет")
    conn.commit()
    conn.close()
    return None


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

    def extractjson(self):


        # Извлечение данных из SQLite
        self.cursor.execute("SELECT * FROM items")
        rows = self.cursor.fetchall()

        # Преобразование данных в список словарей
        data = []
        for row in rows:
            data.append(dict(zip([column[0] for column in self.cursor.description], row)))

        # Преобразовать данные в формат JSON с указанной кодировкой
        json_data = json.dumps(data, indent=4, ensure_ascii=False)

        # Сохраните JSON в файл с указанной кодировкой
        with open('out/data.json', 'w', encoding='utf-8') as f:
            f.write(json_data)

        # Закройте соединение


    def extractcsv(self):
        self.cursor.execute("SELECT * FROM items")
        data = self.cursor.fetchall()
        with open('out/data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([i[0] for i in self.cursor.description])  # Write header
            writer.writerows(data)  # Write data rows


    def extractxml(self):
        self.cursor.execute("SELECT * FROM items")
        rows = self.cursor.fetchall()

        # 2. Создание корневого элемента
        root = ET.Element("items")

        # 3. Создание XML-структуры из данных
        for row in rows:
            user_element = ET.SubElement(root, "Item")
            user_id = ET.SubElement(user_element, "id")
            user_id.text = str(row[0])
            user_name = ET.SubElement(user_element, "name")
            user_name.text = row[1]
            user_aprove = ET.SubElement(user_element, "Need_approve")
            user_aprove.text = str(row[2])
            user_size = ET.SubElement(user_element, "Size")
            user_size.text = str(row[3])
            user_type = ET.SubElement(user_element, "Item_type")
            user_type.text = row[4]
            user_place = ET.SubElement(user_element, "Shelve_placement")
            user_place.text = str(row[5])

        # 4. Запись в XML-файл
        tree = ET.ElementTree(root)
        tree.write('out/data.xml', encoding='utf-8', xml_declaration=True)

    def extractyaml(self):
        self.cursor.execute("SELECT * FROM items")
        data_from_db = self.cursor.fetchall()
        keys = [description[0] for description in self.cursor.description]
        data_for_yaml = [dict(zip(keys, row)) for row in data_from_db]
        with open('out/data.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(data_for_yaml, file, allow_unicode=True)
            self.conn.close()

    def close(self):
        self.conn.close()
