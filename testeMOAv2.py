from ortools.linear_solver import pywraplp
import time
from typing import List

# LEITURA, RESOLUÇÃO E ESCRITA DE INSTÂNCIAS SCP

# Classe que representa um subconjunto, com seu ID, peso, elementos cobertos e variável de decisão
class Subconjunto:
    def __init__(self, id=0):
        self.id = 0
        self.peso = 0
        self.elementos_cobertos = []
        self.var_escolha = 0

# Classe que representa um elemento e suas variáveis de cobertura
class Elemento:
    def __init__(self, id=0):
        self.id = 0
        self.num_coberturas = 0
        self.var_cobertura_unica = 0
        self.var_cobertura_total = 0

# Classe que representa um arquivo scp.txt
class Arquivo_scp:
    def __init__(self, id=0):
        self.id = 0
        self.arquivo = 0
        self.nome = []
        self.linhas = 0
        self.colunas = 0
        self.conjuntos_escolhidos = []

# Função que abre o arquivo de entrada e lê todas as linhas
# Retorna uma lista de strings com o conteúdo do arquivo
# Se não conseguir abrir, encerra o programa
def abrir_arquivo(arquivo_leitura):
        try:
            with open(arquivo_leitura.nome, "r") as arquivo_leitura.arquivo:
                linhas_arquivo = arquivo_leitura.arquivo.readlines()

                # Leitura do cabeçalho do 'arquivo_leitura'
                arquivo_leitura.linhas, arquivo_leitura.colunas = ler_cabecalho(linhas_arquivo)

                # Leitura do conteúdo do 'arquivo_leitura'
                subconjuntos, matriz, elementos = ler_conteudo(arquivo_leitura.linhas, arquivo_leitura.colunas, linhas_arquivo)

                arquivo_leitura.arquivo.close()
            print("\nO arquivo foi aberto com sucesso!")
            return subconjuntos, matriz, elementos
        except FileNotFoundError:
            print("\nERRO! O arquivo não foi aberto!")
            exit(1)

# Função que lê a primeira linha do arquivo contendo:
# - número de linhas (elementos)
# - número de colunas (subconjuntos)
# Retorna os dois valores como inteiros
def ler_cabecalho(linhas_arquivo):
    primeira_linha = linhas_arquivo[0].strip().split()
    l = int(primeira_linha[0])
    c = int(primeira_linha[1])
    return l, c

def ler_conteudo(l, c, linhas_arquivo):
    # Inicializa variaveis:

    # Lista dos elementos(linhas)
    elementos = [Elemento(id=i) for i in range(l)]

    # Lista dos subconjuntos(colunas)
    subconjuntos = [Subconjunto(id=j) for j in range(c)]

    # Matriz linhas x colunas
    matriz = [[0 for _ in range(c)] for _ in range(l)]

    # Numero de coberturas total do elemento atual
    num_cobertos_total = 0

    # Numero de coberturas realizadas para o elemento atual
    num_cobertos_atual = 0

    # Variáveis de auxílio
    i = 0
    j = 0

    # Linha atual para leitura
    linha_atual = 1

    # Leitura dos pesos dos subconjuntos
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
    # 'i' representa o numeros de elementos lidos
    i = 0
    while linha_atual < len(linhas_arquivo):
        
        # Leitura da linha atual
        conteudo_linha = list(map(int, linhas_arquivo[linha_atual].strip().split()))

        # Verifica se já leu todos os subconjuntos que cobrem um elemento
        # Se 'num_cobertos_atual == num_cobertos_total', isso significa que: ou estão na primeira iteração, ou já foram lidos todos os subconjuntos que cobrem um elemento  
        if num_cobertos_atual == num_cobertos_total:
            # Se a iteração entro no 'if', significa que já lemos todos as coberturas do elemento anterior, o que siginifica que o 'conteudo_linha' contem o número de coberturas do elemento posteirio (elemento[i+1])
            elementos[i-1].num_coberturas = conteudo_linha[0]
            num_cobertos_total = conteudo_linha[0]
            num_cobertos_atual = 0
            i += 1
        else:
            # Seta em 1 a cobertura do elemento aij na matriz para cada j presente em conteudo linha
            for j in conteudo_linha:
                matriz[i-1][j-1] = 1
                subconjuntos[j-1].elementos_cobertos.append(i-1)
                num_cobertos_atual += 1
        
        # Avança para a próxima linha]
        linha_atual += 1
        
    return subconjuntos, matriz, elementos

def escreve_teste(linhas, colunas, elementos:Elemento, subconjuntos:Subconjunto, matriz, teste, arquivo_leitura, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo,  media_cobertura_total, tempo_execucao):
    
    # Abertura do arquivo de escrita
    try:
        with open(arquivo_escrita, "a") as escrita:
            # Alterna a escrita inicial dependendo se for um teste ou não
            if not teste:
                escrita.write("\n\n\n\nNome do arquivo: " + arquivo_leitura)
            else: 
                escrita.write("\n\n\n\nMatriz: " +  str(matriz))

            # Se não foi possivel criar variaveis ou restricoes, escreve que não foi possivel a criação do solver e finaliza a execução o programa
            if num_vars == 0 or num_restricoes == 0:
                escrita.write("\nNao foi possivel criar o solver CBC\n\n")
                exit(1)

            # Elementos centrais do solver 
            escrita.write("\nSolver CBC criado com sucesso!")

            escrita.write("\n\nFuncao objetivo:")
            escrita.write("\n          Max ∑ yᵢ                                               para i=1 até Linhas")
            escrita.write("\nSujeito a:") 
            escrita.write("\n          ∑ aᵢⱼ·xⱼ = zᵢ                    ∀i, 1 <= i <= Linhas, para j=1 até Colunas")
            escrita.write("\n          yᵢ <= zᵢ                         ∀i, 1 <= i <= Linhas")
            escrita.write("\n          (M - 1)yᵢ + zᵢ <= M              ∀i, 1 <= i <= Linhas")
            escrita.write("\n          y ∈ {0,1}ⁿ, z ∈ ℤⁿ, x ∈ {0,1}ᵐ")
            escrita.write("\n\nNumero total de variaveis = " + str(num_vars))
            escrita.write("\nNumero total de restricoes = " + str(num_restricoes))
            
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
    except FileNotFoundError:
        print("\nERRO! O arquivo de escrita não foi aberto!")
        exit(1)


def executa_solver(linhas, colunas, elementos: List[Elemento], subconjuntos: List[Subconjunto], matriz, tempo_max, output):
    # Definição de M ≥ |U|
    M = colunas + 1
    media_cobertura_total = 0

    # Instancia o solver CBC
    solver = pywraplp.Solver.CreateSolver("CBC")
    if not solver:
        print("Nao foi possivel criar o solver CBC")
        return 0 
    else:
        print("Solver CBC criado com sucesso!")

    infinity = solver.infinity()

    # Define as variáveis booleanas xⱼ
    for j in range(colunas):
        subconjuntos[j].var_escolha = solver.BoolVar(f'x{j+1}')

    for i in range(linhas):
        # Define as variáveis booleanas yᵢ
        elementos[i].var_cobertura_unica = solver.BoolVar(f'y{i+1}')

        # Define as variáveis inteiras zᵢ
        elementos[i].var_cobertura_total = solver.IntVar(0, infinity, (f'z{i+1}'))

    num_vars = solver.NumVariables()

    # Define a restrição 1) -> ∑ aᵢⱼ·xⱼ = zᵢ
    for i in range(linhas):
        solver.Add(sum(matriz[i][j] * subconjuntos[j].var_escolha for j in range(colunas)) == elementos[i].var_cobertura_total)

    for i in range(linhas):
        # Define a restrição 2) -> yᵢ ≤ zᵢ
        solver.Add(elementos[i].var_cobertura_unica <= elementos[i].var_cobertura_total)

        # Define a restrição 3) -> (M - 1)yᵢ + zᵢ ≤ M 
        solver.Add((M-1) * elementos[i].var_cobertura_unica + elementos[i].var_cobertura_total <= M)
    num_restricoes = solver.NumConstraints()

    
    funcao_objetivo = solver.Objective()
    for i in range(linhas):
        # Define a função objetivo como ∑ yᵢ
        funcao_objetivo.SetCoefficient(elementos[i].var_cobertura_unica, 1)

    # Define a função objetivo como maximização
    funcao_objetivo.SetMaximization()

    print("\nFuncao objetivo:")
    print("            Max ∑ yᵢ                             para i=1 até Linhas")
    print("Sujeito a:") 
    print("            ∑ aᵢⱼ·xⱼ = zᵢ                        ∀i, 1 ≤ i ≤ Linhas, para j=1 até Colunas")
    print("            yᵢ ≤ zᵢ                              ∀i, 1 ≤ i ≤ Linhas")
    print("            (M - 1)yᵢ + zᵢ ≤ M                   ∀i, 1 ≤ i ≤ Linhas")
    print("            y ∈ {0,1}ⁿ, z ∈ ℤⁿ, x ∈ {0,1}ᵐ")
    print("\nNumero de variáveis =", num_vars)
    print("Número de restrições =", num_restricoes)

    # Define tempo máximo de execução do solver
    solver.set_time_limit(tempo_max)

    # Define a saida de um output muito detalhado do 'branch-and-bound' ('branch-and-cut' no caso do solver CBC)*Dar uma pesquisada depois*
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

    # Quantidade de Arquivos a serem lidos.
    qtd_arquivos_leitura = 5

    # Inicialização dos arquivos de leitura.
    arquivo_leitura = [Arquivo_scp(id=i) for i in range(qtd_arquivos_leitura)]

    # Nome dos arquivos a serem lidos (opcional para testes).
    arquivo_leitura[0].nome = "scp41.txt"
    arquivo_leitura[1].nome = "scp49.txt"
    arquivo_leitura[2].nome = "scp51.txt"
    arquivo_leitura[3].nome = "scp57.txt"
    arquivo_leitura[4].nome = "scp63.txt"
    
    # Tempo máximo de excução em milisegundos (milissegundos -> segundos/1000).
    tempo_max = 1000     
    
    # Avalia se o programa lerá o arquivo especificado em "nome" (teste=0) ou executará um teste com a matriz "ma" (teste=1).
    teste = 0

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
        for i in range(qtd_arquivos_leitura):
            # Abertura do 'arquivo_leitura'
            subconjuntos, matriz, elementos= abrir_arquivo(arquivo_leitura[i])

            # Execução do solver
            num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao = executa_solver(arquivo_leitura[i].linhas, arquivo_leitura[i].colunas, elementos, subconjuntos, matriz, tempo_max, output)

            if escrita:
                # Grava o retorno do solver no 'arquivo_escrita'
                escreve_teste(linhas, colunas, elementos, subconjuntos, matriz, teste, arquivo_leitura, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao)
    else:

        # Inicialização das listas de subconjuntos e elementos
        subconjuntos = [Subconjunto() for j in range(colunas)]
        elementos = [Elemento() for i in range(linhas)]

        print("Matriz: ", ma)
        print("Linhas: ", linhas)
        print("Colunas: ", colunas)

        num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao = executa_solver(linhas, colunas, elementos, subconjuntos, ma, tempo_max, output)

        if escrita:
            escreve_teste(linhas, colunas, elementos, subconjuntos, ma, teste, arquivo_leitura, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao)


    #print("\nMatriz: ")
    #for i in range(linhas):
     #   for j in range(colunas):
      #      print(("a", i+1, j+1 ) + (" = ", matriz[i][j]))

    

if __name__ == "__main__":
    main()  
