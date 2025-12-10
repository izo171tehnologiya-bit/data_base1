from data_base.src.Database.db import create_tables, insert_sample_data
from data_base.src.repository.repository import Repository, new_item, del_item
from data_base.src.out.Out_functions import Out_functions
import os

DB_FILE = "library.db"
OUT_DICT = "out"

# Пользователь Логин User1 Пароль 1234
# Продавец Логин Seller1 Пароль qwert

def main():
    # Если базы нет, создаются таблицы и вставляются тестовые данные
    if not os.path.exists(DB_FILE):
        create_tables(DB_FILE)
        insert_sample_data(DB_FILE)
    if not os.path.exists(OUT_DICT):
        os.makedirs(OUT_DICT)

    repo = Repository(DB_FILE)
    out = Out_functions(DB_FILE)
    seller_flag = True
    aut_flag = True

    # --- Основной цикл программы ---
    while True:
        if not aut_flag:
            users = repo.authorisation()
            inp_login = input("Введите логин: ")
            inp_password = input("Введите пароль: ")
            for user in users:
                if (user.name == inp_login) and (user.password == inp_password):
                    seller_flag = user.is_seller
                    aut_flag = True
        if aut_flag:
            print("\nВыберите действие:")
            print("1 - Показать все товары")
            print("2 - Узнать необходимость рецепта")
            print("3 - Проверить наличие товара в магазине")
            if seller_flag:
                print("4 - Добавить новый товар")
            if seller_flag:
                print("5 - Вывести(обновить) данные в виде разных таблиц")
            if seller_flag:
                print("6 - Удалить товар")
            print("0 - Выход")
            choice = input("Ваш выбор: ")

            if choice == "1":
                items = repo.get_all_items()
                print("\nСписок всех товаров:")
                for item in items:
                    print(f"{item.it_id}: {item.name} {item.price} руб")

            elif choice == "2":
                while True:
                    inp_name = input("Введите название товара:  ")
                    if inp_name.isalpha():
                        break
                    else:
                        print("Неверно. Попробуйте ещё раз")
                items = repo.get_all_items()
                for item in items:
                    if item.name == inp_name:
                        if item.need_approve == 1:
                            print("Необходим рецепт от врача.")
                            break
                    print("Рецепт не требуется.")
                    break

            elif choice == "3":
                while True:
                    inp_name = input("Введите название товара:  ")
                    if inp_name.isalpha():
                        break
                    else:
                        print("Неверно, попробуйте ещё раз")
                items = repo.get_all_items()
                for item in items:
                    if item.name == inp_name:
                        if seller_flag == True:
                            print(f"Товар есть в магазине. Он расположен на {item.shelve_placement} полке")
                        break
                    print("Товар есть в магазине.")
                else:
                    print("Товара нет")


            elif choice == "4":
                    new_item()

            elif choice == "5":
                out.extractjson()
                out.extractcsv()
                out.extractxml()
                out.extractyaml()

            elif choice == "6":
                del_item()

            elif choice == "0":
                print("Выход из программы...")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")


        else:
            print("Такого пользователя нет в системе")
            break
    out.close()

if __name__ == "__main__":
    main()
