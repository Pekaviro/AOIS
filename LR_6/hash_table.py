class HashTable:
    def __init__(self, size=20, initialize_test_data=True):
        self.size = size
        self.count = 0
        self.table = [None] * size
        self.load_factor_threshold = 0.7
        if initialize_test_data:
            self._initialize_test_data()
    
    def _char_to_num(self, char):
        """Конвертирует русскую букву в числовое значение"""
        char = char.upper()
        if char == 'Ё':
            return 6
        code = ord(char) - ord('А')
        # Буквы после 'Е' (кроме 'Ё') смещаются на -1
        if code > 6:
            code -= 1
        return code if 0 <= code <= 32 else -1
    
    def _hash_function(self, key, B=0):
        """Вычисляет хеш-значение для ключа"""
        if not isinstance(key, str):
            raise ValueError("Ключ должен быть строкой")
        if len(key) < 2:
            raise ValueError("Ключ должен содержать хотя бы 2 символа")
        
        first_char = key[0]
        second_char = key[1]
        
        v1 = self._char_to_num(first_char)
        v2 = self._char_to_num(second_char)
        
        if v1 == -1 or v2 == -1:
            raise ValueError("Ключ должен начинаться с русских букв")
        
        V = v1 * 33 + v2
        hash_value = (V % self.size + B) % self.size
        return hash_value
    
    def _resize(self):
        """Увеличивает размер таблицы при достижении порога заполнения"""
        old_table = self.table
        self.size = self.size * 2
        self.table = [None] * self.size
        self.count = 0
        
        for item in old_table:
            if item is not None:
                key, value, _, _ = item
                self.insert(key, value)
    
    def _initialize_test_data(self):
        """Инициализация таблицы тестовыми данными"""
        literature_data = [
            ("АннаКаренина", "Л. Толстой - Анна Каренина"),
            ("АннаСнегина", "С. Есенин - Анна Снегина"),
            ("БратьяКарамазовы", "Ф. Достоевский - Братья Карамазовы"),
            ("БелаяГвардия", "М. Булгаков - Белая гвардия"),
            ("ВойнаиМир", "Л. Толстой - Война и мир"),
            ("ВишневыйСад", "А. Чехов - Вишневый сад"),
            ("ГеройНашегоВремени", "М. Лермонтов - Герой нашего времени"),
            ("ГореотУма", "А. Грибоедов - Горе от ума"),
            ("ЕвгенийОнегин", "А. Пушкин - Евгений Онегин"),
            ("КапитанскаяДочка", "А. Пушкин - Капитанская дочка"),
            ("МастериМаргарита", "М. Булгаков - Мастер и Маргарита"),
            ("МертвыеДуши", "Н. Гоголь - Мертвые души")
        ]
        
        for key, value in literature_data:
            self.insert(key, value)
    
    def insert(self, key, value):
        """Вставка элемента в хеш-таблицу"""
        if self.count / self.size >= self.load_factor_threshold:
            self._resize()
        
        B = 0
        original_index = self._hash_function(key)  # Здесь может возникнуть ValueError
        
        while True:
            index = self._hash_function(key, B)
            
            if self.table[index] is None:
                self.table[index] = (key, value, original_index, B)
                self.count += 1
                return True
            elif self.table[index][0] == key:
                self.table[index] = (key, value, original_index, B)
                return False
            
            B += 1
            if B >= self.size:
                self._resize()
                return self.insert(key, value)

    def get(self, key):
        """Поиск элемента по ключу"""
        B = 0
        while True:
            index = self._hash_function(key, B)  # Здесь может возникнуть ValueError
            
            if self.table[index] is None:
                return None
            elif self.table[index][0] == key:
                return self.table[index][1]
            
            B += 1
            if B >= self.size:
                return None

    def update(self, key, new_value):
        """Обновление значения по ключу"""
        B = 0
        while True:
            index = self._hash_function(key, B)  # Здесь может возникнуть ValueError
            
            if self.table[index] is None:
                return False
            elif self.table[index][0] == key:
                original_index = self.table[index][2]
                self.table[index] = (key, new_value, original_index, B)
                return True
            
            B += 1
            if B >= self.size:
                return False

    def delete(self, key):
        """Удаление элемента по ключу"""
        B = 0
        while True:
            index = self._hash_function(key, B)  # Здесь может возникнуть ValueError
            
            if self.table[index] is None:
                return False
            elif self.table[index][0] == key:
                self.table[index] = None
                self.count -= 1
                return True
            
            B += 1
            if B >= self.size:
                return False
    
    def display(self):
        """Вывод таблицы с обозначением коллизий"""
        print("\n+" + "-"*8 + "+" + "-"*25 + "+" + "-"*45 + "+" + "-"*20 + "+")
        print(f"| {'Индекс':^6} | {'Ключ':^23} | {'Литературное произведение':^43} | {'Коллизия':^18} |")
        print("+" + "-"*8 + "+" + "-"*25 + "+" + "-"*45 + "+" + "-"*20 + "+")
        
        for i in range(self.size):
            if self.table[i] is not None:
                key, value, original_index, B = self.table[i]
                if B > 0:
                    collision_info = f"Да ({original_index})"
                else:
                    collision_info = "Нет"
                print(f"| {i:^6} | {key:^23} | {value:^43} | {collision_info:^18} |")
            else:
                print(f"| {i:^6} | {'':^23} | {'':^43} | {'':^18} |")
        print("+" + "-"*8 + "+" + "-"*25 + "+" + "-"*45 + "+" + "-"*20 + "+")
