from typing import Dict, List
from LR_2.variable_manager import VariableManager
from LR_2.rpn_converter import ReversePolishNotationConverter
from LR_2.truth_table_generator import TruthTableGenerator

class LogicalExpression:
    def __init__(self, expression: str):
        self.expression = expression
        self.variable_manager = VariableManager(expression)
        self.rpn_converter = ReversePolishNotationConverter(expression)
        self.rpn = self.rpn_converter.to_reverse_polish_notation()
        self.truth_table_generator = TruthTableGenerator(self.variable_manager.get_variable_map(), self.rpn)

    def generate_truth_table(self) -> Dict[str, List[bool]]:
        truth_table = self.variable_manager.get_variable_map().copy()
        final_result, intermediates = self.truth_table_generator.evaluate_expression()
        
        if intermediates:
            last_key = list(intermediates.keys())[-1]
            del intermediates[last_key]
        
        truth_table.update(intermediates)
        truth_table[self.expression] = final_result
        return truth_table

    def print_truth_table(self):
        truth_table = self.generate_truth_table()
        num_combinations = 2 ** self.variable_manager.count_variables()
        headers = list(truth_table.keys())
        
        col_widths = {header: max(len(header), 3) for header in headers}
        
        header_row = " | ".join(header.ljust(col_widths[header]) for header in headers)
        print(header_row)
        print("-" * len(header_row))
        
        for i in range(num_combinations):
            row = []
            for header in headers:
                val = '1' if truth_table[header][i] else '0'
                row.append(val.ljust(col_widths[header]))
            print(" | ".join(row))

    def generate_pdnf(self):
        result = []
        expression_result = self.generate_truth_table()[self.expression]

        for i in range(len(expression_result)):
            if expression_result[i]:
                clause = []
                for variable in self.variable_manager.get_variable_map().keys():
                    clause.append(variable if self.variable_manager.get_variable_map()[variable][i] else f"!{variable}")
                result.append(" & ".join(clause))

        return LogicalExpression(" | ".join(f"({clause})" for clause in result))

    def generate_pcnf(self):
        result = []
        expression_result = self.generate_truth_table()[self.expression]

        for i in range(len(expression_result)):
            if not expression_result[i]:
                clause = []
                for variable in self.variable_manager.get_variable_map().keys():
                    clause.append(f"!{variable}" if self.variable_manager.get_variable_map()[variable][i] else variable)
                result.append(" | ".join(clause))

        return LogicalExpression(" & ".join(f"({clause})" for clause in result))

    def to_numeric_form_pdnf(self) -> str:
        result = []
        expression_result = self.generate_truth_table()[self.expression]

        for i in range(len(expression_result)):
            if expression_result[i]:
                result.append(str(i))

        return f"( {' , '.join(result)} ) |"

    def to_numeric_form_pcnf(self) -> str:
        result = []
        expression_result = self.generate_truth_table()[self.expression]

        for i in range(len(expression_result)):
            if not expression_result[i]:
                result.append(str(i))

        return f"( {' , '.join(result)} ) &"

    def to_index_form(self) -> int:
        expression_result = self.generate_truth_table()[self.expression]
        binary_string = ''.join('1' if value else '0' for value in expression_result)
        return int(binary_string, 2)

    def get_expression(self) -> str:
        return self.expression