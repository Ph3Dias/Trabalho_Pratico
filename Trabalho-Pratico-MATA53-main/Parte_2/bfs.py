import networkx as nx
import polars as pl
from Parte_2.no import *
from collections import deque

def criar_grafo_from_csv(
    caminho_arquivo: str,
    n_linhas: int | None = None,
    coluna_origem: str = "src",
    coluna_destino: str = "dst",
):
    
    arestas = pl.read_csv(
        caminho_arquivo,
        separator="\t",
        n_rows=n_linhas,
        has_header=True,
        new_columns=[coluna_origem, coluna_destino],
        )

    arestas = (
        arestas.select(
            pl.col(coluna_origem).cast(pl.String).str.strip_chars(),
            pl.col(coluna_destino).cast(pl.String).str.strip_chars(),
        )
        .drop_nulls()
        .unique()
    )

    adjacencias_df = arestas.group_by(coluna_origem, maintain_order=True).agg(
        pl.col(coluna_destino).alias("adj")
    )

    grafo: dict[str, no] = {}

    for origem, lista_destinos in adjacencias_df.iter_rows():
        grafo[origem] = no(id=origem, adj=list(lista_destinos))

    
    for destino in arestas[coluna_destino].unique():
        if destino not in grafo:
            grafo[destino] = no(id=destino, adj=[])

    return grafo

def busca_em_largura(caminho_csv, tamanho_csv, no_raiz_id, no_alvo_id=None, coluna_origem="src", coluna_destino="dst"):

    grafo = criar_grafo_from_csv(caminho_csv, tamanho_csv, coluna_origem, coluna_destino)

    no_raiz = grafo[no_raiz_id]
    
    if no_alvo_id != None:
        no_alvo = grafo[no_alvo_id]
    else:
        no_alvo = no_raiz

    for no in grafo.values():
        no.setCor("branco")
        no.setDis(None)
        no.setPai(None)

    no_raiz.setCor("preto")
    no_raiz.setDis(0)
    no_raiz.setPai(None)

    fila: deque[no] = deque([no_raiz])

    while fila:
        u = fila.popleft()

        for v in u.getAdj():
            v = grafo[v]
            if v.getCor() == "branco":
                v.setCor("preto")
                v.setDis(u.getDis()+1)
                v.setPai(u)
                fila.append(v)


    arvore_predecessores(no_raiz, no_alvo)
    return no_raiz

def arvore_predecessores(no_raiz, no_alvo):
    if no_raiz.getId() == no_alvo.getId():
        print(no_alvo.getId())
    elif no_alvo.pai == None:
        print(f"não há caminhos de {no_raiz.getId()} para {no_alvo.getId()}")
        return
    else:
        arvore_predecessores(no_raiz, no_alvo.getPai())
        print(no_alvo.getId())



if __name__ == "__main__":
    arvore = busca_em_largura("Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv", None, "2", "49")


    
