# Problema da cobertura única
O propósito desse projeto de otimização é aplicar duas diferentes abordagens de algoritmos para resolver uma formulação de Programação Linear Inteira (PLI) do problema da cobertura única de conjunto, que é uma variação do problema clássico da cobertura de conjuntos.

Este projeto foi realizado durante as aulas de Modelagem e Otimização Algoritmica na gradução de Informática pela UEM. As duas abordagens utilizadas são: 
  - Algoritmo Branch and Cut - CBC
  - Metaheuristica de algoritmo genético - BRKGA

### Informações: 
  Os relatórios detalham informações sobre o projeto, instâncias, experimentos e resultados;

  Para executar o algoritmo você vai precisar:
  - Ter Python acima da versão 3.11 instalado
  - Instalar a biblioteca OR-Tools para executar o UniqueCoverSolver.py
  
    ```bash
      pip install ortools
    ```
  - Instalar o BRKGA to python para executar o UniqueCoverSolverBRKGA.py
    ```bash
      pip3.7 install brkga-mp-ipr
    ```
  - A pasta "Instâncias" contém todos os arquivos TXT das instãncias a executar, em formato especifico.
  - Na função main() pode ser ajustado algumas variaveis
    - arquivo_escrita
    - tempo_max 
    - teste
    - escrita 
    - output_padrao_completo

### Utilizado:
  - 🐍 Python
  - 📚 [OR-Tools](https://developers.google.com/optimization/introduction/python?hl=pt-br)<br/>
  - 📚 [BRKGA](https://github.com/ceandrade/brkga_mp_ipr_python)<br/>
  - 📍 Instâncias: [OR-Library](https://people.brunel.ac.uk/~mastjjb/jeb/info.html)<br/> 


### Artigo de referencia:

[O Problema da Cobertura única](http://www.din.uem.br/sbpo/sbpo2011/pdf/88121.pdf ) por Regina Beretta Mazaro. <br/>



