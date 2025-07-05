from ortools.linear_solver import pywraplp
import time

#LEITURA, RESOLUÇÃO E ESCRITA DE INSTANCIAS SCP

class Subconjunto:
    id: int
    peso: int
    elementos_cobertos = []
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

    #arquivo.read(1)
    while True:
        aux = arquivo.read(1)
        if aux == ' ':
            if not linha:
                continue
            else:
                linha = ''.join(linha)
                break
        linha.append(aux)
    l = int(linha)
    #print("linhas: ", linha)

    while True:
        aux = arquivo.read(1)
        if aux == ' ':
            if not coluna:
                continue
            else:
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

    #arquivo.read(1)
    for i in range(c):
        buffer = []
        while True:
            aux = arquivo.read(1)
            if aux == ' ':
                if not buffer:
                    continue
                else:
                    buffer = ''.join(buffer)
                    break
            elif aux == '\n':
                arquivo.read(1)
                continue
            else:
                buffer.append(aux)
        subconjuntos[i].id = i
        subconjuntos[i].peso = int(buffer)
    #arquivo.read(1)


    for i in range(l):

        #arquivo.read(1)
        buffer = []
        while True:
            aux = arquivo.read(1)
            if aux == ' ':
                if not buffer:
                    continue
                else:
                    buffer = ''.join(buffer)
                break
            elif aux == '\n':
                arquivo.read(1)
                continue
            else:
                buffer.append(aux)
        elementos[i].num_coberturas = int(buffer)
        #print("coberturas da linha {i} = {elementos[i].num_coberturas}")


        #arquivo.read(1)
        for _ in range(elementos[i].num_coberturas):
            buffer = []
            while True:
                aux = arquivo.read(1)
                if aux == ' ':
                    if not buffer:
                        continue
                    else:
                        buffer = ''.join(buffer)
                        break
                elif aux == '\n':
                    arquivo.read(1)
                    continue
                else:
                    buffer.append(aux)

            aux_num = int(buffer)
            m[i][aux_num-1] = 1
            subconjuntos[aux_num-1].elementos_cobertos.append(i)

        #arquivo.read(1)

    return subconjuntos, m, elementos

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


def executa_solver(linhas, colunas, elementos:Elemento , subconjuntos:Subconjunto, matriz, tempo_max, output):

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
        
    for i in range(linhas):
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
    print("Resolvendo com o solver ", versao_solver)
    
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
        print("\nValor da Função Objetivo (elementos cobertos unicamente) = ", funcao_objetivo)
        
        
        print("\nConjuntos selecionados:")

        for j in range(colunas):
            subconjuntos[j].var_escolha = subconjuntos[j].var_escolha.solution_value()
            if subconjuntos[j].var_escolha > 0.5:
                print(f"- Conjunto S {j+1}\n    Elementos cobertos: {subconjuntos[j].elementos_cobertos}")
                

        print("\nDetalhes da cobertura por elemento:")
        
        for i in range(linhas):
            elementos[i].var_cobertura_total = elementos[i].var_cobertura_total.solution_value()
            elementos[i].var_cobertura_unica = elementos[i].var_cobertura_unica.solution_value()
            coberto_unicamente = "Sim" if elementos[i].var_cobertura_unica > 0.5 else "Não"
            print(f'Elemento {i+1}: coberto {int(elementos[i].var_cobertura_total)} vez(es). Cobertura única: {coberto_unicamente}')
            
            media_cobertura_total += elementos[i].var_cobertura_total
        
        media_cobertura_total = media_cobertura_total/linhas
        print(f"\nCobertura média dos elementos:  {media_cobertura_total:.2f}")
        

    else:
        print('O problema não tem solução.')
        

    print(f"Tempo de execução da instância: {tempo_execucao:.4f} segundos")

    return num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao
    

def main():
    #Parametros básicos para a execução:

    #Nome do arquivo no qual o resultado dos testes poderá ser escrito (opcional).
    arquivo_escrita = "testes.txt"

    #Nome do arquivo a ser lido (opcional para testes).
    arquivo_leitura = "scp41.txt"
    
    #Tempo máximo de excução em milisegundos (milissegundos -> segundos/1000).
    tempo_max = 1000     
    
    #Avalia se o programa lerá o arquivo especificado em "nome" (teste=0) ou executará um teste com a matriz "ma" (teste=1).
    teste = 0 

    #Avalia se o resultado do solver será escrito no 'arquivo_escrita'.
    escrita = 0 

    #Matriz 'ma' utilizada em testes.
    ma = [[1, 0, 0, 0, 1],  
          [0, 1, 0, 0, 0],  
          [1, 1, 0, 0, 0],  
          [1, 0, 0, 0, 1],  
          [0, 0, 1, 0, 0]]
    

    if not teste:
        #Abertura do 'arquivo_leitura'
        arquivo = abrir_arquivo(arquivo_leitura)

        #Leitura do cabeçalho do 'arquivo_leitura'
        linhas, colunas = ler_cabecalho(arquivo)

        #Leitura do conteúdo do 'arquivo_leitura'
        subconjuntos, matriz, elementos = ler_conteudo(linhas, colunas, arquivo)

        #fechamento do 'arquivo_leitura'
        arquivo.close()

        #Chamada da função executa_solver para gerar um solução a partir da matriz presente no 'arquivo_escrita'
        num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao = executa_solver(linhas, colunas, elementos, subconjuntos, matriz, tempo_max, 0)
    else:
        linhas = 5
        colunas = 5

        subconjuntos = [Subconjunto() for _ in range(colunas)]
        elementos = [Elemento() for _ in range(linhas)]

        print("Matriz: ", ma)

        print("Linhas: ", linhas)
        print("Colunas: ", colunas)

        num_vars, num_restricoes, versao_solver, funcao_objetivo, media_cobertura_total, tempo_execucao = executa_solver(5, 5, elementos, subconjuntos, ma, tempo_max, 0)

    #Chamada da função de escrita, para gravar os resultados da execução do solver no 'arquivo_escrita'
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
