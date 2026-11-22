import polars as pl
from Parte_2.no import no
from collections import deque
from Parte_2.bfs import criar_grafo_from_csv


def relaxa(u,v, w):

    if v.getDis() > u.getDis() + w:
        v.setDis(u.getDis()+w)
        v.setPai(u)
        return True
    return False

def contar_vertices(caminho_entrada, tamanho_csv):
    # Função meramente utilizada para confirmar a quantidade de vértices fornecidas no site
    df = pl.read_csv(
        caminho_entrada,
        separator="\t",
        comment_prefix="#",
        n_rows=tamanho_csv,
        has_header=True,
        new_columns=["src", "dst"],
        schema_overrides={"src": pl.Int64, "dst": pl.Int64},
    )
    # Junta src e dst em uma única coluna, remove duplicatas e ordena em ordem crescente
    df_vertices = (
        pl.select(pl.concat([df["src"], df["dst"]]).alias("vertex"))
        .unique(subset=["vertex"], maintain_order=False)
        .sort("vertex", descending=False)
    )
    # Salva em arquivo .csv
    df_vertices.write_csv(
        "Output/Tratamento_de_entrada/vertices_unicos.csv",
        separator=" ",
        include_header=False,
    )
    return df_vertices
def bellman_ford_forcado(caminho_csv, tamanho_csv, no_raiz, coluna_origem="src", coluna_destino="dst"):
    arestas = pl.read_csv(
        caminho_csv,
        has_header=True,
        separator="\t",
        n_rows= tamanho_csv,
        new_columns=[coluna_origem, coluna_destino],
    )
    vertices = contar_vertices(caminho_csv,tamanho_csv)
    
    grafo: dict[str, no] = {}

    for (vertice,) in vertices.iter_rows():
        novo_no = no(vertice,[])
        novo_no.setDis(float("inf"))
        novo_no.setPai(None)

        grafo[str(vertice)] = novo_no
        
    no_raiz = grafo[no_raiz]
    no_raiz.setDis(0)
    for i in range(vertices.height -1):
        for aresta in arestas.iter_rows(named=True):
            relaxa(grafo[str(aresta["src"])], grafo[str(aresta["dst"])], w=1)
    for aresta in arestas.iter_rows(named=True):
        if relaxa(grafo[str(aresta["src"])], grafo[str(aresta["dst"])],w=1):
            return False

    return True, grafo
        
if __name__ == '__main__':
    ctrl, grafo =(bellman_ford_forcado("Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv", 1000, "2"))
    print(ctrl, grafo["316"].getDis())