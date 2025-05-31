from itertools import product
from logical_function import LogicalFunction

variables = ['x4', 'x3', 'x2', 'x1']

truth_table = {
    'y4': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1] + ['-'] * 6,  # 0-9 + избыточные
    'y3': [0, 0, 0, 1, 1, 1, 1, 0, 0, 0] + ['-'] * 6,
    'y2': [0, 1, 1, 0, 0, 1, 1, 0, 0, 1] + ['-'] * 6,
    'y1': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] + ['-'] * 6,
}

print("Таблица истинности для преобразователя 8421 → 8421+1:")
print("J | x4 x3 x2 x1 | y4 y3 y2 y1")
print("-----------------------------")
for j in range(16):
    x4, x3, x2, x1 = (j >> 3) & 1, (j >> 2) & 1, (j >> 1) & 1, j & 1
    y4 = truth_table['y4'][j] if j < len(truth_table['y4']) else '-'
    y3 = truth_table['y3'][j] if j < len(truth_table['y3']) else '-'
    y2 = truth_table['y2'][j] if j < len(truth_table['y2']) else '-'
    y1 = truth_table['y1'][j] if j < len(truth_table['y1']) else '-'
    print(f"{j:2}| {x4}  {x3}  {x2}  {x1} | {y4}  {y3}  {y2}  {y1}")

truth_table = {
    'y4': [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    'y3': [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    'y2': [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
    'y1': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
}    

print("\nМинимизация ДНФ для выходов:")
for output in ['y4', 'y3', 'y2', 'y1']:
    print(f"\n--- {output} ---")
    
    lf = LogicalFunction(
        variables=variables,
        expression=output,
        truth_table={output: truth_table[output]}
    )
    
    minimized_dnf = lf.minimize_with_kmap(is_dnf = True)
    print(f"Минимизированная ДНФ: {minimized_dnf}")
    
    print("\nКарта Карно:")
    lf.display_kmap(is_dnf=True)