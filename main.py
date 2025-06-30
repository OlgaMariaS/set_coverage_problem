from ortools.linear_solver import pywraplp

def solve_ucp():
    """
    Função para modelar e resolver o Problema de Cobertura Única (UCP)
    usando a formulação do artigo de Beretta e Hoshino.
    """
    # --- 1. Dados da Instância ---
    # Baseado na Figura 1 do artigo [cite: 13, 14, 15, 16]
    # U = {1, 2, 3, 4, 5, 6, 7, 8}, S = {S1, S2, S3, S4}

    num_elementos = 8  # n: número de pontos/elementos
    num_conjuntos = 4  # m: número de conjuntos

    # Matriz de incidência a_ij: a[i][j] = 1 se o elemento i está no conjunto j
    # Elementos e conjuntos são indexados a partir de 0
    # Elemento 1 -> índice 0, ... Elemento 8 -> índice 7
    # Conjunto S1 -> índice 0, ... Conjunto S4 -> índice 3
    a = [
        # S1, S2, S3, S4
        [1, 0, 0, 0],  # Elemento 1
        [1, 1, 0, 0],  # Elemento 2
        [0, 1, 0, 0],  # Elemento 3
        [1, 0, 0, 0],  # Elemento 4
        [0, 1, 1, 0],  # Elemento 5
        [0, 0, 1, 0],  # Elemento 6
        [1, 0, 0, 1],  # Elemento 7
        [0, 0, 1, 1],  # Elemento 8
    ]

    # --- 2. Inicializar o Solver ---
    # Usaremos o solver SCIP que é bom para programação inteira mista.
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Solver SCIP não disponível.")
        return

    # --- 3. Declaração das Variáveis --- [cite: 48, 49]
    # Variável x_j: 1 se o conjunto j for escolhido, 0 caso contrário.
    x = {}
    for j in range(num_conjuntos):
        x[j] = solver.BoolVar(f'x_{j}')

    # Variável z_i: conta quantas vezes o elemento i é coberto.
    z = {}
    for i in range(num_elementos):
        # Limite superior pode ser o número de conjuntos.
        z[i] = solver.IntVar(0, num_conjuntos, f'z_{i}')

    # Variável y_i: 1 se o elemento i é coberto unicamente, 0 caso contrário.
    y = {}
    for i in range(num_elementos):
        y[i] = solver.BoolVar(f'y_{i}')

    # Constante M, um número grande. O número de conjuntos é um limite superior seguro. 
    M = num_conjuntos

    print(f"Número de variáveis = {solver.NumVariables()}")

    # --- 4. Definição das Restrições ---
    # Restrição (2) do artigo: z_i = soma(a_ij * x_j) [cite: 55]
    for i in range(num_elementos):
        solver.Add(sum(a[i][j] * x[j] for j in range(num_conjuntos)) == z[i])

    # Restrições (3) e (4) garantem que y_i seja 1 se e somente se z_i for 1. [cite: 56, 57, 58]
    for i in range(num_elementos):
        # Restrição (3): y_i <= z_i
        solver.Add(y[i] <= z[i])
        # Restrição (4): (M-1)*y_i + z_i <= M
        solver.Add((M - 1) * y[i] + z[i] <= M)

    print(f"Número de restrições = {solver.NumConstraints()}")

    # --- 5. Definição da Função Objetivo ---
    # Função Objetivo (1): Maximizar o número de elementos cobertos unicamente. [cite: 54]
    solver.Maximize(solver.Sum(y[i] for i in range(num_elementos)))

    # --- 6. Resolver o Problema ---
    status = solver.Solve()

    # --- 7. Apresentar os Resultados ---
    if status == pywraplp.Solver.OPTIMAL:
        print("\nSolução ótima encontrada!")
        print(f'Valor da Função Objetivo (elementos cobertos unicamente) = {int(solver.Objective().Value())}')
        
        print("\nConjuntos selecionados:")
        for j in range(num_conjuntos):
            if x[j].solution_value() > 0.5: # Verifica se é 1
                print(f'- Conjunto S{j+1}')

        print("\nDetalhes da cobertura por elemento:")
        for i in range(num_elementos):
            cobertura_z = z[i].solution_value()
            coberto_unicamente_y = "Sim" if y[i].solution_value() > 0.5 else "Não"
            print(f'Elemento {i+1}: coberto {int(cobertura_z)} vez(es). Cobertura única: {coberto_unicamente_y}')

    else:
        print('O problema não tem solução ótima.')

# Executa a função principal
if __name__ == '__main__':
    solve_ucp()