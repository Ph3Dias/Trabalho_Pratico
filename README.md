# Trabalho Prático — MATA53

Repositório desenvolvido para a disciplina MATA53, contendo implementações de algoritmos e análises relacionadas à teoria dos grafos.

O projeto utiliza como conjunto de dados principal a rede **Wiki-Talk**, uma rede direcionada que representa interações entre usuários da Wikipédia.

A implementação está organizada em módulos Python, responsáveis pelo tratamento dos dados, análise estrutural do grafo e execução de diferentes algoritmos.

## Objetivos

- Realizar o tratamento de um conjunto de dados de grafos em larga escala.
- Analisar propriedades estruturais de redes direcionadas.
- Implementar algoritmos clássicos de grafos.
- Identificar componentes fortemente conexas.
- Calcular caminhos mínimos.
- Comparar algoritmos de árvore geradora mínima.
- Analisar o desempenho das implementações.

## Estrutura do projeto

A implementação principal está localizada no diretório `TP/`.

```text
Trabalho_Pratico/
│
├── Dataset/
│   └── wiki-talk-temporal.txt
│
├── Output/
│   ├── Tratamento_de_entrada/
│   ├── Parte1/
│   └── ...
│
├── TP/
│   │
│   ├── main.py
│   │
│   ├── Tratamento_de_entrada/
│   │   └── tratamento_entrada.py
│   │
│   ├── Parte_1/
│   │   └── analise_estrutural.py
│   │
│   ├── Parte_2/
│   │   ├── arvore_geradora_minima.py
│   │   ├── bellman_ford.py
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── dijkstra.py
│   │   ├── floyd_warshall.py
│   │   ├── minheap.py
│   │   ├── no.py
│   │   ├── tarjan.py
│   │   └── verificacao_eulerianidade.py
│   │
│   └── Parte_3/
│
├── Trabalho-Pratico-MATA53-main/
├── vizinhanca.png
└── README.md
```

> A pasta `Trabalho-Pratico-MATA53-main` contém uma implementação separada e não faz parte do fluxo de execução documentado neste README.

### Organização dos módulos

| Diretório/Arquivo | Descrição |
|---|---|
| `main.py` | Ponto de entrada da aplicação e menu interativo. |
| `Tratamento_de_entrada/` | Responsável pelo processamento inicial dos dados. |
| `Parte_1/` | Implementação das análises estruturais do grafo. |
| `Parte_2/` | Implementação dos algoritmos de teoria dos grafos. |
| `Parte_3/` | Módulo complementar da terceira parte do trabalho. |

### Principais arquivos

**main.py**

Controla a execução do programa, apresenta o menu de opções e chama as funções implementadas nos demais módulos.

**tratamento_entrada.py**

Realiza a conversão do grafo temporal para uma representação estática, removendo timestamps e arestas duplicadas.

**analise_estrutural.py**

Implementa funções para calcular métricas estruturais, distribuições de graus, componentes fortemente conexas e propriedades do grafo.

**arvore_geradora_minima.py**

Implementa os algoritmos de Prim e Kruskal para encontrar árvores ou florestas geradoras mínimas.

## Tecnologias e dependências

O projeto utiliza Python e as seguintes bibliotecas:

| Biblioteca | Utilização |
|---|---|
| Polars | Leitura, processamento e manipulação dos dados. |
| NetworkX | Representação e análise de grafos. |
| Matplotlib | Construção de gráficos. |
| igraph | Representação e visualização de grafos. |

### Requisitos

- Python 3.10 ou superior.
- Git.
- Pip.

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/Ph3Dias/Trabalho_Pratico.git
```

Entrar no diretório:

```bash
cd Trabalho_Pratico
```

### 2. Criar ambiente virtual

Recomenda-se utilizar um ambiente virtual para isolar as dependências.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install polars networkx matplotlib igraph
```

## Como executar

A execução deve ser realizada a partir da raiz do repositório, pois os caminhos dos arquivos utilizados pela aplicação são relativos a esse diretório.

Execute:

```bash
python TP/main.py
```

No Linux/macOS:

```bash
python3 TP/main.py
```

Após iniciar, será apresentado um menu interativo no terminal.

## Utilização da main.py

A aplicação disponibiliza oito operações principais.

### Menu

```text
Selecione o algoritmo digitando o número correspondente:

1 - Realizar tratamento no grafo de entrada (wiki-talk-temporal.txt)

2 - Árvore Geradora Mínima (Aplicada no Grafo Completo Wiki-Talk)

3 - Bellman-Ford (bellman_ford)

4 - Busca em Largura / BFS (bfs)

5 - Busca em Profundidade / DFS (dfs)

6 - Dijkstra (dijkstra)

7 - Floyd-Warshall (floyd_warshall)

8 - Componentes Fortemente Conexas / Tarjan (tarjan)

0 - Sair
```

### 0 — Sair

Encerra a execução do programa.

### 1 — Tratamento do grafo de entrada

Realiza o processamento inicial do arquivo `wiki-talk-temporal.txt`.

O procedimento contempla:

1. Leitura do conjunto de dados temporal.
2. Remoção da informação temporal das arestas.
3. Remoção de arestas duplicadas.
4. Ordenação das arestas por vértice de origem e destino.
5. Identificação dos vértices existentes.
6. Cálculo dos graus de entrada e saída.
7. Geração das distribuições de graus.
8. Cálculo de métricas estruturais.
9. Identificação das componentes fortemente conexas.
10. Identificação da maior componente fortemente conexa.
11. Geração de visualizações do grafo.

Essa operação pode consumir bastante memória e tempo de processamento devido ao tamanho do dataset.

### 2 — Árvore Geradora Mínima

Executa dois algoritmos:

**Prim**

Constrói uma árvore geradora mínima utilizando uma estrutura de heap mínimo para selecionar as arestas.

**Kruskal**

Ordena as arestas pelo peso e utiliza a estrutura Union-Find para evitar a formação de ciclos.

Os resultados apresentados incluem:

- Quantidade de arestas selecionadas.
- Custo total da árvore geradora.
- Tempo de execução de cada algoritmo.

A implementação utiliza peso padrão igual a 1 quando não existe peso associado às arestas.

### 3 — Bellman-Ford

Executa o algoritmo de Bellman-Ford sobre a maior componente fortemente conexa.

O programa solicita o vértice de origem:

```text
Insira o id do vértice raíz:
```

O algoritmo verifica a existência de ciclos negativos e informa o tempo de execução.

### 4 — Busca em Largura (BFS)

Executa o algoritmo Breadth-First Search.

Solicita um identificador de vértice inicial e utiliza a representação do grafo armazenada em CSV.

A BFS percorre os vértices alcançáveis a partir da origem, explorando primeiro os vizinhos mais próximos.

O tempo de execução é apresentado ao final.

### 5 — Busca em Profundidade (DFS)

Executa o algoritmo Depth-First Search por meio de uma implementação iterativa.

A busca explora os caminhos em profundidade antes de retornar para explorar outros caminhos disponíveis.

O programa informa o tempo de execução.

### 6 — Dijkstra

Executa o algoritmo de Dijkstra para calcular caminhos mínimos a partir de um vértice de origem.

O programa solicita:

```text
Insira o ID do vértice raíz:
```

A execução utiliza o grafo estático armazenado na pasta de tratamento de entrada.

### 7 — Floyd-Warshall

Executa o algoritmo de Floyd-Warshall para calcular os caminhos mínimos entre pares de vértices.

O programa solicita a quantidade de arestas que será utilizada:

```text
Insira a quantidade de arestas (para usar todas, insira -1):
```

- Um número positivo limita a quantidade de arestas consideradas.
- `-1` utiliza todas as arestas disponíveis.

O processamento é realizado sobre a maior componente fortemente conexa.

### 8 — Tarjan

Executa o algoritmo de Tarjan para identificar as componentes fortemente conexas do grafo.

Ao final, apresenta:

- Quantidade total de componentes fortemente conexas.
- Tempo de execução.

### Reexibir o menu

Durante a execução, é possível digitar:

```text
h
```

Para exibir novamente as opções disponíveis.

## Arquivos gerados

Os resultados são armazenados no diretório `Output/`.

### Tratamento de entrada

| Arquivo | Descrição |
|---|---|
| `arestas_ordenadas_estaticas.csv` | Lista de arestas após a conversão do grafo temporal para estático. |
| `vertices_grafo_ordenado.csv` | Lista de vértices identificados no grafo. |

### Parte 1 — Análise estrutural

| Arquivo | Descrição |
|---|---|
| `graus_vertices.csv` | Graus de entrada e saída dos vértices. |
| `distribuicao_in_degree.csv` | Distribuição dos graus de entrada. |
| `distribuicao_out_degree.csv` | Distribuição dos graus de saída. |
| `maior_cfc_arestas.csv` | Arestas pertencentes à maior componente fortemente conexa. |

Também são gerados gráficos com as distribuições dos graus e visualizações do grafo.

## Observações importantes

- A opção 1 deve ser executada antes dos algoritmos que dependem dos arquivos gerados pelo tratamento de entrada.
- Os arquivos CSV intermediários são utilizados pelas demais funcionalidades.
- A maior componente fortemente conexa é utilizada em operações específicas, como Bellman-Ford e Floyd-Warshall.
- A execução de algoritmos sobre grafos grandes pode exigir bastante memória e processamento.
- Os caminhos dos arquivos são relativos à raiz do repositório.

## Autores

Desenvolvido como trabalho prático da disciplina MATA53.

Repositório: https://github.com/Ph3Dias/Trabalho_Pratico