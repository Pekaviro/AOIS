class Word:
    def __init__(self, bits):
        if len(bits) != 16:
            raise ValueError("Слово должно быть 16-битным")
        self.bits = bits  # строка из '0' и '1'

    def get_v(self):
        return self.bits[0:3]

    def get_a(self):
        return self.bits[3:7]

    def get_b(self):
        return self.bits[7:11]

    def get_s(self):
        return self.bits[11:16]

    def set_s(self, new_s):
        if len(new_s) != 5:
            raise ValueError("Поле S должно быть 5 бит")
        self.bits = self.bits[:11] + new_s + self.bits[16:]

    def get_value(self, field):
        if field == 'v':
            return int(self.get_v(), 2)
        elif field == 'a':
            return int(self.get_a(), 2)
        elif field == 'b':
            return int(self.get_b(), 2)
        elif field == 's':
            return int(self.get_s(), 2)
        else:
            raise ValueError("Неизвестное поле")

    def __repr__(self):
        return (
            f"V: {self.get_v()} ({self.get_value('v')}) | "
            f"A: {self.get_a()} ({self.get_value('a')}) | "
            f"B: {self.get_b()} ({self.get_value('b')}) | "
            f"S: {self.get_s()} ({self.get_value('s')})"
        )