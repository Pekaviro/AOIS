from typing import List

class ReversePolishNotationConverter:
    def __init__(self, expression: str):
        self.expression = expression

    def to_reverse_polish_notation(self) -> List[str]:
        result = []
        stack = []
        i = 0
        while i < len(self.expression):
            if self.expression[i] == '-' and i + 1 < len(self.expression) and self.expression[i + 1] == '>':
                operator = '->'
                i += 2
            else:
                operator = self.expression[i]
                i += 1

            if self.is_operand(operator):
                result.append(operator)
            elif operator == '(':
                stack.append(operator)
            elif operator == ')':
                while stack and stack[-1] != '(':
                    result.append(stack.pop())
                stack.pop()
            elif self.is_operator(operator):
                while stack and self.get_priority(stack[-1]) >= self.get_priority(operator):
                    result.append(stack.pop())
                stack.append(operator)
        
        while stack:
            result.append(stack.pop())
        
        return result

    def is_operator(self, token: str) -> bool:
        return token in {'!', '&', '|', '~', '->'}

    def get_priority(self, operator: str) -> int:
        return {
            '!': 5,
            '&': 4,
            '|': 3,
            '->': 2,
            '~': 1
        }.get(operator, 0)

    def is_operand(self, token: str) -> bool:
        return token.isalnum()