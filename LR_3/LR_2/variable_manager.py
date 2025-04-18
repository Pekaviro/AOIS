from typing import Dict, List

class VariableManager:
    def __init__(self, expression: str):
        self.expression = expression
        self.variable_map = {}
        self.initialize_variable_map()

    def extract_variables(self):
        for character in self.expression:
            if self.is_operand(character) and character not in self.variable_map:
                self.variable_map[character] = []

    def initialize_variable_map(self):
        self.extract_variables()
        num_vars = self.count_variables() 
        num_combinations = 2 ** num_vars   # Количество комбинаций

        for var in self.variable_map:
            self.variable_map[var] = []

        for i in range(num_combinations):
            bin_str = format(i, f'0{num_vars}b')
            for idx, var in enumerate(self.variable_map):
                self.variable_map[var].append(bin_str[idx] == '1')

    def is_operand(self, token: str) -> bool:
        return token.isalnum()

    def count_variables(self) -> int:
        return len(self.variable_map)

    def get_variable_map(self) -> Dict[str, List[bool]]:
        return self.variable_map