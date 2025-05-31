from typing import Dict, List, Tuple

class TruthTableGenerator:
    def __init__(self, variable_map: Dict[str, List[bool]], rpn: List[str]):
        self.variable_map = variable_map
        self.rpn = rpn

    def evaluate_expression(self) -> Tuple[List[bool], Dict[str, List[bool]]]:
        intermediate_results = {}
        final_result = []
        num_combinations = 2 ** len(self.variable_map)
        
        step_number = 1
        for token in self.rpn:
            if self.is_operator(token):
                op_name = f"step_{step_number} ({token})"
                intermediate_results[op_name] = [None] * num_combinations
                step_number += 1

        for i in range(num_combinations):
            stack = []
            step_number = 1
            
            for token in self.rpn:
                if self.is_operand(token):
                    stack.append(self.variable_map[token][i])
                elif self.is_operator(token):
                    op_name = f"step_{step_number} ({token})"
                    
                    if token == '!':
                        operand = stack.pop()
                        result = not operand
                    else:
                        operand2 = stack.pop()
                        operand1 = stack.pop()
                        if token == '&':
                            result = operand1 and operand2
                        elif token == '|':
                            result = operand1 or operand2
                        elif token == '->':
                            result = (not operand1) or operand2
                        elif token == '~':
                            result = operand1 == operand2
                    
                    intermediate_results[op_name][i] = result
                    stack.append(result)
                    step_number += 1
            
            final_result.append(stack.pop())

        return final_result, intermediate_results

    def is_operator(self, token: str) -> bool:
        return token in {'!', '&', '|', '~', '->'}

    def is_operand(self, token: str) -> bool:
        return token.isalnum()