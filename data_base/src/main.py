from data_base.src.Database.db import get_connection,create_tables, insert_sample_data
from data_base.src.repository.repository import Repository
import os

DB_FILE = "library.db"


def main():
    # Если базы нет, создаем таблицы и вставляем тестовые данные
    if not os.path.exists(DB_FILE):
        create_tables(DB_FILE)
        insert_sample_data(DB_FILE)

    repo = Repository(DB_FILE)
    user_flag = False
    # Для отладки флаг  для  авторизации сделан True
    aut_flag = True

    # --- Основной цикл программы ---
    while True:
        if not aut_flag:
            users = repo.authorisation()
            inp_login = input("Введите логин: ")
            inp_password = input("Введите пароль: ")
            for user in users:
                if (user.name == inp_login) and (user.password == inp_password):
                    user_flag = user.is_seller
                    aut_flag = True
        if aut_flag:

            print("\nВыберите действие:")
            print("1 - Показать все товары")
            print("2 - Узнать необходимость рецепта")
            print("3 - Проверить наличие товара в магазине")
            print("0 - Выход")
            choice = input("Ваш выбор: ")

            if choice == "1":
                items = repo.get_all_items()
                print("\nСписок всех товаров:")
                for item in items:
                    print(f"{item.it_id}: {item.name} ")

            elif choice == "2":
                inp_name = input("Введите название товара:  ")
                items = repo.get_all_items()
                for item in items:
                    if item.name == inp_name:
                        if item.need_approve == 1:
                            print("Необходим рецепт от врача")
                            break
                else: print("Рецепт не требуется")

            elif choice == "3":
                inp_name = input("Введите название товара:  ")
                items = repo.get_all_items()
                for item in items:
                    if item.name == inp_name:
                        print("Товар есть в магазине")
                        break
                else: print("Товара нет")

            elif choice == "0":
                print("Выход из программы...")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")


        else:
            print("Такого пользователя нет в системе")
            break
    repo.close()

if __name__ == "__main__":
    main()
