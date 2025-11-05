from data_base.src.Database.db import create_tables, insert_sample_data
from data_base.src.repository.repository import Repository
import os

DB_FILE = "../../../../data_base1/data_base/src/library.db"


def main():
    # Если базы нет, создаем таблицы и вставляем тестовые данные
    if not os.path.exists(DB_FILE):
        create_tables(DB_FILE)
        insert_sample_data(DB_FILE)

    repo = Repository(DB_FILE)

    # --- Основной цикл программы ---
    while True:
        print("\nВыберите действие:")
        print("1 - Показать все книги")
        print("2 - Показать авторов с более чем 2 книгами")
        print("0 - Выход")
        choice = input("Ваш выбор: ")

        if choice == "1":
            books = repo.get_all_books()
            print("\nСписок всех книг:")
            for book in books:
                author = repo.get_author(book.author_id)
                print(f"{book.id}: {book.title} (Автор: {author.name})")

        elif choice == "2":
            authors = repo.authors_with_more_than_n_books(2)
            print("\nАвторы с более чем 2 книгами:")
            if authors:
                for author in authors:
                    print(f"{author.id}: {author.name}")
            else:
                print("Таких авторов нет.")

        elif choice == "0":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    repo.close()

if __name__ == "__main__":
    main()
