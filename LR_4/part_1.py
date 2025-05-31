from logical_function import LogicalFunction

def get_subtractor_truth_table():
    # Таблица истинности для ОДВ-3: A (уменьшаемое), B (вычитаемое), C (заем)
    # Выходы: D (разность), P (перенос)
    truth_table = {
        'A': [0, 0, 0, 0, 1, 1, 1, 1],
        'B': [0, 0, 1, 1, 0, 0, 1, 1],
        'C': [0, 1, 0, 1, 0, 1, 0, 1],
        'D': [0, 1, 1, 0, 1, 0, 0, 1], 
        'P': [0, 1, 1, 1, 0, 0, 0, 1]  
    }
    return truth_table

def build_sdnf(truth_table, output_name):
    sdnf_terms = []
    variables = ['A', 'B', 'C']
    
    for i in range(8):
        if truth_table[output_name][i] == 1: 
            term = []
            for var in variables:
                val = truth_table[var][i]
                term.append(f"{var if val else f'!{var}'}")
            sdnf_terms.append(" & ".join(term))
    
    return " | ".join([f"({term})" for term in sdnf_terms]) if sdnf_terms else "0"

def main():
    truth_table = get_subtractor_truth_table()

    print("Таблица истинности ОДВ-3:")
    print("A | B | C | D | P")
    print("-----------------")
    for i in range(8):
        print(f"{truth_table['A'][i]} | {truth_table['B'][i]} | {truth_table['C'][i]} | {truth_table['D'][i]} | {truth_table['P'][i]}")

    # Строим СДНФ для D и P
    D_sdnf = build_sdnf(truth_table, 'D')
    P_sdnf = build_sdnf(truth_table, 'P')

    print("\nСДНФ для разности (D):")
    print(D_sdnf)

    print("\nСДНФ для переноса (P):")
    print(P_sdnf)

    variables = ['A', 'B', 'C']

    D_function = LogicalFunction(
        variables,
        D_sdnf,
        {'D': truth_table['D']}
    )

    print("\nМинимизированная СДНФ для разности (D):")
    minimized_D_sdnf = D_function.minimize_sdnf_calculus()

    P_function = LogicalFunction(
        variables,
        P_sdnf,
        {'P': truth_table['P']}
    )

    print("\nМинимизированная СДНФ для переноса (P):")
    minimized_P_sdnf = P_function.minimize_sdnf_calculus()

if __name__ == "__main__":
    main()