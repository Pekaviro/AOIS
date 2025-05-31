from itertools import product
from logical_function import LogicalFunction

variables = ['q3', 'q2', 'q1', 'v']

inputs = {
    'in3':[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    'in2':[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    'in1':[0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]
}

outputs = {
    'out3':[0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    'out2':[0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1],
    'out1':[0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0]
}

def compare_dicts(dict1, dict2):
    result = {}
    for key_in in dict1:
        key_out = key_in.replace('in', 'out')
        if key_out in dict2:
            list1 = dict1[key_in]
            list2 = dict2[key_out]
            compared = [1 if a != b else 0 for a, b in zip(list1, list2)]
           
            new_key = key_in.replace('in', 'h')
            result[new_key] = compared
    return result

truth_table = compare_dicts(inputs, outputs)

table = []
for i in range(len(inputs['in1'])):
    row = [
        inputs['in3'][i], inputs['in2'][i], inputs['in1'][i],
        i % 2, 
        outputs['out3'][i], outputs['out2'][i], outputs['out1'][i], 
        truth_table['h3'][i], truth_table['h2'][i], truth_table['h1'][i]  
    ]
    table.append(row)

headers = ["in3", "in2", "in1", "v", "out3", "out2", "out1", "h3", "h2", "h1"]

col_widths = [
    max(len(head), max(len(str(row[i])) for row in table) + 2)
    for i, head in enumerate(headers)
]

header_line = " | ".join(head.ljust(col_widths[i]) for i, head in enumerate(headers))
print(header_line)
print("-" * len(header_line))

for row in table:
    row_str = " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
    print(row_str)

print("\nМинимизация ДНФ для выходов:")
for output in ['h3', 'h2', 'h1']:
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