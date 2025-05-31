from hash_table import HashTable



def print_menu():
    """Вывод меню"""
    print("\nМЕНЮ:")
    print("1. Показать хеш-таблицу")
    print("2. Добавить произведение")
    print("3. Найти произведение")
    print("4. Обновить произведение")
    print("5. Удалить произведение")
    print("0. Выход")

def main():
    ht = HashTable()
    
    while True:
        print_menu()
        choice = input("Выберите действие: ")
        
        try:
            if choice == "1":
                ht.display()
            
            elif choice == "2":
                key = input("Введите ключ (название слитно, например 'АннаКаренина'): ").strip()
                value = input("Введите значение (автор и название, например 'Л. Толстой - Анна Каренина'): ").strip()
                if not key or not value:
                    print("Ошибка: ключ и значение не могут быть пустыми")
                    continue
                
                if ht.insert(key, value):
                    print("Произведение успешно добавлено!")
                else:
                    print("Произведение с таким ключом уже существует и было обновлено!")
            
            elif choice == "3":
                key = input("Введите ключ для поиска: ").strip()
                if not key:
                    print("Ошибка: ключ не может быть пустым")
                    continue
                
                result = ht.get(key)
                if result is not None:
                    print(f"Найдено: {result}")
                else:
                    print("Произведение с таким ключом не найдено.")
            
            elif choice == "4":
                key = input("Введите ключ для обновления: ").strip()
                new_value = input("Введите новое значение: ").strip()
                if not key or not new_value:
                    print("Ошибка: ключ и значение не могут быть пустыми")
                    continue
                
                if ht.update(key, new_value):
                    print("Произведение успешно обновлено!")
                else:
                    print("Произведение с таким ключом не найдено.")
            
            elif choice == "5":
                key = input("Введите ключ для удаления: ").strip()
                if not key:
                    print("Ошибка: ключ не может быть пустым")
                    continue
                
                if ht.delete(key):
                    print("Произведение успешно удалено!")
                else:
                    print("Произведение с таким ключом не найдено.")
            
            elif choice == "0":
                print("Выход из программы.")
                break
            
            else:
                print("Неверный ввод. Пожалуйста, выберите пункт меню от 0 до 5.")
        
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()