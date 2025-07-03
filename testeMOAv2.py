from dataclasses import dataclass
from typing import List, Tuple
from ortools.init.python import init
from ortools.linear_solver import pywraplp

class Subconjunto:
    id: int
    peso: int
    var_escolha: int

class Elemento:
    id: int
    num_coberturas: int
    var_cobertura_unica: int
    var_cobertura_total: int

class Subconjunto:
    def __init__(self, id=0, peso=0):
        self.id = id
        self.peso = peso

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

    # Ler a primeira linha at� espa�o
    arquivo.read(1)
    while True:
        aux = arquivo.read(1)
        if aux == ' ':
            linha = ''.join(linha)
            break
        linha.append(aux)
    l = int(linha)
    print("linhas: ", linha)

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
    print("colunas: ", coluna)

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
        elementos[i] = int(buffer)
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

def main():
    nome = "scp41.txt"


    arquivo = abrir_arquivo(nome)

    linhas, colunas = ler_cabecalho(arquivo)

    subconjuntos, matriz, elementos = ler_conteudo(linhas, colunas, arquivo)


    arquivo.close()

    print("\nMatriz: ")
    for i in range(linhas):
        for j in range(colunas):
            print(("a", i+1, j+1 ) + (" = ", matriz[i][j]))

    m = [[1, 0, 1], [0, 1, 0], [1, 0 ,1]]

    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("Nao foi possivel criar o solver GLOP")
        return

    for j in range(colunas):
        subconjuntos[j].var_escolha = solver.NumVar(0, 1, ("x", j))

    for i in range(linhas):
        elementos[i].var_esolha



    variavel_y = solver.NumVar(0, 1, "y%i")
    variavel_z = solver.NumVar(0, 1, "z")

    print("Number of variables =", solver.NumVariables())

if __name__ == "__main__":
    main()
