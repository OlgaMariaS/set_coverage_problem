#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct{
    int id;
    int peso;
} subconjunto;

void abrir_arquivo(char nome[], FILE **arquivo){
    if ((*arquivo = fopen(nome, "r")) == NULL)
    {
        printf("\nERRO! O arquivo não foi aberto!\n");
        exit(1);
    }
    else
    {
        printf("\nO arquivo foi aberto com sucesso! %i", strcmp("a","b"));
    }
}

void ler_cabecalho(int *l, int *c, FILE *arquivo){
    int i, espaco;
    char aux, linha[10], coluna[10];

    espaco = 1;
    i=0;
    fread(&aux, sizeof(char), 1, arquivo);
    while(espaco){
        fread(&aux, sizeof(char), 1, arquivo);
        //printf("\n aux = %c, %i", aux, i);
        if(aux == ' '){
            espaco = 0;
            linha[i] = '\0';
        }else{
            linha[i] = aux;
            i++;
        }
    }
    *l = atoi(linha);

    espaco = 1;
    i=0;
    while(espaco){
        fread(&aux, sizeof(char), 1, arquivo);
        //printf("\n aux = %c", aux);
        if(aux == ' '){
            fread(&aux, sizeof(char), 1, arquivo);
            espaco = 0;
            coluna[i] = '\0';
        }else if(aux == '\n'){
                fread(&aux, sizeof(char), 1, arquivo);
            }else{
                coluna[i] = aux;
                i++;
        }
    }
    *c = atoi(coluna);
}

void ler_conteudo(int l, int c, subconjunto v[], int m[l][c], int num_coberturas[], FILE *arquivo){
    int i, j, k, espaco;
    int aux_num, num_atual;
    char aux;
    char buffer[15];

    espaco = 1;
    i=0;
    fread(&aux, sizeof(char), 1, arquivo);
    while(i<c){
        j = 0;
        while(espaco){
            fread(&aux, sizeof(char), 1, arquivo);
            printf("\n aux3 = %c, i = %i", aux, i);
            if(aux == ' '){
                espaco = 0;
                buffer[j] = '\0';
                v[i].id = i;
                v[i].peso = atoi(buffer);
            }else if(aux == '\n'){
                    fread(&aux, sizeof(char), 1, arquivo);
                }else{
                    buffer[j] = aux;
                    j++;
                }
        }
        espaco = 1;
        i++;
    }
    fread(&aux, sizeof(char), 1, arquivo);

    aux_num = 0;
    i = 0;
    j = 0;
    k = 0;

    while(i<l){
        num_atual = 0;
        j = 0;

        fread(&aux, sizeof(char), 1, arquivo);
        while(espaco){
            fread(&aux, sizeof(char), 1, arquivo);
            printf("\n aux4 = %c", aux);
            if(aux == ' '){
                espaco = 0;
                buffer[j] = '\0';
            }else{
                buffer[j] = aux;
                j++;
            }
        }
        fread(&aux, sizeof(char), 1, arquivo);

        espaco = 1;
        num_coberturas[i] = atoi(buffer);
        printf("\ncoberturas da linha %i = %i", i, num_coberturas[i]);

        fread(&aux, sizeof(char), 1, arquivo);
        for(k=0;k<num_coberturas[i];k++){
            j=0;
            while(espaco){
                fread(&aux, sizeof(char), 1, arquivo);
                //printf("\n aux5 = %c", aux);
                if(aux == ' '){
                    espaco = 0;
                    buffer[j] = '\0';
                    aux_num = atoi(buffer);
                    m[i][aux_num - 1] = 1;
                    //printf("\nlinha1 = %i, coluna = %i == %i", i, aux_num-1, m[i][aux_num-1]);
                    for(j=num_atual;j<aux_num-1;j++){
                        m[i][j] = 0;
                        //printf("\nlinha2 = %i, coluna = %i == %i", i, j, m[i][j]);
                    }
                    num_atual = aux_num;
                }else if(aux == '\n'){
                        fread(&aux, sizeof(char), 1, arquivo);
                    }else{
                        buffer[j] = aux;
                        j++;
                    }
            }
            espaco = 1;
        }
        fread(&aux, sizeof(char), 1, arquivo);
        for(j=num_atual;j<c;j++){
            m[i][j] = 0;
            //printf("\nlinha3 = %i, coluna = %i == %i", i, j, m[i][j]);
        }

        i++;
    }
}

int main (){
    int i, j;
    int linhas, colunas;
    char nome[20];
    FILE *arquivo;

    strcpy(nome, "scp41.txt");

    //abrir arquivo:
    //READ  -> 0
    //WRITE -> 1
    abrir_arquivo(nome, &arquivo);

    ler_cabecalho(&linhas, &colunas, arquivo);

    subconjunto vetor[colunas];
    int matriz[linhas][colunas];
    int num_coberturas[linhas];

    ler_conteudo(linhas, colunas, vetor, matriz, num_coberturas, arquivo);

    fclose(arquivo);

    /*while(i<c){
        printf("\nVetor[%i]\nID = %i \nPeso = %i\n", i, vetor[i].id, vetor[i].peso);
        i++;
    }


    printf("\nMatriz: \n");
    for(i=0;i<linhas;i++){
        for(j=0;j<colunas;j++){
            printf("%i | %i ", i, matriz[i][j]);
        }
        printf("\n");
    }*/



}
