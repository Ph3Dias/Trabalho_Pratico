import polars as pl
from Parte_2.no import no 
from Parte_2.bfs import criar_grafo_from_csv
from Parte_2.bellman_ford import relaxa
from Parte_2.minheap import MinHeapVertices


def dijkstra_forcado(
    caminho_csv: str,
    tamanho_csv: int,
    no_raiz: str,
    coluna_origem: str = "src",
    coluna_destino: str = "dst",
):
    grafo = criar_grafo_from_csv(caminho_csv, tamanho_csv, coluna_origem, coluna_destino)

    if no_raiz not in grafo:
        raise KeyError(f"Vértice raiz '{no_raiz}' não encontrado no grafo.")

    for v in grafo.values():
        v.setPai(None)
        v.setDis(float("inf"))

    raiz = grafo[no_raiz]
    raiz.setDis(0)

    q = MinHeapVertices()
    s = []
    for v in grafo.values():
        q.inserir(v.getId(), v.getDis())

    while not q.esta_vazio():
        extraido = q.extrair_minimo()
        if extraido is None:
            break

        _, u_id = extraido
        u = grafo[u_id]
        s.append(u.getId())

        for v in u.getAdj():
            v = grafo[v]
            relaxado = relaxa(u, v, w=1)

            if relaxado:
                q.atualizar_distancia(v.getId(), v.getDis())

    return grafo
if __name__ =='__main__':
    grafo = dijkstra_forcado("Output/Parte1/maior_cfc_arestas.csv", None, "2")
    print(grafo["2"].getDis(), grafo["1138648"].getDis())