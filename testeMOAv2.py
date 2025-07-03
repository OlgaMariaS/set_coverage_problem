from dataclasses import dataclass
from typing import List, Tuple
from ortools.init.python import init
from ortools.linear_solver import pywraplp
import time

class Subconjunto:
    id: int
    peso: int
    var_escolha: int

class Elemento:
    id: int
    num_coberturas: int
    var_cobertura_unica: int
    var_cobertura_total: int

def abrir_arquivo(nome):
    try:
        arquivo = open(nome, "r")
        print("\nO arquivo foi aberto com sucesso!")
        return arquivo
    except FileNotFoundError:
        print("\nERRO! O arquivo n�o foi aberto!")
        exit(1)

def ler_cabecalho(arquivo):
    linha = []
    coluna = []

    arquivo.read(1)
    while True:
        aux = arquivo.read(1)
        if aux == ' ':
            linha = ''.join(linha)
            break
        linha.append(aux)
    l = int(linha)
    #print("linhas: ", linha)

    while True:
        aux = arquivo.read(1)
        if aux == ' ':
            coluna = ''.join(coluna)
            arquivo.read(1)
            break
        elif aux == '\n':
            aux = arquivo.read(1)
            continue
        else:
            coluna.append(aux)
    c = int(coluna)
    #print("colunas: ", coluna)

    return l, c

def ler_conteudo(l, c, arquivo):
    subconjuntos = [Subconjunto() for _ in range(c)]
    m = [[0 for _ in range(c)] for _ in range(l)]
    elementos = [Elemento() for _ in range(l)]

    i = 0
    arquivo.read(1)
    while i < c:
        buffer = []
        while True:
            aux = arquivo.read(1)
            if aux == ' ':
                buffer = ''.join(buffer)
                break
            elif aux == '\n':
                arquivo.read(1)
                continue
            else:
                buffer.append(aux)
        subconjuntos[i].id = i
        subconjuntos[i].peso = int(buffer)
        i += 1
    arquivo.read(1)


    for i in range(l):

        arquivo.read(1)
        buffer = []
        while True:
            aux = arquivo.read(1)
            if aux == ' ':
                buffer = ''.join(buffer)
                arquivo.read(1)
                break
            else:
                buffer.append(aux)
        elementos[i].num_coberturas = int(buffer)
        #print("coberturas da linha {i} = {elementos[i].num_coberturas}")


        arquivo.read(1)
        for _ in range(elementos[i].num_coberturas):
            buffer = []
            while True:
                aux = arquivo.read(1)
                if aux == ' ':
                    buffer = ''.join(buffer)
                    break
                elif aux == '\n':
                    arquivo.read(1)
                    continue
                else:
                    buffer.append(aux)

            aux_num = int(buffer)
            m[i][aux_num-1] = 1

        arquivo.read(1)

    return subconjuntos, m, elementos

def executa_solver(linhas, colunas, elementos:Elemento , subconjuntos:Subconjunto, matriz, tempo_max, output, escrita):

    M = colunas

    solver = pywraplp.Solver.CreateSolver("CBC")
    if not solver:
        print("Nao foi possivel criar o solver CBC")
        escrita.write("\nNao foi possivel criar o solver CBC\n\n")
        return
    else:
        print("Solver CBC criado com sucesso!")
        escrita.write("\nSolver CBC criado com sucesso!")


    infinity = solver.infinity()
    for j in range(colunas):
        subconjuntos[j].var_escolha = solver.BoolVar(f'x{j+1}')

    for i in range(linhas):
        elementos[i].var_cobertura_unica = solver.BoolVar(f'y{i+1}')
        
    for i in range(linhas):
        elementos[i].var_cobertura_total = solver.IntVar(0, infinity, ('z' + str(i+1)))

    num_vars = solver.NumVariables()
    print("Numero de variáveis =", num_vars)
    escrita.write("\nNumero de variaveis = " + str(num_vars))

    for i in range(linhas):
        solver.Add(sum(matriz[i][j] * subconjuntos[j].var_escolha for j in range(colunas)) == elementos[i].var_cobertura_total)

    for i in range(linhas):
        solver.Add(elementos[i].var_cobertura_unica <= elementos[i].var_cobertura_total)

        solver.Add((M-1) * elementos[i].var_cobertura_unica + elementos[i].var_cobertura_total <= M)
    
    num_resticoes = solver.NumConstraints()
    print("Número de restrições =", num_resticoes)
    escrita.write("\nNumero de restricoes = " + str(num_resticoes))
    
    funcao_objetivo = solver.Objective()
    for i in range(linhas):
        funcao_objetivo.SetCoefficient(elementos[i].var_cobertura_unica, 1)
    funcao_objetivo.SetMaximization()

    solver.set_time_limit(tempo_max)
    if output:
        solver.EnableOutput()

    versao_solver = solver.SolverVersion()
    print("Resolvendo com o solver ", versao_solver)
    escrita.write("\nResolvendo com o solver " + versao_solver)
    start_time = time.time()
    resultado = solver.Solve()
    end_time = time.time()

    tempo_execucao = end_time - start_time

    if resultado == pywraplp.Solver.OPTIMAL or resultado == pywraplp.Solver.FEASIBLE:
        
        if resultado == pywraplp.Solver.OPTIMAL:
            print("\nSolução ótima encontrada!")
            escrita.write("\n\nSolucao otima encontrada!")
        else:
            print("\nUma solução factível foi encontrada")
            escrita.write("\n\nUma solucao factivel foi encontrada.")
        
        print("\nValor da Função Objetivo (elementos cobertos unicamente) = ", funcao_objetivo.Value())
        escrita.write("\n\nValor da Funcao Objetivo (elementos cobertos unicamente) = " + str(funcao_objetivo.Value()))
        
        print("\nConjuntos selecionados:")
        escrita.write("\n\nConjuntos selecionados:")
        for j in range(colunas):
            subconjuntos[j].var_escolha = subconjuntos[j].var_escolha.solution_value()
            if subconjuntos[j].var_escolha > 0.5:
                print("- Conjunto S", j+1)
                escrita.write("\n- Conjunto S" + str(j+1))

        print("\nDetalhes da cobertura por elemento:")
        escrita.write("\n\nDetalhes da cobertura por elemento:")
        for i in range(linhas):
            elementos[i].var_cobertura_total = elementos[i].var_cobertura_total.solution_value()
            elementos[i].var_cobertura_unica = elementos[i].var_cobertura_unica.solution_value()
            coberto_unicamente = "Sim" if elementos[i].var_cobertura_unica > 0.5 else "Não"
            print(f'Elemento {i+1}: coberto {int(elementos[i].var_cobertura_total)} vez(es). Cobertura única: {coberto_unicamente}')
            escrita.write("\nElemento " + str(i+1) + ": coberto " + str(elementos[i].var_cobertura_total) + " vez(es). Cobertura unica: " + coberto_unicamente)

    else:
        print('O problema não tem solução ótima.')
        escrita.write("\nO problema nao tem solucao otima.")


    print(f"\nTempo de execução da instância: {tempo_execucao:.4f} segundos")
    escrita.write(f"\n\nTempo de execucao da instancia: {tempo_execucao:.4f} segundos")

def main():
    escrita = open("testes.txt", "a")
    #O resultado da execução será escrita no fim do arquivo "testes.txt" para guardar os resultados gerados pelo solver.

    #parametros básicos para a execução
    nome = "scp41.txt" #nome do arquivo a ser lido (opcional para testes).
    tempo_max = 60000 #tempo máximo de excução em milisegundos (Ex: 60.000 milisegundos -> 60 segundos * 1000, ou seja, são 60 segundo de execução do solver.)
    teste = 1 #avalia se o programa lerá o arquivo especificado em "nome" (teste=0) ou executará um teste com a matriz "ma" (teste=1)
    ma = [[1, 0, 0, 0, 1],  
          [0, 1, 0, 0, 0],  
          [1, 1, 0, 0, 0],  
          [1, 0, 0, 0, 1],  
          [0, 0, 1, 0, 0]] #matriz "ma", para testes.
    
    if not teste:
        arquivo = abrir_arquivo(nome)
        escrita.write("\n\nNome do arquivo: " + nome)

        linhas, colunas = ler_cabecalho(arquivo)
        escrita.write("\nLinhas: " + str(linhas))
        escrita.write("\nColunas: " + str(colunas))

        subconjuntos, matriz, elementos = ler_conteudo(linhas, colunas, arquivo)

        arquivo.close()

        #print("Matriz: ", matriz)
        executa_solver(linhas, colunas, elementos, subconjuntos, matriz, tempo_max, 0, escrita)
    else:
        subconjuntos = [Subconjunto() for _ in range(5)]
        elementos = [Elemento() for _ in range(5)]

        print("Matriz: ", ma)
        escrita.write("\n\nMatriz: " +  str(ma))

        print("Linhas: 5")
        print("Colunas: 5")
        escrita.write("\nLinhas: 5")
        escrita.write("\nColunas: 5")

        executa_solver(5, 5, elementos, subconjuntos, ma, tempo_max, 0, escrita)


    escrita.close()

    #print("\nMatriz: ")
    #for i in range(linhas):
     #   for j in range(colunas):
      #      print(("a", i+1, j+1 ) + (" = ", matriz[i][j]))

    

if __name__ == "__main__":
    main()  
