from brkga_mp_ipr.enums import ParsingEnum, Sense
from brkga_mp_ipr.types_io import load_configuration
from brkga_mp_ipr.algorithm import BrkgaMpIpr, BrkgaParams
import time
import math
import random
from copy import deepcopy
import os
import re
from typing import List

# LEITURA, RESOLUÇÃO E ESCRITA DE INSTÂNCIAS SCP

# Classe que representa um subconjunto, com seu ID, peso, elementos cobertos e variável de decisão
class Subconjunto:
    def __init__(self, id):
        self.id = id
        self.peso = 0
        self.elementos_cobertos = []
        self.prioridade = 0
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

class StopRule(ParsingEnum):

    GENERATIONS = 0
    TARGET = 1
    IMPROVEMENT = 2

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

            print("\n\n\nO arquivo foi aberto com sucesso!")
            return subconjuntos, matriz, elementos
        except FileNotFoundError:
            print("\n\n\nERRO! O arquivo não foi aberto!")
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
    elementos = [Elemento(id=i+1) for i in range(l)]

    # Lista dos subconjuntos(colunas)
    subconjuntos = [Subconjunto(id=j+1) for j in range(c)]

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

def escreve_cabecalho(qtd_arquivos, arquivo_escrita, config_file, parametros):
    # Abertura do arquivo de escrita
    try:
        with open(arquivo_escrita, "w" ,encoding="utf-8") as escrita:
            # Alterna a escrita inicial dependendo se for um teste ou não
            
            if qtd_arquivos == -1:
                escrita.write(f"\t*****TESTE*****")


            escrita.write("Função Objetiva:")

            # Elementos centrais do solver 
            escrita.write("\n                   Max ∑ yᵢ                             para i=1 até Linhas")
            escrita.write("\nSujeito a:") 
            escrita.write("\n                   ∑ aᵢⱼ·xⱼ = zᵢ                        ∀i, 1 ≤ i ≤ Linhas, para j=1 até Colunas")
            escrita.write("\n                   yᵢ ≤ zᵢ                              ∀i, 1 ≤ i ≤ Linhas")
            escrita.write("\n                   (M - 1)yᵢ + zᵢ ≤ M                   ∀i, 1 ≤ i ≤ Linhas")
            escrita.write("\n                   y ∈ {0,1}ⁿ, z ∈ ℤⁿ, x ∈ {0,1}ᵐ")

            escrita.write(f"\n\nArquivo de configuração: {config_file}")
            escrita.write(f"\n\nParâmetros do algoritmo:")

            output_string = ""

            for name, value in vars(parametros[0]).items():
                output_string += f"\n>  -{name} {value}"
            for name, value in vars(parametros[1]).items():
                output_string += f"\n>  -{name} {value}"

            escrita.write(output_string)
    except FileNotFoundError:
        print("\nERRO! O arquivo de escrita não foi aberto!")
        exit(1)

# Função executada para a gravação das execuções do solver no 'arquivo_escrita', definido na main()
def escreve_teste(arquivo_leitura:Arquivo_scp, subconjuntos: List[Subconjunto], elementos:List[Elemento], arquivo_escrita, padrao_resposta,  media_cobertura_total, tempo_execucao):
    # Abertura do arquivo de escrita
    try:
        with open(arquivo_escrita, "a", encoding="utf-8") as escrita:
            # Alterna a escrita inicial dependendo se for um teste ou não

            escrita.write(f"\n\n\n\nInstância: {arquivo_leitura.nome}")
            escrita.write(f'\nElementos = {arquivo_leitura.linhas}')
            escrita.write(f'\nSubconjutos = {arquivo_leitura.colunas}')

            escrita.write(f"\n\nSeed: {padrao_resposta[0]}")
            escrita.write(f"\nTempo máximo de execução (s): {tempo_execucao}")

            escrita.write(f"\n\n\nConstruindo solver BRKGA...")

            escrita.write(f"\n\nGenerando sequência inicial...")

            escrita.write(f"\n\nCusto inicial: {padrao_resposta[14][0]}")
            escrita.write(f"\nCromossomo inicial: {padrao_resposta[14][1]}")

            escrita.write(f"\n\nIter | Resp | Temp")

            for i in padrao_resposta[1]:
                escrita.write(f"\n* {i[0]} | {i[1]:.0f} | {i[2]:.2f}")

            if media_cobertura_total > 0:
                if  media_cobertura_total == 1:
                    escrita.write("\n\nSolucao otima encontrada!")
                else:
                    escrita.write("\n\nUma solucao factivel foi encontrada.")

                escrita.write(f"\nMelhor resultado:                      {padrao_resposta[1][len(padrao_resposta[1])-1][1]:.0f}")
                escrita.write(f"\nGAP integralidade:                     {padrao_resposta[10]:.2f}%")
                escrita.write(f"\nGAP proporcional à solução encontrada: {padrao_resposta[11]:.2f}%")
                escrita.write(f"\nPeso total:                           {padrao_resposta[3]}")
                escrita.write(f"\nQuantidad de nós:                      {padrao_resposta[2]}")
                escrita.write(f"\nTotal de iterações:                    {padrao_resposta[9]}")
                escrita.write(f"\nCobertura media dos elementos:         {media_cobertura_total:.2f}")
                escrita.write(f"\nSeed:                                  {padrao_resposta[0]}")
           
                escrita.write(f"\nTempo em segundos:                     {tempo_execucao:.2f}s")
                
                h, m, s, ms = converter_tempo(tempo_execucao)

                escrita.write(f"\nTempo em horas:                        {h}h {m}min {s}s {ms}ms")

                escrita.write(f"\nMaior número de iterações sem melhora: {padrao_resposta[6]}")
                escrita.write(f"\nÚltima iteração de melhora:            {padrao_resposta[7]}")
                escrita.write(f"\nÚltimo momento de melhora:             {padrao_resposta[8]:.2f}s")

                escrita.write("\n\nConjuntos selecionados:")

                for j in padrao_resposta[4]:
                    escrita.write(f"\n- Conjunto S {j+1}\n    Elementos cobertos: {subconjuntos[j-1].elementos_cobertos}")

                escrita.write("\n\nDetalhes da cobertura por elemento:")
                
                for e in elementos:
                    coberto_unicamente = "Sim" if e.var_cobertura_unica == 1 else "Não"
                    escrita.write(f'\nElemento {str(e.id)}: coberto {str(e.var_cobertura_total)} vez(es). Cobertura unica: {coberto_unicamente}')

            else:
                escrita.write('\n\nO problema não tem solução.')
                escrita.write(f"\n\nTempo em segundos: {tempo_execucao:.2f};")

                h, m, s, ms = converter_tempo(tempo_execucao)

                escrita.write(f"\nTempo em horas: {h}h {m}min {s}s {ms}ms")

    except FileNotFoundError:
        print("\nERRO! O arquivo de escrita não foi aberto!")
        exit(1)

def converter_tempo(segundos_totais):
    horas = int(segundos_totais / 3600)
    minutos = int((segundos_totais % 3600) / 60)
    segundos = int(segundos_totais % 60)
    milissegundos = int(round((segundos_totais - int(segundos_totais)) * 1000))

    return horas, minutos, segundos, milissegundos

def Atualiza_Pesos(subconjuntos, elementos, fim):

    for s in subconjuntos:
        peso = 0
        for i in s.elementos_cobertos:
            if elementos[i-1].var_cobertura_total == 0:
                peso += 1
            elif elementos[i-1].var_cobertura_total == 1:
                if fim:
                    peso -= 1
                else:
                    peso -= len(elementos)
            # caso contrário, peso não muda
        s.peso = peso


def Encontra_max_min(subconjuntos):
    pesos_positivos = [s.peso for s in subconjuntos if s.var_escolha == 0 and s.peso > 0]
    if not pesos_positivos:
        return None, None, 0
    return max(pesos_positivos), min(pesos_positivos), len(pesos_positivos)

def Constroi_RCL(subconjuntos, maximo, minimo, alpha):
    threshold = minimo + (maximo - minimo) * alpha
    rcl = [s for s in subconjuntos if s.var_escolha == 0 and s.peso >= threshold]
    return rcl

def Seleciona_conjunto(rcl):
    return max(rcl, key=lambda s: s.prioridade) if rcl else None


def Busca_Local(subconjuntos, elementos):
    melhorou = True
    qtd_melhora = 0            

    while melhorou:
        
        melhorou = False
        solucao_atual = []
        conjuntos_possiveis = []

        for s in subconjuntos:
            if s.var_escolha == 1:
                solucao_atual.append(s)
            else:
                conjuntos_possiveis.append(s)

        conjuntos_possiveis = sorted(conjuntos_possiveis, key=lambda s: s.prioridade, reverse=True) if conjuntos_possiveis is not None else None

        for s in solucao_atual:
            Atualiza_Pesos(subconjuntos, elementos, 1)
            ganho_antes = sum(1 for e in elementos if e.var_cobertura_total == 1)

            # Simula remoção de s
            elementos_afetados = []
            for i in s.elementos_cobertos:
                e = elementos[i - 1]
                if e.var_cobertura_total == 1:
                    elementos_afetados.append(i)

            # Se não há elementos com cobertura única perdida, continue
            if not elementos_afetados:
                continue

            # Testa subconjuntos fora da solução que podem cobrir os elementos afetados
            for s_sub in conjuntos_possiveis:
                if s_sub.var_escolha == 1 or s_sub == s:
                    continue
                
                if all(i in s_sub.elementos_cobertos for i in elementos_afetados) and s_sub.peso >= s.peso:

                    if s_sub.peso == s.peso:
                        if len(s.elementos_cobertos) < len(s_sub.elementos_cobertos):
                            continue
                        else:
                            if s.prioridade >= s_sub.prioridade:
                                continue

                    # Aplica a substituição
                    for i in s.elementos_cobertos:
                        elementos[i - 1].var_cobertura_total -= 1

                    for i in s_sub.elementos_cobertos:
                        elementos[i - 1].var_cobertura_total += 1

                    #ganho_depois = sum(1 for e in elementos if e.num_coberturas == 1)
                  
                    s.var_escolha = 0
                    s_sub.var_escolha = 1
                       
                    # Atualiza as coberturas únicas
                    for e in elementos:
                        z = e.var_cobertura_total
                        e.var_cobertura_unica = 1 if z == 1 else 0

                    melhorou = True
                    qtd_melhora += 1 

                    break
                
                # Avalia se adicionar s_sub melhora a cobertura única
                if s_sub.peso > 0:
        
                    # Simula adição
                    for i in s_sub.elementos_cobertos:
                        elementos[i - 1].var_cobertura_total += 1
                    ganho_depois = sum(1 for e in elementos if e.var_cobertura_total == 1)
                    
                    if ganho_depois > ganho_antes:
                        s_sub.var_escolha = 1
                            
                        for e in elementos:
                            z = e.var_cobertura_total
                            e.var_cobertura_unica = 1 if z == 1 else 0   
                            
                        melhorou = True
                        qtd_melhora += 1 

                        break
                    else:
                        for i in s_sub.elementos_cobertos:
                            elementos[i - 1].var_cobertura_total -= 1
            if melhorou:
                break 

    solucao_atual = []
    for s in subconjuntos:
        if s.var_escolha == 1:
            solucao_atual.append(s)
    return solucao_atual

def greedy(subconjuntos, elementos, cromossomos):

    for i, c in enumerate(cromossomos):
        subconjuntos[i].prioridade = c
    
    maximo = 0
    minimo = len(elementos)

    fim = 0
    unicos = 0
    alpha = 0.1
    Atualiza_Pesos(subconjuntos, elementos, fim)

    while True:
            
        maximo, minimo, disponiveis = Encontra_max_min(subconjuntos)
        if disponiveis == 0:
            break

        rcl = Constroi_RCL(subconjuntos, maximo, minimo, alpha)
        escolhido = Seleciona_conjunto(rcl)
        if escolhido is None:
            break

        escolhido.var_escolha = 1
        for i in escolhido.elementos_cobertos:
            elementos[i-1].var_cobertura_total += 1

        Atualiza_Pesos(subconjuntos, elementos, fim)

    solucao = Busca_Local(subconjuntos, elementos)

    for s in solucao:
        for i in s.elementos_cobertos:
            if elementos[i-1].var_cobertura_total == 1:
                unicos += 1

    return unicos

# Decodificador BRKGA
class SCPDecoder():
    def __init__(self, subconjuntos: List[Subconjunto], elementos: List[Elemento], M, alpha):
        self.subconjuntos = subconjuntos
        self.elementos = elementos
        self.M = M        
        self.alpha = alpha
        self.subconjuntos_resposta = subconjuntos
        self.elementos_resposta = elementos
        self.melhor_solucao = []
        self.melhor_solucao_elementos = []
        self.melhor_resultado = 0
        self.media = 0
        self.nos = 0
        self.melhor_custo = 0

    def decode(self, chromosome, rewrite: bool):

        for gene, s in zip(chromosome, self.subconjuntos):
            s.prioridade = gene

        for s in self.subconjuntos:
            s.var_escolha = 0
        for e in self.elementos:
            e.var_cobertura_total = 0

        maximo = 0
        minimo = len(self.elementos)

        fim = 0
        unicos = 0
        custo_total = 0
        media = 0
        elementos_cobertos = []
        Atualiza_Pesos(self.subconjuntos, self.elementos, fim)

        while True:
            
            maximo, minimo, disponiveis = Encontra_max_min(self.subconjuntos)
            if disponiveis == 0:
                break

            rcl = Constroi_RCL(self.subconjuntos, maximo, minimo, self.alpha)
            escolhido = Seleciona_conjunto(rcl)
            if escolhido is None:
                break

            escolhido.var_escolha = 1
            for i in escolhido.elementos_cobertos:
                self.elementos[i-1].var_cobertura_total += 1

            Atualiza_Pesos(self.subconjuntos, self.elementos, fim)
    

        solução = Busca_Local(self.subconjuntos, self.elementos)

        for s in solução:
            custo_total += s.peso
            for i in s.elementos_cobertos:
                if i not in elementos_cobertos:
                    elementos_cobertos.append(i)
                if self.elementos[i-1].var_cobertura_total == 1:
                    unicos += 1
                media += self.elementos[i-1].var_cobertura_total
        
        if unicos > self.melhor_resultado:
            self.melhor_solução = []
            for s in solução:
                self.melhor_solução.append(s.id)
            self.subconjuntos_resposta = self.subconjuntos
            self.elementos_resposta = self.elementos
            self.media = media/len(self.elementos)
            self.melhor_solucao_elementos = elementos_cobertos
            self.melhor_resultado = unicos
            self.nos = len(self.melhor_solução)
            self.melhor_custo = custo_total

        return unicos


# Executa o solver
def executa_solver(arquivo_leitura: List[Arquivo_scp], matriz, tempo_max, regras_parada, output_padrao_completo,escrita, arquivo_escrita):
    # Inicialização das variaveis:

    alterar_target = 1 if regras_parada[1] == None else 0

    # Quantidade de arquivos no vetor arquivo leitura, menos o 'TESTE'
    qtd_arquivos = arquivo_leitura[len(arquivo_leitura)-1].id

    # Vetor  que armazena o tempo de execução de cada instância.
    tempo_execucao = [0 for _ in range(len(arquivo_leitura))]
    iteracoes_total = [0 for _ in range(len(arquivo_leitura))]
    

    if tempo_max <= 0.0:
        raise RuntimeError(f"O tempo máximo de execução deve ser maior que 0.0. "
                            f"Given {tempo_execucao}.")

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
                escrita_permitida = 1
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

    configuration_file = "config.conf"

    parametros_brkga, controle_brkga = load_configuration(configuration_file)

    print(f"\nArquivo de configuração: {configuration_file}")
    print(f"\nParâmetros do algoritmo:")
    output_string = ""

    for name, value in vars(parametros_brkga).items():
        output_string += f"\n>  -{name} {value}"
    for name, value in vars(controle_brkga).items():
        output_string += f"\n>  -{name} {value}"

    print(output_string.strip())

    if escrita_permitida:
        escreve_cabecalho(qtd_arquivos, arquivo_escrita, configuration_file, [parametros_brkga, controle_brkga])

    # Verifica se a execução é um teste
    if qtd_arquivos == -1:

        # Garante a leitura apenas do ultimo elemento do vetor arquivo_leitura, sendo ele o teste
        qtd_arquivos = len(arquivo_leitura)
        qtd = len(arquivo_leitura)-1

        # Inicialização das listas de subconjuntos e elementos do teste
        subconjuntos = [Subconjunto(id=j+1) for j in range(arquivo_leitura[qtd].colunas)]
        elementos = [Elemento(id = i+1) for i in range(arquivo_leitura[qtd].linhas)]
    else:
        qtd = 0

    solucao = [0 for _ in range(qtd_arquivos)]
    solucao_elementos = [0 for _ in range(qtd_arquivos)]    
    nos = [0 for _ in range(qtd_arquivos)]
    custo_total= [0 for _ in range(qtd_arquivos)]

    while qtd < qtd_arquivos:
        i = 0
        j = 0 

        #Inicialização da média da cobertura total de um elemento
        media_cobertura = 0

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
        
        # Definição de M ≥ |U|
        M = arquivo_leitura[qtd].colunas + 1
        alpha = 0.1
        cromossomo_qtd = len(subconjuntos)
        seed=time.time()
        regras_parada[1] = len(elementos) if alterar_target == 1 else regras_parada[1]

        print(f"Instância: {arquivo_leitura[qtd].nome}")
        print(f'Elementos = {arquivo_leitura[qtd].linhas}')
        print(f'Subconjutos = {arquivo_leitura[qtd].colunas}')
        

        print(f"\nSeed: {seed}")
        print(f"Tempo máximo de execução (s): {tempo_max}")

        print(f"\n\nConstruindo solver BRKGA...")
        
        decode = SCPDecoder(subconjuntos, elementos, M, alpha)

        solver_brkga = BrkgaMpIpr(
            decoder=decode,
            sense = Sense.MAXIMIZE,
            seed=seed,
            chromosome_size=cromossomo_qtd,
            params = parametros_brkga
        )

        print(f"\nGenerando sequência inicial...")

        # Generate a greedy solution to be used as warm start for BRKGA.
        random.seed(seed)
        tam_possivel_escolha = math.floor(len(subconjuntos)*0.08)
        cromossomo = []
        gera_1 = [random.uniform(0.85,1) for _ in range(tam_possivel_escolha)]
        gera_2 = [random.uniform(0.01, 0.85) for _ in range(len(subconjuntos)- tam_possivel_escolha)]
        cromossomo.extend(gera_1)
        cromossomo.extend(gera_2)
        random.shuffle(cromossomo)

        resultado_inicial = greedy(subconjuntos, elementos, cromossomo)
        print(f"Custo inicial: {resultado_inicial}")

        cromossomo = sorted(cromossomo, reverse=True)

        solucao_inicial = sorted(subconjuntos, key=lambda s: s.var_escolha, reverse=True)

        # Then, we visit each node in the tour and assign to it a key.
        cromossomo_inicial = [0] * len(subconjuntos)
        for i in range(len(subconjuntos)):
            cromossomo_inicial[solucao_inicial[i].id-1] = cromossomo[i]

        # Inject the warm start solution in the initial population.
        solver_brkga.set_initial_population([cromossomo_inicial])

        solver_brkga.initialize()

        bogus_alg = deepcopy(solver_brkga)
        bogus_alg.evolve(2)
        bogus_alg.get_best_fitness()
        bogus_alg.get_best_chromosome()
        bogus_alg = None

        best_cost = resultado_inicial
        iteracao = 0
        last_update_time = 0.0
        last_update_iteration = 0
        large_offset = 0
        run = True
        start_time = time.time()

        print(f"\nIter | Resp | Temp")

        guarda_iteracoes = []

        while run:
            iteracao += 1

            # Evolves one iteration.
            solver_brkga.evolve()

            # Checks the current results and holds the best.
            fitness = solver_brkga.get_best_fitness()
            if fitness > best_cost:
                last_update_time = time.time() - start_time
                update_offset = iteracao - last_update_iteration

                if large_offset < update_offset:
                    large_offset = update_offset

                last_update_iteration = iteracao
                best_cost = fitness

                guarda_iteracoes.append([iteracao, best_cost, last_update_time])

                print(f"* {iteracao} | {best_cost:.0f} | {last_update_time:.2f}")
            
            iter_without_improvement = iteracao - last_update_iteration

            run = not (
                (time.time()- start_time > tempo_max)
                or
                ((0 if regras_parada[0] != None else None) == StopRule.GENERATIONS.value and iteracao == regras_parada[0])
                or
                ((1 if regras_parada[1] != None else None) == StopRule.TARGET.value and best_cost == regras_parada[1])
                or
                ((2 if regras_parada[2] != None else None) == StopRule.IMPROVEMENT.value and iter_without_improvement >= regras_parada[2])
                
            )

        subconjuntos = decode.subconjuntos_resposta
        elementos = decode.elementos_resposta

        tempo_execucao[qtd] = time.time() - start_time
        iteracoes_total[qtd] = iteracao

        solucao[qtd] = decode.melhor_solucao
        solucao_elementos[qtd] = decode.melhor_solucao_elementos
        nos[qtd] = decode.nos
        custo_total[qtd] = decode.melhor_custo
        gap1 = ((len(elementos) - best_cost)/len(elementos)) * 100
        gap2 = ((len(elementos) - best_cost)/best_cost) * 100
        

        if best_cost > 0:

            print('\nUma solução factível foi encontrada.')

            
            print(f"\n\nMelhor resultado:                      {best_cost:.0f}")
            print(f"Gap integralidade:                     {gap1:.2f}%")
            print(f"Gap proporcional à solução encontrada: {gap2:.2f}%")
            print(f"Peso total:                           {custo_total[qtd]}")
            print(f"Quantidade de nós:                     {nos[qtd]}")
            print(f"Total de iterações:                    {iteracoes_total[qtd]}")

            media_cobertura = decode.media
            print(f"Cobertura média dos elementos:         {media_cobertura:.2f}")
            print(f"Seed:                                  {seed}")
            print(f"\nTempo em segundos:                     {tempo_execucao[qtd]:.2f}")
            h_c, m_c, s_c, ms_c = converter_tempo(tempo_execucao[qtd])
            print(f"Tempo em horas:                        {h_c}h {m_c}min {s_c}s {ms_c}ms")
            

            # Descreve todos os subconjuntos selecionados e seus respectivos elementos cobertos
            if output_padrao_completo == 1:
                
                print(f"\nMaior número de iterações sem melhora: {large_offset};")
                print(f"Última iteração de melhora:            {last_update_iteration};")
                print(f"Último momento de melhora:               {last_update_time:.2f}s;")

                print('\nConjuntos selecionados:')
                for j in solucao[qtd]:
                    print(f'- Conjunto S{j}\n    Elementos cobertos: {subconjuntos[j].elementos_cobertos}')

                print(f'\nDetalhes da cobertura por elemento da instancia {arquivo_leitura[qtd].nome}:')
                for i in range(len(elementos)):
                    coberto_unicamente = "Sim" if (i+1) in solucao_elementos else "Não"
                    print(f'Elemento {i+1}: coberto {int(elementos[i].var_cobertura_total)} vez(es). Cobertura única: {coberto_unicamente}')

            
        else:
            print('\nO problema não tem solução.')
            
            h_c, m_c, s_c, ms_c = converter_tempo(tempo_total)

            print(f"Tempo em segundos: {tempo_execucao[qtd]:.2f}s;")
            
            print(f"Tempo em horas: {h_c}h {m_c}min {s_c}s {ms_c}ms")

            media_cobertura = 0
            gap1 = 0
            gap2 = 0

        padrao_resposta = [seed, guarda_iteracoes, nos[qtd], custo_total[qtd], solucao[qtd], solucao_elementos[qtd], large_offset, last_update_iteration, last_update_time, iteracoes_total[qtd], gap1, gap2, configuration_file, [parametros_brkga, controle_brkga], [resultado_inicial, cromossomo_inicial]]

        if escrita_permitida:
            # Verifica se o TESTE está ativado
            if qtd == len(arquivo_leitura) - 1:
                arquivo_escrita = "testes.txt"
                
            # Grava o retorno do solver no 'arquivo_escrita'
            escreve_teste(arquivo_leitura[qtd], subconjuntos, elementos, arquivo_escrita, padrao_resposta, media_cobertura, tempo_execucao[qtd])

        qtd += 1

    # Verifica se mais de 1 execução foi realizada para a impressão da soma dos tempos de execução
    if not (arquivo_leitura[qtd-1].nome == "TESTE" or qtd_arquivos == 1):
        tempo_total = sum(i for i in tempo_execucao)

        h_c, m_c, s_c, ms_c = converter_tempo(tempo_total)

        print(f"\n\nTempo total de execução da(s) {qtd} instância(s) (segundos): {tempo_total:.3f} segundos")
        
        print(f"\nTempo total de execução da(s) {qtd} instância(s) (horas): {h_c}h {m_c}min {s_c}s {ms_c}ms")

        if escrita_permitida:
            with open(arquivo_escrita, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"\n\n\nTempo total de execução da(s) {qtd} instância(s) (segundos): {tempo_total:.3f} segundos")

                arquivo.write(f"\n\nTempo total de execução da(s) {qtd} instância(s) (horas):    {h_c}h {m_c}min {s_c}s {ms_c}ms")

    return subconjuntos, elementos, matriz

def main():
    # Parametros básicos para a execução:
    
    # Nome do arquivo no qual o resultado dos testes poderá ser escrito (opcional).
    arquivo_escrita = "resultadosBRKGA.txt"

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

    # Tempo máximo de excução em segundos.
    tempo_max = 3600

    regra_parada_geracao = None

    regra_parada_valor_alvo = None

    regra_parada_sem_melhora = None

    regras_parada = [regra_parada_geracao, regra_parada_valor_alvo, regra_parada_sem_melhora]   
    
    # Avalia se o programa lerá o arquivo especificado em "nome" (teste=0) ou executará um teste com a matriz "matriz" (teste=1).
    teste = 0

    # Avalia se o resultado do solver será escrito no 'arquivo_escrita'.
    escrita = 1

    # Define a saida de uma descrição detalhada, no terminal, dos subconjuntos escolhidos e elementos cobertos (opicional)
    output_padrao_completo = 0

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
        arquivo_escrita = "testesBRKGA.txt"
        arquivo_leitura[qtd_arquivos_leitura].id = -1

    # Execução do solver
    executa_solver(arquivo_leitura, matriz, tempo_max, regras_parada, output_padrao_completo, escrita, arquivo_escrita)



if __name__ == "__main__":
    main()  
