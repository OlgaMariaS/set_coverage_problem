from ortools.linear_solver import pywraplp
import time
import os
from typing import List

# LEITURA, RESOLUÇÃO E ESCRITA DE INSTÂNCIAS SCP

# Classe que representa um subconjunto, com seu ID, peso, elementos cobertos e variável de decisão
class Subconjunto:
    def __init__(self, id):
        self.id = id
        self.peso = 0
        self.elementos_cobertos = []
        # Variáveis x
        self.var_escolha = 0

# Classe que representa um elemento e suas variáveis de cobertura
class Elemento:
    def __init__(self, id):
        self.id = id
        self.num_coberturas = 0
        # Variáveis y
        self.var_cobertura_unica = 0
        # Variáveis z
        self.var_cobertura_total = 0

# Classe que representa um arquivo scp.txt
class Arquivo_scp:
    def __init__(self, id):
        self.id = id
        self.arquivo = 0
        self.caminho = []
        self.nome = []
        self.linhas = 0
        self.colunas = 0
        self.conjuntos_escolhidos = []

# Função que abre o arquivo de entrada e lê todas as linhas
# Retorna uma lista de strings com o conteúdo do arquivo
# Se não conseguir abrir, encerra o programa
def abrir_arquivo(arquivo_leitura):
        try:
            with open(arquivo_leitura.caminho, "r") as arquivo_leitura.arquivo:
                linhas_arquivo = arquivo_leitura.arquivo.readlines()

                # Leitura do cabeçalho do 'arquivo_leitura'
                arquivo_leitura.linhas, arquivo_leitura.colunas = ler_cabecalho(linhas_arquivo)

                # Leitura do conteúdo do 'arquivo_leitura'
                subconjuntos, matriz, elementos = ler_conteudo(arquivo_leitura.linhas, arquivo_leitura.colunas, linhas_arquivo)

                # Fechamento do arquivo
                arquivo_leitura.arquivo.close()
            print("\nO arquivo foi aberto com sucesso!")
            return subconjuntos, matriz, elementos
        except FileNotFoundError:
            print("\nERRO! O arquivo não foi aberto!")
            exit(1)
        

# Função que lê a primeira linha do arquivo contendo:
# - número de linhas (elementos);
# - número de colunas (subconjuntos);
# Retorna os dois valores como inteiros
def ler_cabecalho(linhas_arquivo):
    primeira_linha = linhas_arquivo[0].strip().split()
    linhas = int(primeira_linha[0])
    colunas = int(primeira_linha[1])
    return linhas, colunas


# Lê o conteudo da instância, armazenado no 'linhas_arquivo', contendo:
# - pesos dos subconjuntos;
# - quantidades de cobertura de cada elemento;
# - subconjuntos que cobrem cada elemento;
# Retorna: Lista de subconjuntos, Lista de elementos e Matriz de cobertura, nesta ordem.
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
                subconjuntos[j-1].elementos_cobertos.append(i)
                num_cobertos_atual += 1
        
        # Avança para a próxima linha]
        linha_atual += 1
        
    return subconjuntos, elementos, matriz

# Função executada para a gravação das execuções do solver no 'arquivo_escrita', definido na main()
def escreve_teste(arquivo_leitura:Arquivo_scp, elementos:List[Elemento], subconjuntos: List[Subconjunto], matriz, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo,  media_cobertura_total, tempo_execucao):

    if arquivo_leitura.id == 0:
        tipo_leitura = "w"
    else:
        tipo_leitura = "a"

    # Abertura do arquivo de escrita
    try:
        with open(arquivo_escrita, tipo_leitura, encoding="utf-8") as escrita:
            # Alterna a escrita inicial dependendo se for um teste ou não

            if arquivo_leitura.nome == "TESTE":
                escrita.write(f"\n\n\n\t*****TESTE*****")

            # Elementos centrais do solver 
            escrita.write("\n\n\n\nFunção Objetiva:")
            escrita.write("\n                   Max ∑ yᵢ                             para i=1 até Linhas")
            escrita.write("\nSujeito a:") 
            escrita.write("\n                   ∑ aᵢⱼ·xⱼ = zᵢ                        ∀i, 1 ≤ i ≤ Linhas, para j=1 até Colunas")
            escrita.write("\n                   yᵢ ≤ zᵢ                              ∀i, 1 ≤ i ≤ Linhas")
            escrita.write("\n                   (M - 1)yᵢ + zᵢ ≤ M                   ∀i, 1 ≤ i ≤ Linhas")
            escrita.write("\n                   y ∈ {0,1}ⁿ, z ∈ ℤⁿ, x ∈ {0,1}ᵐ")


            # Se não foi possivel criar variaveis ou restricoes, escreve que não foi possivel a criação do solver e finaliza a execução o programa
            if num_vars == 0 or num_restricoes == 0:
                escrita.write("\nNao foi possivel criar o solver CBC\n\n")
                exit(1)
            escrita.write("\nSolver CBC criado com sucesso!")

            if not arquivo_leitura.nome == "TESTE":
                escrita.write(f"\n\n\n{arquivo_leitura.id+1})")

            escrita.write("\nInstancia: " + arquivo_leitura.nome)
            escrita.write("\nLinhas: " + str(arquivo_leitura.linhas))
            escrita.write("\nColunas: " + str(arquivo_leitura.colunas))

            escrita.write("\n\nNumero total de variaveis = " + str(num_vars))
            escrita.write("\nNumero total de restricoes = " + str(num_restricoes))
            
            escrita.write("\nResolvendo com o solver " + versao_solver)

            if media_cobertura_total == 1:
                escrita.write("\n\nSolucao otima encontrada!")
            elif media_cobertura_total > 1:
                escrita.write("\n\nUma solucao factivel foi encontrada.")
            elif media_cobertura_total == 0:
                escrita.write("\nO problema nao tem solucao.")

            escrita.write("\n\nValor da Funcao Objetivo (elementos cobertos unicamente) = " + str(funcao_objetivo))
            escrita.write("\n\nConjuntos selecionados:")

            for j in range(arquivo_leitura.colunas):
                if subconjuntos[j].var_escolha > 0.5:
                    escrita.write(f"\n- Conjunto S {j+1}\n    Elementos cobertos: {subconjuntos[j].elementos_cobertos}")

            escrita.write("\n\nDetalhes da cobertura por elemento:")
            
            for i in range(arquivo_leitura.linhas):
                coberto_unicamente = "Sim" if elementos[i].var_cobertura_unica > 0.5 else "Não"
                escrita.write(f'\nElemento {str(i+1)}: coberto {str(elementos[i].var_cobertura_total)} vez(es). Cobertura unica: {coberto_unicamente}')

            escrita.write(f"\nCobertura media dos elementos: {media_cobertura_total:.2f}")
            if arquivo_leitura.nome == "TESTE":
                escrita.write(f"\n\nTempo de execucao da instancia: {tempo_execucao[len(tempo_execucao)-1]:.4f} segundos")
            else:
                escrita.write(f"\n\nTempo de execucao da instancia: {tempo_execucao[arquivo_leitura.id]:.4f} segundos")

            escrita.close()
    except FileNotFoundError:
        print("\nERRO! O arquivo de escrita não foi aberto!")
        exit(1)


def executa_solver(arquivo_leitura: List[Arquivo_scp], matriz, tempo_max, output_branch_and_bound, output_padrao_completo, escrita, arquivo_escrita):
    # Inicialização das variaveis:

    # Quantidade de arquivos no vetor arquivo leitura, menos o 'TESTE'
    qtd_arquivos = arquivo_leitura[len(arquivo_leitura)-1].id

    #Inicialização da média da cobertura total de um elemento
    media_cobertura_total = 0

    # Vetor  que armazena o tempo de execução de cada instância.
    tempo_execucao = [0 for _ in range(len(arquivo_leitura))]

    if escrita:
        try:
            with open(arquivo_escrita, "r", encoding="utf-8") as arquivo:
                linhas_arquivo = arquivo.readlines()

                if not linhas_arquivo:
                    escrita_permitida = 1
                else:
                    escrita_permitida = 0

                arquivo.close()
        except FileNotFoundError:
            escrita_permitida = 1 
    
    if qtd_arquivos == -1:
        print(f"\n\t*TESTE*")

    print("\nFuncao objetivo:")
    print("            Max ∑ yᵢ                             para i=1 até Linhas")
    print("Sujeito a:") 
    print("            ∑ aᵢⱼ·xⱼ = zᵢ                        ∀i, 1 ≤ i ≤ Linhas, para j=1 até Colunas")
    print("            yᵢ ≤ zᵢ                              ∀i, 1 ≤ i ≤ Linhas")
    print("            (M - 1)yᵢ + zᵢ ≤ M                   ∀i, 1 ≤ i ≤ Linhas")
    print("            y ∈ {0,1}ⁿ, z ∈ ℤⁿ, x ∈ {0,1}ᵐ")
    
    # Verifica se a execução é um teste
    if qtd_arquivos == -1:

        # Garante a leitura apenas do ultimo elemento do vetor arquivo_leitura, sendo ele o teste
        qtd_arquivos = len(arquivo_leitura)
        qtd = len(arquivo_leitura)-1

        # Inicialização das listas de subconjuntos e elementos do teste
        subconjuntos = [Subconjunto(id=j) for j in range(arquivo_leitura[qtd].colunas)]
        elementos = [Elemento(id = i) for i in range(arquivo_leitura[qtd].linhas)]
    else:
        qtd = 0

    while qtd < qtd_arquivos:
        i = 0
        j = 0


        # Instancia o solver CBC
        solver = pywraplp.Solver.CreateSolver("CBC")
        if not solver:
            print("\n\nNao foi possivel criar o solver CBC")
            return 0 
        else:
            print("\n\nSolver CBC criado com sucesso!\n")

        infinity = solver.infinity()
        
        if arquivo_leitura[qtd].nome == "TESTE":

            # Verifica a cobertura de cada elemento, gravando os elementos cobertos por cada conjunto do TESTE
            for i in range(arquivo_leitura[qtd].linhas):
                for j in range(arquivo_leitura[qtd].colunas):
                    aux = matriz[i][j]

                    if aux == 1:
                        elementos[i].num_coberturas += 1
                        subconjuntos[j].elementos_cobertos.append(i+1)
        else:
            # Abertura do 'arquivo_leitura'
            subconjuntos, elementos, matriz  = abrir_arquivo(arquivo_leitura[qtd])
            print(f'\n\n{qtd+1})')

        print(f'Instância = {arquivo_leitura[qtd].nome}')
        print(f'Linhas = {arquivo_leitura[qtd].linhas}')
        print(f'Colunas = {arquivo_leitura[qtd].colunas}')

        # Definição de M ≥ |U|
        M = arquivo_leitura[qtd].colunas + 1
        
        # Define as variáveis booleanas xⱼ
        for j in range(arquivo_leitura[qtd].colunas):
            subconjuntos[j].var_escolha = solver.BoolVar(f'x{j+1}')

        for i in range(arquivo_leitura[qtd].linhas):
            # Define as variáveis booleanas yᵢ
            elementos[i].var_cobertura_unica = solver.BoolVar(f'y{i+1}')

            # Define as variáveis inteiras zᵢ
            elementos[i].var_cobertura_total = solver.IntVar(0, infinity, (f'z{i+1}'))

        num_vars = solver.NumVariables()

        # Define a restrição 1) -> ∑ aᵢⱼ·xⱼ = zᵢ (aᵢⱼ -> matriz[i][j]; xⱼ -> subconjuntos[j].var_escolha; zᵢ -> elementos[i].var_cobertura_total)
        for i in range(arquivo_leitura[qtd].linhas):
            solver.Add(sum(matriz[i][j] * subconjuntos[j].var_escolha for j in range(arquivo_leitura[qtd].colunas)) == elementos[i].var_cobertura_total)

        for i in range(arquivo_leitura[qtd].linhas):
            # Define a restrição 2) -> yᵢ ≤ zᵢ
            solver.Add(elementos[i].var_cobertura_unica <= elementos[i].var_cobertura_total)

            # Define a restrição 3) -> (M - 1)yᵢ + zᵢ ≤ M 
            solver.Add((M-1) * elementos[i].var_cobertura_unica + elementos[i].var_cobertura_total <= M)

        num_restricoes = solver.NumConstraints()
        
        funcao_objetivo = solver.Objective()
        for i in range(arquivo_leitura[qtd].linhas):
            # Define a função objetivo como ∑ yᵢ
            funcao_objetivo.SetCoefficient(elementos[i].var_cobertura_unica, 1)

        # Define a função objetivo como maximização
        funcao_objetivo.SetMaximization()

        print("\nNumero de variáveis =", num_vars)
        print("Número de restrições =", num_restricoes)

        # Define tempo máximo de execução do solver
        solver.set_time_limit(tempo_max)

        # Define a saida de um output muito detalhado do 'branch-and-bound' ('branch-and-cut' no caso do solver CBC)*Dar uma pesquisada depois*
        if output_branch_and_bound:
            solver.EnableOutput()

        versao_solver = solver.SolverVersion()
        print("\nResolvendo com o solver", versao_solver)

        start_time = time.time()
        resultado = solver.Solve()
        end_time = time.time()

        tempo_execucao[qtd] = end_time - start_time

        if resultado == pywraplp.Solver.OPTIMAL or resultado == pywraplp.Solver.FEASIBLE:
            if resultado == pywraplp.Solver.OPTIMAL:
                print('\nSolução ótima encontrada!')
            else:
                print('\nUma solução factível foi encontrada.')

            funcao_objetivo = funcao_objetivo.Value()
            print(f'\nValor da Função Objetivo (elementos cobertos unicamente) = {funcao_objetivo}')

            for j in range(arquivo_leitura[qtd].colunas):
                subconjuntos[j].var_escolha = subconjuntos[j].var_escolha.solution_value()
                if subconjuntos[j].var_escolha > 0.5:
                    arquivo_leitura[qtd].conjuntos_escolhidos.append(subconjuntos[j].id)

            for i in range(arquivo_leitura[qtd].linhas):
                elementos[i].var_cobertura_total = elementos[i].var_cobertura_total.solution_value()
                elementos[i].var_cobertura_unica = elementos[i].var_cobertura_unica.solution_value()
                media_cobertura_total += elementos[i].var_cobertura_total
            media_cobertura_total /= arquivo_leitura[qtd].linhas

            # Descreve todos os subconjuntos selecionados e seus respectivos elementos cobertos
            if output_padrao_completo == 1:
                print('\nConjuntos selecionados:')
                for j in range(arquivo_leitura[qtd].colunas):
                    if subconjuntos[j].var_escolha > 0.5:
                        print(f'- Conjunto S{j+1}\n    Elementos cobertos: {subconjuntos[j].elementos_cobertos}')

                print(f'\nDetalhes da cobertura por elemento da instancia {arquivo_leitura[qtd].nome}:')
                for i in range(arquivo_leitura[qtd].linhas):
                    coberto_unicamente = "Sim" if elementos[i].var_cobertura_unica > 0.5 else "Não"
                    print(f'Elemento {i+1}: coberto {int(elementos[i].var_cobertura_total)} vez(es). Cobertura única: {coberto_unicamente}')

            print(f"\nCobertura média dos elementos: {media_cobertura_total:.2f}")
        else:
            print('O problema não tem solução.')
            funcao_objetivo = 0
            media_cobertura_total = 0

        print(f"Tempo de execução da instância: {tempo_execucao[qtd]:.4f} segundos") 

        if escrita:
            if qtd == len(arquivo_leitura) - 1:
                arquivo_escrita = "testes.txt"
                # Grava o retorno do solver no 'arquivo_escrita'
                escreve_teste(arquivo_leitura[qtd], elementos, subconjuntos, matriz, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao)
            else:
                if escrita_permitida:
                    # Grava o retorno do solver no 'arquivo_escrita'
                    escreve_teste(arquivo_leitura[qtd], elementos, subconjuntos, matriz, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao)
                else:
                    while True:
                        resposta = input("Deseja sobrescrever o arquivo atual? (s/n): ").strip().lower()
                        if resposta in ["s", "n"]:
                            break
                        print("Por favor, digite 's' para sim ou 'n' para não.")

                    if resposta == "s":
                        # Grava o retorno do solver no 'arquivo_escrita'
                        escreve_teste(arquivo_leitura[qtd], elementos, subconjuntos, matriz, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao)
                        escrita_permitida = 1
                    else:
                        escrita = 0

        qtd += 1

    # Verifica se mais de 1 execução foi realizada para a impressão da soma dos tempos de execução
    if not (arquivo_leitura[qtd-1].nome == "TESTE" or qtd_arquivos == 1):
        print(f"\nTempo total de execução da(s) {qtd} instância(s): {sum(tempo_execucao):.4f} segundos")

        if escrita:
            with open(arquivo_escrita, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"\n\nTempo total de execção da(s) {qtd} instância(s): {sum(tempo_execucao):.4f} segundos")
                arquivo.close()


    return

def main():
    # Parametros básicos para a execução:
    
    # Nome do arquivo no qual o resultado dos testes poderá ser escrito (opcional).
    arquivo_escrita = "resultados.txt"

    # Quantidade de Arquivos a serem lidos.
    #qtd_arquivos_leitura = 5


    # Nome dos arquivos a serem lidos (arquivo_leitura[qtd_arquivos_leitura] reservada para testes).
    #arquivo_leitura[0].nome = "scp49.txt"
    #arquivo_leitura[1].nome = "scp51.txt"
    #arquivo_leitura[2].nome = "scp57.txt"
    #arquivo_leitura[3].nome = "scp63.txt"
    #arquivo_leitura[4].nome = "scp65.txt"

    # Caminho da pasta onde o script está
    pasta_script = os.path.dirname(os.path.abspath(__file__))

    # Caminho completo da subpasta "instancias"
    pasta_instancias = os.path.join(pasta_script, "Instâncias")

    # Lista os arquivos .txt dentro da pasta "instancias"
    lista_instancias = os.listdir(pasta_instancias)

    # Inicialização de 'qtd_arquivos_leitura', que representa a quantidade de instâncias utilizadas;
    qtd_arquivos_leitura = 0

    # Inicialização dos arquivos de leitura.
    arquivo_leitura = [Arquivo_scp(id=i) for i in range(len(lista_instancias)+1)]

    for nome_arquivo in lista_instancias:
        if nome_arquivo.endswith(".txt"):
            caminho_completo = os.path.join(pasta_instancias, nome_arquivo)
            arquivo_leitura[qtd_arquivos_leitura].caminho = caminho_completo
            arquivo_leitura[qtd_arquivos_leitura].nome = nome_arquivo
            qtd_arquivos_leitura += 1

    # Definição do 'arquivo' de teste
    arquivo_leitura[qtd_arquivos_leitura].nome = "TESTE"

    # Tempo máximo de excução em milisegundos (milissegundos -> segundos/1000).
    tempo_max = 1000     
    
    # Avalia se o programa lerá o arquivo especificado em "nome" (teste=0) ou executará um teste com a matriz "matriz" (teste=1).
    teste = 1

    # Avalia se o resultado do solver será escrito no 'arquivo_escrita'.
    escrita = 1

    # Define a saida de uma descrição detalhada dos subconjuntos escolhidos e elementos cobertos (opicional)
    output_padrao_completo = 1

    # Define a saida de uma descrição detalhada do funcionamento do solver (opicional)
    output_branch_and_bound = 0

    # Total de linhas da matriz (calculado automaticamente para as instancias, uso predefinido apenas para testes)   
    arquivo_leitura[qtd_arquivos_leitura].linhas = 5

    # Total de colunas da matriz (calculado automaticamente para as instancias, uso predefinido apenas para testes)
    arquivo_leitura[qtd_arquivos_leitura].colunas = 5

    #Matriz utilizada em testes (reescrita ao ler um arquivo)
    matriz = [[1, 0, 0, 0, 1],  
              [0, 1, 0, 0, 0],  
              [1, 1, 0, 0, 0],  
              [1, 0, 0, 0, 1],  
              [0, 0, 1, 0, 0]]
    

    if not teste:
        # Define o ID do 'arquivo_leitura' de testes para a quantidade de arquivos definidos anteriormente, utilizado para a automatização da execução.
        arquivo_leitura[qtd_arquivos_leitura].id = qtd_arquivos_leitura

    else:
        # Define o ID do 'arquivo_leitura' de testes para a 1, utilizado para a automatização da execução.
        arquivo_leitura[qtd_arquivos_leitura].id = -1

    # Execução do solver
    executa_solver(arquivo_leitura, matriz, tempo_max, output_branch_and_bound, output_padrao_completo, escrita, arquivo_escrita)

if __name__ == "__main__":
    main()  
