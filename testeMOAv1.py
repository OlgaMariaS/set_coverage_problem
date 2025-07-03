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
        print("\nERRO! O arquivo não foi aberto!")
        exit(1)

def ler_cabecalho(arquivo):
    linha = []
    coluna = []
    
    # Ler a primeira linha até espaço
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
    v = [Subconjunto() for _ in range(c)]
    m = [[0 for _ in range(c)] for _ in range(l)]
    num_coberturas = [0 for _ in range(l)]

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
        v[i].id = i
        v[i].peso = int(buffer)
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
        num_coberturas[i] = int(buffer)
        #print(f"coberturas da linha {i} = {num_coberturas[i]}")


        arquivo.read(1)
        for _ in range(num_coberturas[i]):
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

    return v, m, num_coberturas

def main():
    nome = ["scp41.txt", "scp51.txt"]


    arquivo = abrir_arquivo(nome[0])

    linhas, colunas = ler_cabecalho(arquivo)

    vetor, matriz, num_coberturas = ler_conteudo(linhas, colunas, arquivo)


    arquivo.close()

    
    for i in range(colunas):
        print(f"\nVetor[{i}]\nID = {vetor[i].id} \nPeso = {vetor[i].peso}")


    print("\nMatriz: ")
    for i in range(linhas):
        for j in range(colunas):
            if matriz[i][j] == 1:   
                print(('a', i+1, j+1 ) + (' = ', matriz[i][j]))

if __name__ == "__main__":
    main()
