import sqlite3
import json
import csv
import yaml
import xml.etree.ElementTree as ET
from xml.dom import minidom


class Out_functions:
    def __init__(self, db_file: str = "library.db"):
        self.conn = sqlite3.connect(db_file) # Соединение с базой данных
        self.conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по имени
        self.cursor = self.conn.cursor() #Создание cursor для выполнения SQL запросов

    def extractjson(self):
        # Извлечение данных из SQLite
        self.cursor.execute("SELECT * FROM items")
        rows = self.cursor.fetchall()

        # Преобразование данных в список словарей
        data = []
        for row in rows:
            data.append(dict(zip([column[0] for column in self.cursor.description], row)))

        # Преобразование данных в формат JSON
        json_data = json.dumps(data, indent=4, ensure_ascii=False) # indent=4 - форматирование с отступами, ensure_ascii=False - поддержка русских букв

        # Сохранение JSON в файл
        with open('out/data.json', 'w', encoding='utf-8') as f:
            f.write(json_data)
        print("Json файл добавлен")




    def extractcsv(self):
        self.cursor.execute("SELECT * FROM items")
        data = self.cursor.fetchall()
        # Открытие файла для записи в CSV
        with open('out/data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([i[0] for i in self.cursor.description])  # Написать заголовок
            writer.writerows(data)  # Запись всех строк данных
        print("Csv файл добавлен")


    def extractxml(self):
        self.cursor.execute("SELECT * FROM items")
        rows = self.cursor.fetchall()

        # Создание корневого элемента
        root = ET.Element("items")

        # Создание XML-структуры из данных
        for row in rows:
            # Cоздание элемента
            item_element = ET.SubElement(root, "Item")
            #  Создание подэлементов
            user_id = ET.SubElement(item_element, "id")
            user_id.text = str(row[0])
            user_name = ET.SubElement(item_element, "name")
            user_name.text = row[1]
            user_aprove = ET.SubElement(item_element, "Need_approve")
            user_aprove.text = str(row[2])
            user_size = ET.SubElement(item_element, "Size")
            user_size.text = str(row[3])
            user_type = ET.SubElement(item_element, "Item_type")
            user_type.text = row[4]
            user_place = ET.SubElement(item_element, "Shelve_placement")
            user_place.text = str(row[5])
            user_price = ET.SubElement(item_element, "Price")
            user_price.text = str(row[6])

        #  Запись в XML-файл
        tree = ET.ElementTree(root)
        # Преобразование XML-дерева в строку
        xml_str = ET.tostring(root, encoding='utf-8', xml_declaration=True)
        # Форматирование XML для вывода с отступами
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="   ")
        # Сохранение в XML файл
        with open('out/data.xml', "w", encoding='utf-8') as f:
            f.write(pretty_xml)
        print("Xml файл добавлен")

    def extractyaml(self):
        self.cursor.execute("SELECT * FROM items")
        data_from_db = self.cursor.fetchall()
        # Извлечение имен колонок для использования в качестве ключей словаря
        keys = [description[0] for description in self.cursor.description]
        # Преобразование каждой строки в словарь
        data_for_yaml = [dict(zip(keys, row)) for row in data_from_db]
        # Запись данных в YAML файл
        with open('out/data.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(data_for_yaml, file, allow_unicode=True)
            self.conn.close()
        print("Yaml файл добавлен")

    def close(self):
        self.conn.close()