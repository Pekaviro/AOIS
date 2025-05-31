# Исправленные юнит-тесты
import unittest
from unittest.mock import patch
from io import StringIO

from hash_table import HashTable

class TestHashTable(unittest.TestCase):
    def setUp(self):
        # Создаем хеш-таблицу без инициализации тестовых данных
        self.ht = HashTable(size=4, initialize_test_data=False)
        # Добавляем только необходимые для тестов данные
        self.sample_data = [
            ("АннаКаренина", "Л. Толстой - Анна Каренина"),
            ("БратьяКарамазовы", "Ф. Достоевский - Братья Карамазовы")
        ]
        for key, value in self.sample_data:
            self.ht.insert(key, value)

    def test_initialization(self):
        self.assertEqual(self.ht.size, 4)
        self.assertEqual(self.ht.count, 2)

    def test_char_to_num(self):
        self.assertEqual(self.ht._char_to_num('А'), 0)
        self.assertEqual(self.ht._char_to_num('а'), 0)
        self.assertEqual(self.ht._char_to_num('Ё'), 6)  # Буква Ё
        self.assertEqual(self.ht._char_to_num('ё'), 6)  # Строчная ё
        self.assertEqual(self.ht._char_to_num('Е'), 5)  # Буква Е (не Ё)
        self.assertEqual(self.ht._char_to_num('е'), 5)   # Строчная е
        self.assertEqual(self.ht._char_to_num('Я'), 30)
        self.assertEqual(self.ht._char_to_num('Z'), -1)

    def test_hash_function_valid(self):
        hash1 = self.ht._hash_function("АннаКаренина")
        hash2 = self.ht._hash_function("АннаКаренина")
        self.assertEqual(hash1, hash2)

    def test_hash_function_invalid(self):
        with self.assertRaises(ValueError):
            self.ht._hash_function("A")  # Слишком короткий ключ

        with self.assertRaises(ValueError):
            self.ht._hash_function(123)  # Не строка

    def test_insert_and_get(self):
        self.ht.insert("ВишневыйСад", "А. Чехов - Вишневый сад")
        self.assertEqual(self.ht.get("ВишневыйСад"), "А. Чехов - Вишневый сад")
        self.assertEqual(self.ht.count, 3)

        # Обновление существующего элемента
        self.ht.insert("АннаКаренина", "Обновленное значение")
        self.assertEqual(self.ht.get("АннаКаренина"), "Обновленное значение")
        self.assertEqual(self.ht.count, 3)

    def test_collision_handling(self):
        # Добавляем элемент с коллизией
        self.ht.insert("АннаСнегина", "С. Есенин - Анна Снегина")
        # Проверяем, что элемент вставлен с учетом коллизии
        self.assertEqual(self.ht.get("АннаСнегина"), "С. Есенин - Анна Снегина")

    def test_resize(self):
        self.ht.insert("ВойнаиМир", "Л. Толстой - Война и мир")
        self.ht.insert("ВишневыйСад", "А. Чехов - Вишневый сад") 
        self.assertEqual(self.ht.size, 8)

    def test_delete(self):
        self.assertTrue(self.ht.delete("АннаКаренина"))
        self.assertEqual(self.ht.count, 1)
        self.assertIsNone(self.ht.get("АннаКаренина"))

    def test_update(self):
        self.assertTrue(self.ht.update("АннаКаренина", "Новое значение"))
        self.assertEqual(self.ht.get("АннаКаренина"), "Новое значение")

    def test_error_handling_in_public_methods(self):
        # Проверка вставки неверного ключа (длина < 2)
        with self.assertRaises(ValueError):
            self.ht.insert("A", "Короткий ключ")

        # Проверка поиска с неверным типом ключа (не строка)
        with self.assertRaises(ValueError):
            self.ht.get(123)

        # Проверка обновления с неверным ключом
        with self.assertRaises(ValueError):
            self.ht.update(123, "Значение")

        # Проверка удаления с неверным ключом
        with self.assertRaises(ValueError):
            self.ht.delete(123)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display(self, mock_stdout):
        self.ht.display()
        self.assertIn("АннаКаренина", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()