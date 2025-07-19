from ortools.linear_solver import pywraplp
import sys
import os
import re
from typing import List

<<<<<<< HEAD
# LEITURA, RESOLUÇÃO E ESCRITA DE INSTÂNCIAS SCP

# Classe que representa um subconjunto, com seu ID, peso, elementos cobertos e variável de decisão
=======

# Classe que representa um subconjunto com seu ID, peso, elementos cobertos e variável de decisão
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
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
<<<<<<< HEAD
        self.num_coberturas = 0
=======
        self.num_coberturas      = 0
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
        # Variáveis y
        self.var_cobertura_unica = 0
        # Variáveis z
        self.var_cobertura_total = 0

<<<<<<< HEAD
# Classe que representa um arquivo scp.txt
=======
# Classe que representa um arquivo de instancia do SCP (Set Covering Problem)
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
class Arquivo_scp:
    def __init__(self, id):
        self.id = id
        self.arquivo = 0
        self.caminho = []
        self.nome = []
        self.linhas = 0
        self.colunas = 0
        self.conjuntos_escolhidos = []

class Tempo_execução:
    def __init__(self):
<<<<<<< HEAD
        self.cpu_time_solver = 0
        self.wall_time_solver = 0
        self.total_wall_time = 0
        self.total_cpu_time = 0

# Função que abre o arquivo de entrada e lê todas as linhas
# Retorna uma lista de strings com o conteúdo do arquivo
# Se não conseguir abrir, encerra o programa
=======
        self.cpu_time_solver    = 0
        self.wall_time_solver   = 0
        self.total_wall_time    = 0
        self.total_cpu_time     = 0

# Le o arquivo de instancia e retorna uma lista de strings
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
def abrir_arquivo(arquivo_leitura):
        try:
            with open(arquivo_leitura.caminho, "r") as arquivo_leitura.arquivo:
                linhas_arquivo = arquivo_leitura.arquivo.readlines()

                # Leitura do cabeçalho do 'arquivo_leitura'
                arquivo_leitura.linhas, arquivo_leitura.colunas = ler_cabecalho(linhas_arquivo)

                # Leitura do conteúdo do 'arquivo_leitura'
                subconjuntos, matriz, elementos = ler_conteudo(arquivo_leitura.linhas, arquivo_leitura.colunas, linhas_arquivo)

            print("\nO arquivo foi aberto com sucesso!")
            return subconjuntos, matriz, elementos
        except FileNotFoundError:
            print("\nERRO! O arquivo não foi aberto!")
            exit(1)
        
<<<<<<< HEAD

# Função que lê a primeira linha do arquivo contendo:
# - número de linhas (elementos);
# - número de colunas (subconjuntos);
# Retorna os dois valores como inteiros
=======
# Lê a primeira linha da instancia contendo:
    # - número de linhas (elementos);
    # - número de colunas (subconjuntos);
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
def ler_cabecalho(linhas_arquivo):
    primeira_linha = linhas_arquivo[0].strip().split()
    linhas = int(primeira_linha[0])
    colunas = int(primeira_linha[1])
    return linhas, colunas

<<<<<<< HEAD

# Lê o conteudo da instância, armazenado no 'linhas_arquivo', contendo:
# - pesos dos subconjuntos;
# - quantidades de cobertura de cada elemento;
# - subconjuntos que cobrem cada elemento;
# Retorna: Lista de subconjuntos, Lista de elementos e Matriz de cobertura, nesta ordem.
def ler_conteudo(l, c, linhas_arquivo):
    # Inicializa variaveis:

=======
# Lê o conteudo da instância, armazenado no 'linhas_arquivo', contendo:
    # - pesos dos subconjuntos;
    # - quantidades de cobertura de cada elemento;
    # - subconjuntos que cobrem cada elemento;
# Retorna: Lista de subconjuntos, Lista de elementos e Matriz de cobertura, nesta ordem.
def ler_conteudo(l, c, linhas_arquivo):
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
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

<<<<<<< HEAD
    # Variáveis de auxílio
=======
    # Auxiliares
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
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
        
<<<<<<< HEAD

    # Leitura das coberturas de cada elemento
    # 'i' representa o numeros de elementos lidos
=======
    # Leitura das coberturas de cada elemento
        # 'i' representa o numeros de elementos lidos
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
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
        
<<<<<<< HEAD
        # Avança para a próxima linha]
=======
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
        linha_atual += 1
        
    return subconjuntos, elementos, matriz

<<<<<<< HEAD
# Função executada para a gravação das execuções do solver no 'arquivo_escrita', definido na main()
=======
def converter_tempo(segundos_totais):
    horas = int(segundos_totais / 3600)
    minutos = int((segundos_totais % 3600) / 60)
    segundos = int(segundos_totais % 60)
    milissegundos = int(round((segundos_totais - int(segundos_totais)) * 1000))

    return horas, minutos, segundos, milissegundos

# Grava as execuções do solver no 'arquivo_escrita' definido na main()
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
def escreve_teste(arquivo_leitura:Arquivo_scp, elementos:List[Elemento], subconjuntos: List[Subconjunto], matriz, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo,  media_cobertura_total, tempo_execucao, padrao_log):

    if arquivo_leitura.id == 0:
        tipo_leitura = "w"
    else:
        tipo_leitura = "a"

<<<<<<< HEAD
    # Abertura do arquivo de escrita
    try:
        with open(arquivo_escrita, tipo_leitura, encoding="utf-8") as escrita:
            # Alterna a escrita inicial dependendo se for um teste ou não

=======
    try:
        with open(arquivo_escrita, tipo_leitura, encoding="utf-8") as escrita:
            # Alterna a escrita inicial dependendo se for um teste ou não
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
            if arquivo_leitura.nome == "TESTE":
                escrita.write(f"\n\n\n\n\t*****TESTE*****")
                escrita.write("\n\nFunção Objetiva:")
            else:
                escrita.write("\n\n\n\nFunção Objetiva:")
<<<<<<< HEAD
            # Elementos centrais do solver 
=======
        
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
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

<<<<<<< HEAD

=======
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
            if media_cobertura_total >= 1:
                if  media_cobertura_total == 1:
                    escrita.write("\n\nSolucao otima encontrada!")
                else:
                    escrita.write("\n\nUma solucao factivel foi encontrada.")
        
                if padrao_log:
<<<<<<< HEAD
                    # Iniciação variáveis do log

                    # Status da solução
                    status = padrao_log.group("status")

                    # Limitante superior (LS) do Branch-and-Bound (Branch-and-cut nesse caso)
=======
                    # Status da solução
                    status = padrao_log.group("status")

                    # Limitante superior (LS) do Branch-and-cut
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
                    limitante_superior = float(padrao_log.group("LS")) if padrao_log.group("LS") else 0.0 

                    # Gap de integralidade -> Diferença percentual entre o valor da função objetivo e o limitante superior
                    gap = abs(float(padrao_log.group("gap"))) if padrao_log.group("gap") else 0.0

<<<<<<< HEAD
                    # Número de nós criados pelo Branch-and-Bound (Branch-and-cut nesse caso)
=======
                    # Número de nós criados pelo Branch-and-cut
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
                    num_nos = padrao_log.group("nos") if padrao_log.group("nos") else 0.0

                    # Número de iterações realizadas pelo Solver
                    num_iteracoes = padrao_log.group("iteracoes") if padrao_log.group("iteracoes") else 0.0

                    # Tempo de execução em cpu do solver (Tempo efetivo do software sendo processado) 
                    tempo_execucao.cpu_time_solver = float(padrao_log.group("cpu"))

                    # Tempo de wallclock do solver (Tempo real do software sendo processado)
                    tempo_execucao.wall_time_solver = float(padrao_log.group("wall"))

                    # Tempo de execução em cpu no total (Tempo efetivo do software sendo processado, incluindo alocação de variáveis, pré-processamento, entre outros.) 
                    tempo_execucao.total_cpu_time = float(padrao_log.group("total_cpu"))

                    # Tempo de wallclock do solver (Tempo real do software sendo processado), incluindo alocação de variáveis, pré-processamento, entre outros.) 
                    tempo_execucao.total_wall_time = float(padrao_log.group("total_wall"))

                    escrita.write(f"\n\nStatus: {status}")
                    escrita.write(f"\nFunção Objetivo: {funcao_objetivo:.2f}")
                    if limitante_superior > 0:
                        escrita.write(f"\nLimitante Superior: {limitante_superior:.2f}")
                    escrita.write(f"\nGap de integralidade: {(gap * 100):.2f}%")
                    escrita.write(f"\nNúmero de nós gerados: {num_nos}")
                    escrita.write(f"\nNúmero de iterações: {num_iteracoes}")
                    escrita.write(f"\nTime (CPU seconds): {tempo_execucao.cpu_time_solver:.2f}")
                    escrita.write(f"\nTime (Wallclock seconds): {tempo_execucao.wall_time_solver:.2f}")
                    escrita.write(f"\nTotal time (CPU seconds): {tempo_execucao.total_cpu_time:.2f}")
                    escrita.write(f"\nTotal time (Wallclock seconds): {tempo_execucao.total_wall_time:.2f}")

                    h_c, m_c, s_c, ms_c = converter_tempo(tempo_execucao.total_cpu_time)
                    h_w, m_w, s_w, ms_w = converter_tempo(tempo_execucao.total_wall_time)

                    escrita.write(f"\n\nTempo em horas:")
                    escrita.write(f"\nTempo de execução em horas (CPU): {h_c}h {m_c}min {s_c}s {ms_c}ms")
                    escrita.write(f"\nTempo total de execução em horas (Wallclock): {h_w}h {m_w}min {s_w}s {ms_w}ms")
                else:
                    escrita.write("\n\nERRO AO LER O LOG")

                escrita.write("\n\nConjuntos selecionados:")

                for j in range(arquivo_leitura.colunas):
                    if subconjuntos[j].var_escolha > 0.5:
                        escrita.write(f"\n- Conjunto S {j+1}\n    Elementos cobertos: {subconjuntos[j].elementos_cobertos}")

                escrita.write("\n\nDetalhes da cobertura por elemento:")
                
                for i in range(arquivo_leitura.linhas):
                    coberto_unicamente = "Sim" if elementos[i].var_cobertura_unica > 0.5 else "Não"
                    escrita.write(f'\nElemento {str(i+1)}: coberto {str(elementos[i].var_cobertura_total)} vez(es). Cobertura unica: {coberto_unicamente}')

                escrita.write(f"\nCobertura media dos elementos: {media_cobertura_total:.2f}")

            else:
                escrita.write("\n\nO problema nao tem solucao.")
                escrita.write(f"\n\nTime (CPU seconds): {tempo_execucao.cpu_time_solver:.2f}")
                escrita.write(f"\nTime (Wallclock seconds): {tempo_execucao.wall_time_solver:.2f}")
                escrita.write(f"\nTotal time (CPU seconds): {tempo_execucao.total_cpu_time:.2f}")
                escrita.write(f"\nTotal time (Wallclock seconds): {tempo_execucao.total_wall_time:.2f}")

                h_c, m_c, s_c, ms_c = converter_tempo(tempo_execucao.total_cpu_time)
                h_w, m_w, s_w, ms_w = converter_tempo(tempo_execucao.total_wall_time)

                escrita.write(f"\n\nTempo em horas:")
                escrita.write(f"\nTempo de execução em horas (CPU): {h_c}h {m_c}min {s_c}s {ms_c}ms")
                escrita.write(f"\nTempo total de execução em horas (Wallclock): {h_w}h {m_w}min {s_w}s {ms_w}ms")


    except FileNotFoundError:
        print("\nERRO! O arquivo de escrita não foi aberto!")
        exit(1)

<<<<<<< HEAD
def converter_tempo(segundos_totais):
    horas = int(segundos_totais / 3600)
    minutos = int((segundos_totais % 3600) / 60)
    segundos = int(segundos_totais % 60)
    milissegundos = int(round((segundos_totais - int(segundos_totais)) * 1000))

    return horas, minutos, segundos, milissegundos

def decoder(cromossomo, matriz, M):
    m = len(cromossomo)
    n = len(matriz)
    x = [1 if gene <= 0.5 else 0 for gene in cromossomo]

# Executa o solver
def executa_solver(arquivo_leitura: List[Arquivo_scp], matriz, tempo_max, output_padrao_completo, escrita, arquivo_escrita):
    # Inicialização das variaveis:

=======
# Executa o solver
def executa_solver(arquivo_leitura: List[Arquivo_scp], matriz, tempo_max, output_padrao_completo, escrita, arquivo_escrita):
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
    # Quantidade de arquivos no vetor arquivo leitura, menos o 'TESTE'
    qtd_arquivos = arquivo_leitura[len(arquivo_leitura)-1].id

    #Inicialização da média da cobertura total de um elemento
    media_cobertura_total = 0

    # Vetor  que armazena o tempo de execução de cada instância.
    tempo_execucao = [Tempo_execução() for _ in range(len(arquivo_leitura))]

    # Define o caminho da subpasta
    subpasta = "logs"

    # Cria a subpasta se ela ainda não existir
    os.makedirs(subpasta, exist_ok=True)

    if escrita:
        escrita_permitida = 1
        try:
            if os.path.getsize(arquivo_escrita) > 0:
                while True:
                    resposta = input("Deseja sobrescrever o arquivo atual? (s/n): ").strip().lower()
                    if resposta in ["s", "n"]:
                        break
                    print("Por favor, digite 's' para sim ou 'n' para não.")
                if resposta == "s":
                    escrita_permitida = 1
                else:
                    escrita_permitida = 0
            else:
                escrita_permitida = 0
        except FileNotFoundError:
            escrita_permitida = 1
    else:
        escrita_permitida = 0
    
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

<<<<<<< HEAD

=======
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
    while qtd < qtd_arquivos:
        i = 0
        j = 0

<<<<<<< HEAD
         # Arquivo que armazenará o log de cada execução
=======
        # Arquivo que armazenará o log de cada execução
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
        caminho_log = "cbc_log_"

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

            # Arquivo que armazenará o log de cada execução
            caminho_log += 'teste.txt'
        else:
            # Abertura do 'arquivo_leitura'
            subconjuntos, elementos, matriz  = abrir_arquivo(arquivo_leitura[qtd])

            caminho_log += arquivo_leitura[qtd].nome
            
            print(f'\n\n{qtd+1})')
            
        # Caminho completo do arquivo dentro da subpasta 'logs'
        caminho_log = os.path.join(subpasta, caminho_log)

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

<<<<<<< HEAD
        # Define a saida de um output muito detalhado do 'branch-and-bound' ('branch-and-cut' no caso do solver CBC)
=======
        # Define a saida de um output muito detalhado do branch-and-cut
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
        solver.EnableOutput()

        versao_solver = solver.SolverVersion()
        print("\nResolvendo com o solver", versao_solver)

        # Cria o arquivo de log e redireciona a saída do solver para ele
        with open(caminho_log, "w", encoding="utf-8") as arquivo_log:
<<<<<<< HEAD
            # Salva os descritores originais de stdout e stderr
            stdout_original= os.dup(1)
            stderr_original = os.dup(2)

            # Redireciona os descritores para o arquivo
            os.dup2(arquivo_log.fileno(), sys.stdout.fileno())
            os.dup2(arquivo_log.fileno(), sys.stderr.fileno())

            try:
                # Execução do solver com saída redirecionada
                resultado = solver.Solve()
            finally:
                # Restaura os descritores originais
=======
            try:
                # Salva os descritores originais
                stdout_original = os.dup(sys.stdout.fileno())
                stderr_original = os.dup(sys.stderr.fileno())

                os.dup2(arquivo_log.fileno(), sys.stdout.fileno())
                os.dup2(arquivo_log.fileno(), sys.stderr.fileno())

                # Roda o solver com saída redirecionada
                resultado = solver.Solve()

            finally:
                # Restaura stdout e stderr
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
                os.dup2(stdout_original, sys.stdout.fileno())
                os.dup2(stderr_original, sys.stderr.fileno())
                os.close(stdout_original)
                os.close(stderr_original)

        # Leituta do log gerado na execução do solver
        with open(caminho_log, "r", encoding="utf-8") as f:
            log_content = f.read()
            indice = log_content.find("Result - ")
            trecho_dados = log_content[indice:] 

        if indice != -1:
<<<<<<< HEAD
        # Leituta do log gerado na execução do solver
=======
            # Leituta do log gerado na execução do solver
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
            padrao_log = re.search(r"Result - (?P<status>.*)\n+(?:No feasible solution found\n+)?(?:Objective value:\s+(?P<f_objetivo>\d*\.?\d+)\n+)?(?:Upper bound:\s+(?P<LS>\d*\.?\d+)\n+)?(?:Gap:\s+(?P<gap>-?\d*\.?\d+)\n+)?(?:Enumerated nodes:\s+(?P<nos>\d+)\n+)?(?:Total iterations:\s+(?P<iteracoes>\d+)\n+)?Time \(CPU seconds\):\s+(?P<cpu>\d*\.?\d+)\n+Time \(Wallclock seconds\):\s+(?P<wall>\d*\.?\d+)\n+Total time \(CPU seconds\):\s+(?P<total_cpu>\d*\.?\d+)\s+\(Wallclock seconds\):\s+(?P<total_wall>\d*\.?\d+)", trecho_dados)
                            
            # Status da solução
            status = padrao_log.group("status")

            # Valor da função objetivo
            funcao_objetivo = funcao_objetivo.Value()

<<<<<<< HEAD
            # Limitante superior (LS) do Branch-and-Bound (Branch-and-cut nesse caso)
=======
            # Limitante superior (LS) do Branch-and-cut
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
            limitante_superior = float(padrao_log.group("LS")) if padrao_log.group("LS") else 0.0 

            # Gap de integralidade -> Diferença percentual entre o valor da função objetivo e o limitante superior
            gap = abs(float(padrao_log.group("gap"))) if padrao_log.group("gap") else 0.0

<<<<<<< HEAD
            # Número de nós criados pelo Branch-and-Bound (Branch-and-cut nesse caso)
=======
            # Número de nós criados pelo Branch-and-cut
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
            num_nos = padrao_log.group("nos") if padrao_log.group("nos") else 0.0

            # Número de iterações realizadas pelo Solver
            num_iteracoes = padrao_log.group("iteracoes") if padrao_log.group("iteracoes") else 0.0

            # Tempo de execução em cpu do solver (Tempo efetivo do software sendo processado) 
            tempo_execucao[qtd].cpu_time_solver = float(padrao_log.group("cpu"))

            # Tempo de wallclock do solver (Tempo real do software sendo processado)
            tempo_execucao[qtd].wall_time_solver = float(padrao_log.group("wall"))

            # Tempo de execução em cpu no total (Tempo efetivo do software sendo processado, incluindo alocação de variáveis, pré-processamento, entre outros.) 
            tempo_execucao[qtd].total_cpu_time = float(padrao_log.group("total_cpu"))

            # Tempo de wallclock do solver (Tempo real do software sendo processado), incluindo alocação de variáveis, pré-processamento, entre outros.) 
            tempo_execucao[qtd].total_wall_time = float(padrao_log.group("total_wall"))
        else:
            padrao_log = None

        if resultado == pywraplp.Solver.OPTIMAL or resultado == pywraplp.Solver.FEASIBLE:
            if resultado == pywraplp.Solver.OPTIMAL:
                print('\nSolução ótima encontrada!')
            else:
                print('\nUma solução factível foi encontrada.')

            if padrao_log:
                print("\nStatus:", status)
                print(f"Função Objetivo: {funcao_objetivo:.2f}")
                if limitante_superior > 0:
                    print(f"Limitante Superior: {limitante_superior:.2f}") 
                print(f"Gap: {(gap * 100):.2f}%")
                print(f"Número de nós gerados: {num_nos}")
                print(f"Número de iterações: {num_iteracoes}")
                print(f"Time (CPU seconds): {tempo_execucao[qtd].cpu_time_solver:.2f}")
                print(f"Time (Wallclock seconds): {tempo_execucao[qtd].wall_time_solver:.2f}")
                print(f"Total time (CPU seconds): {tempo_execucao[qtd].total_cpu_time:.2f}")
                print(f"Total time (Wallclock seconds): {tempo_execucao[qtd].total_wall_time:.2f}")
            else:
                print("ERRO AO LER O LOG GERADO")    

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

<<<<<<< HEAD
            print(f"\nCobertura média dos elementos: {media_cobertura_total:.2f}")
=======
            print(f"\n\nCobertura média dos elementos: {media_cobertura_total:.2f}")
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
        else:
            print('\nO problema não tem solução.')
            funcao_objetivo = 0
            media_cobertura_total = 0    
            print(f"\n⚙️  Tempo CPU usado na execução do solver (CPU seconds): {tempo_execucao[qtd].cpu_time_solver:.3f} s")
            print(f"⏱️  Tempo real decorrido na execução do solver (Wallclock seconds): {tempo_execucao[qtd].wall_time_solver:.3f} s")
            print(f"\n⚙️  Tempo total de CPU usado (CPU seconds): {tempo_execucao[qtd].total_cpu_time:.3f} s")
            print(f"⏱️  Tempo real total decorrido (Wallclock seconds): {tempo_execucao[qtd].total_wall_time:.3f} s")

        if escrita_permitida:
            # Verifica se o TESTE está ativado
            if qtd == len(arquivo_leitura) - 1:
                arquivo_escrita = "testes.txt"
                
<<<<<<< HEAD
            # Grava o retorno do solver no 'arquivo_escrita'
=======
            # Grava o retorno do solver 
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
            escreve_teste(arquivo_leitura[qtd], elementos, subconjuntos, matriz, arquivo_escrita, num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao[qtd], padrao_log)

        qtd += 1

    # Verifica se mais de 1 execução foi realizada para a impressão da soma dos tempos de execução
    if not (arquivo_leitura[qtd-1].nome == "TESTE" or qtd_arquivos == 1):
        tempo_total_cpu = sum(tempo_execucao[i].total_cpu_time for i in range(len(tempo_execucao) - 1))
        tempo_total_wall = sum(tempo_execucao[i].total_wall_time for i in range(len(tempo_execucao) - 1))

        h_c, m_c, s_c, ms_c = converter_tempo(tempo_total_cpu)
        h_w, m_w, s_w, ms_w = converter_tempo(tempo_total_wall)

        print(f"\nTempo em segundos:")
        print(f"⚙️  Tempo total de execução da(s) {qtd} instância(s) (CPU seconds): {tempo_total_cpu:.3f} segundos")
        print(f"⏱️  Tempo total de execução da(s) {qtd} instância(s) (Wallclock seconds): {tempo_total_wall:.3f} segundos")
        
        print(f"\nTempo em horas:")
        print(f"⚙️  Tempo total de execução da(s) {qtd} instância(s) (CPU seconds): {h_c}h {m_c}min {s_c}s {ms_c}ms")
        print(f"⏱️  Tempo total de execução da(s) {qtd} instância(s) (Wallclock seconds): {h_w}h {m_w}min {s_w}s {ms_w}ms")

        if escrita_permitida:
            with open(arquivo_escrita, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"\n\nTempo em segundos:")
                arquivo.write(f"\nTempo total de execução da(s) {qtd} instância(s) (CPU seconds): {tempo_total_cpu:.3f} segundos")
                arquivo.write(f"\nTempo total de execução da(s) {qtd} instância(s) (Wallclock seconds): {tempo_total_wall:.3f} segundos")                

                arquivo.write(f"\n\nTempo em horas:")
                arquivo.write(f"\nTempo total de execução da(s) {qtd} instância(s) (CPU seconds): {h_c}h {m_c}min {s_c}s {ms_c}ms")
                arquivo.write(f"\nTempo total de execução da(s) {qtd} instância(s) (Wallclock seconds): {h_w}h {m_w}min {s_w}s {ms_w}ms")

    return

def main():
<<<<<<< HEAD
    # Parametros básicos para a execução:
    
    # Nome do arquivo no qual o resultado dos testes poderá ser escrito (opcional).
=======
    # Nome do arquivo no qual o resultado serão escritos.
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152
    arquivo_escrita = "resultados.txt"

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
    teste = 0

    # Avalia se o resultado do solver será escrito no 'arquivo_escrita'.
    escrita = 0

    # Define a saida de uma descrição detalhada, no terminal, dos subconjuntos escolhidos e elementos cobertos (opicional)
<<<<<<< HEAD
    output_padrao_completo = 1
=======
    output_padrao_completo = 0
>>>>>>> e00120d6938018a3001b9074d41b78a4929a6152

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
    executa_solver(arquivo_leitura, matriz, tempo_max, output_padrao_completo, escrita, arquivo_escrita)

if __name__ == "__main__":
    main()  
