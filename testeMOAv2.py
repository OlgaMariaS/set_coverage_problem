from ortools.linear_solver import pywraplp
import time
from typing import List

# LEITURA, RESOLUÇÃO E ESCRITA DE INSTÂNCIAS SCP

class Subconjunto:
    def __init__(self):
        self.id = 0
        self.peso = 0
        self.elementos_cobertos = []
        self.var_escolha = 0

class Elemento:
    def __init__(self):
        self.id = 0
        self.num_coberturas = 0
        self.var_cobertura_unica = 0
        self.var_cobertura_total = 0

def abrir_arquivo(nome):
    try:
        with open(nome, "r") as arquivo:
            linhas_arquivo = arquivo.readlines()
        print("\nO arquivo foi aberto com sucesso!")
        return arquivo, linhas_arquivo
    except FileNotFoundError:
        print("\nERRO! O arquivo não foi aberto!")
        exit(1)

def ler_cabecalho(linhas_arquivo):
    primeira_linha = linhas_arquivo[0].strip().split()
    l = int(primeira_linha[0])
    c = int(primeira_linha[1])
    return l, c

def ler_conteudo(l, c, linhas_arquivo):
    # Inicializa variaveis
    subconjuntos = [Subconjunto() for _ in range(c)]
    matriz = [[0 for _ in range(c)] for _ in range(l)]
    elementos = [Elemento() for _ in range(l)]
    num_cobertos_atual = 0
    num_cobertos_total = 0
    i = 0
    j = 0

    # Leitura dos pesos dos subconjuntos
    linha_atual = 1
    while i<c:
        j = 0
        pesos = list(map(int, linhas_arquivo[linha_atual].strip().split()))
        while j<len(pesos):
            subconjuntos[i].id = i
            subconjuntos[i].peso = pesos[j]
            j += 1
            i += 1
        linha_atual += 1
        

    # Leitura das coberturas de cada elemento
    i = -1
    while linha_atual < len(linhas_arquivo):
        
        info = list(map(int, linhas_arquivo[linha_atual].strip().split()))

        if num_cobertos_atual == num_cobertos_total:
            elementos[i].num_coberturas = info[0]
            num_cobertos_total = info[0]
            num_cobertos_atual = 0
            i += 1
        else:
            for j in info:
                matriz[i][j-1] = 1
                subconjuntos[j-1].elementos_cobertos.append(i)
                num_cobertos_atual += 1
        
        linha_atual += 1
        
    return subconjuntos, matriz, elementos

def escreve_teste(linhas, colunas, elementos:Elemento, subconjuntos:Subconjunto, matriz, teste, arquivo_leitura, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo,  media_cobertura_total, tempo_execucao):
    
    try:
        escrita = open(arquivo_escrita, "a")
    except FileNotFoundError:
        print("\nERRO! O arquivo de escrita não foi aberto!")
        exit(1)

    if not teste:
        escrita.write("\n\n\n\nNome do arquivo: " + arquivo_leitura)
    else: 
        escrita.write("\n\n\n\nMatriz: " +  str(matriz))

    if num_vars == 0 or num_restricoes == 0:
        escrita.write("\nNao foi possivel criar o solver CBC\n\n")
        exit(1)
    
    escrita.write("\nSolver CBC criado com sucesso!")
    escrita.write("\nNumero de variaveis = " + str(num_vars))
    escrita.write("\nNumero de restricoes = " + str(num_restricoes))
    escrita.write("\nResolvendo com o solver " + versao_solver)

    if media_cobertura_total == 1:
        escrita.write("\n\nSolucao otima encontrada!")
    elif media_cobertura_total > 1:
        escrita.write("\n\nUma solucao factivel foi encontrada.")
    else:
        escrita.write("\nO problema nao tem solucao.")

    escrita.write("\n\nValor da Funcao Objetivo (elementos cobertos unicamente) = " + str(funcao_objetivo))
    escrita.write("\n\nConjuntos selecionados:")

    for j in range(colunas):
        if subconjuntos[j].var_escolha > 0.5:
            escrita.write(f"\n- Conjunto S {j+1}\n    Elementos cobertos: {subconjuntos[j].elementos_cobertos}")

    escrita.write("\n\nDetalhes da cobertura por elemento:")

    for i in range(linhas):
        coberto_unicamente = "Sim" if elementos[i].var_cobertura_unica > 0.5 else "Não"
        escrita.write(f'\nElemento {str(i+1)}: coberto {str(elementos[i].var_cobertura_total)} vez(es). Cobertura unica: {coberto_unicamente}')

    escrita.write(f"\nCobertura media dos elementos: {media_cobertura_total:.2f}")
    escrita.write(f"\nTempo de execucao da instancia: {tempo_execucao:.4f} segundos")

    escrita.close()


def executa_solver(linhas, colunas, elementos: List[Elemento], subconjuntos: List[Subconjunto], matriz, tempo_max, output):
    M = colunas
    media_cobertura_total = 0

    solver = pywraplp.Solver.CreateSolver("CBC")
    if not solver:
        print("Nao foi possivel criar o solver CBC")
        return 0 
    else:
        print("Solver CBC criado com sucesso!")

    infinity = solver.infinity()
    for j in range(colunas):
        subconjuntos[j].var_escolha = solver.BoolVar(f'x{j+1}')

    for i in range(linhas):
        elementos[i].var_cobertura_unica = solver.BoolVar(f'y{i+1}')
        elementos[i].var_cobertura_total = solver.IntVar(0, infinity, ('z' + str(i+1)))

    num_vars = solver.NumVariables()
    print("Numero de variáveis =", num_vars)

    for i in range(linhas):
        solver.Add(sum(matriz[i][j] * subconjuntos[j].var_escolha for j in range(colunas)) == elementos[i].var_cobertura_total)

    for i in range(linhas):
        solver.Add(elementos[i].var_cobertura_unica <= elementos[i].var_cobertura_total)
        solver.Add((M-1) * elementos[i].var_cobertura_unica + elementos[i].var_cobertura_total <= M)

    num_restricoes = solver.NumConstraints()
    print("Número de restrições =", num_restricoes)

    funcao_objetivo = solver.Objective()
    for i in range(linhas):
        funcao_objetivo.SetCoefficient(elementos[i].var_cobertura_unica, 1)
    funcao_objetivo.SetMaximization()

    solver.set_time_limit(tempo_max)
    if output:
        solver.EnableOutput()

    versao_solver = solver.SolverVersion()
    print("Resolvendo com o solver", versao_solver)

    start_time = time.time()
    resultado = solver.Solve()
    end_time = time.time()

    tempo_execucao = end_time - start_time

    if resultado == pywraplp.Solver.OPTIMAL or resultado == pywraplp.Solver.FEASIBLE:
        if resultado == pywraplp.Solver.OPTIMAL:
            print("\nSolução ótima encontrada!")
        else:
            print("\nUma solução factível foi encontrada")

        funcao_objetivo = funcao_objetivo.Value()
        print("\nValor da Função Objetivo (elementos cobertos unicamente) =", funcao_objetivo)

        print("\nConjuntos selecionados:")
        for j in range(colunas):
            subconjuntos[j].var_escolha = subconjuntos[j].var_escolha.solution_value()
            if subconjuntos[j].var_escolha > 0.5:
                print(f"- Conjunto S{j+1}\n    Elementos cobertos: {subconjuntos[j].elementos_cobertos}")

        print("\nDetalhes da cobertura por elemento:")
        for i in range(linhas):
            elementos[i].var_cobertura_total = elementos[i].var_cobertura_total.solution_value()
            elementos[i].var_cobertura_unica = elementos[i].var_cobertura_unica.solution_value()
            coberto_unicamente = "Sim" if elementos[i].var_cobertura_unica > 0.5 else "Não"
            print(f'Elemento {i+1}: coberto {int(elementos[i].var_cobertura_total)} vez(es). Cobertura única: {coberto_unicamente}')
            media_cobertura_total += elementos[i].var_cobertura_total

        media_cobertura_total /= linhas
        print(f"\nCobertura média dos elementos: {media_cobertura_total:.2f}")
    else:
        print('O problema não tem solução.')

    print(f"Tempo de execução da instância: {tempo_execucao:.4f} segundos")

    return num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao

def main():
    # Parametros básicos para a execução:

    # Nome do arquivo no qual o resultado dos testes poderá ser escrito (opcional).
    arquivo_escrita = "testes.txt"

    # Nome do arquivo a ser lido (opcional para testes).
    arquivo_leitura = "scp41.txt"
    
    # Tempo máximo de excução em milisegundos (milissegundos -> segundos/1000).
    tempo_max = 1000     
    
    # Avalia se o programa lerá o arquivo especificado em "nome" (teste=0) ou executará um teste com a matriz "ma" (teste=1).
    teste = 1 

    # Avalia se o resultado do solver será escrito no 'arquivo_escrita'.
    escrita = 0 

    # Define a saida de uma descrição detalhada do funcionamento do solver (opicional)
    output = 0

    # Total de linhas da matriz (calculado automaticamente para as instancias, uso predefinido apenas para testes)   
    linhas = 5

    # Total de colunas da matriz (calculado automaticamente para as instancias, uso predefinido apenas para testes)
    colunas = 5

    #Matriz 'ma' utilizada em testes.
    ma = [[1, 0, 0, 0, 1],  
          [0, 1, 0, 0, 0],  
          [1, 1, 0, 0, 0],  
          [1, 0, 0, 0, 1],  
          [0, 0, 1, 0, 0]]
    

    if not teste:

        # Abertura do 'arquivo_leitura'
        arquivo, linhas_arquivo = abrir_arquivo(arquivo_leitura)

        # Leitura do cabeçalho do 'arquivo_leitura'
        linhas, colunas = ler_cabecalho(linhas_arquivo)

        # Leitura do conteúdo do 'arquivo_leitura'
        subconjuntos, matriz, elementos = ler_conteudo(linhas, colunas, linhas_arquivo)

        # Execução do solver
        num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao = executa_solver(linhas, colunas, elementos, subconjuntos, matriz, tempo_max, output)
    else:

        # Inicialização das listas de subconjuntos e elementos
        subconjuntos = [Subconjunto() for j in range(colunas)]
        elementos = [Elemento() for i in range(linhas)]

        

        print("Matriz: ", ma)
        print("Linhas: ", linhas)
        print("Colunas: ", colunas)

        num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao = executa_solver(linhas, colunas, elementos, subconjuntos, ma, tempo_max, output)

    # Chamada da função de escrita, para gravar os resultados da execução do solver no 'arquivo_escrita'
    if escrita:
        if not teste:
            escreve_teste(linhas, colunas, elementos, subconjuntos, matriz, teste, arquivo_leitura, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao)
        else:
            escreve_teste(linhas, colunas, elementos, subconjuntos, ma, teste, arquivo_leitura, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao)
        
    #print("\nMatriz: ")
    #for i in range(linhas):
     #   for j in range(colunas):
      #      print(("a", i+1, j+1 ) + (" = ", matriz[i][j]))

    

if __name__ == "__main__":
    main()  
