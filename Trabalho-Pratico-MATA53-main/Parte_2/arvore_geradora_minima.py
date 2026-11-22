from Parte_2.bfs import criar_grafo_from_csv
from Parte_2.minheap import MinHeapVertices


def _obter_peso(u, v_id: str, peso_padrao: int | float = 1) -> int | float:
    if hasattr(u, "getPeso") and callable(u.getPeso):
        try:
            peso = u.getPeso(v_id)
            if peso is not None:
                return peso
        except TypeError:
            pass
    return peso_padrao


def _construir_adjacencia_nao_direcionada(
    grafo: dict,
    peso_padrao: int | float = 1,
) -> tuple[dict[str, list[tuple[str, int | float]]], list[tuple[int | float, str, str]]]:
    """Constrói lista de adjacência não direcionada e lista única de arestas não direcionadas.
    Em arestas duplicadas/bidirecionais entre os mesmos dois vértices, mantém o menor peso.
    """
    adj: dict[str, dict[str, int | float]] = {v_id: {} for v_id in grafo}

    for u_id, u_no in grafo.items():
        for v_id in u_no.getAdj():
            if v_id not in grafo or v_id == u_id:
                continue
            w = _obter_peso(u_no, v_id, peso_padrao)
            if v_id not in adj[u_id] or w < adj[u_id][v_id]:
                adj[u_id][v_id] = w
            if u_id not in adj[v_id] or w < adj[v_id][u_id]:
                adj[v_id][u_id] = w

    adj_lista: dict[str, list[tuple[str, int | float]]] = {
        v_id: list(vizinhos.items()) for v_id, vizinhos in adj.items()
    }

    arestas: list[tuple[int | float, str, str]] = []
    visitadas: set[tuple[str, str]] = set()
    for u_id, vizinhos in adj.items():
        for v_id, w in vizinhos.items():
            par = (u_id, v_id) if u_id < v_id else (v_id, u_id)
            if par not in visitadas:
                visitadas.add(par)
                arestas.append((w, par[0], par[1]))

    return adj_lista, arestas


def prim_mst(
    caminho_csv: str,
    tamanho_csv: int,
    no_raiz: str | None = None,
    coluna_origem: str = "src",
    coluna_destino: str = "dst",
    peso_padrao: int | float = 1,
):
    """Algoritmo de Prim para Árvore/Floresta Geradora Mínima usando MinHeapVertices.

    Retorna:
        arestas_mst: lista de tuplas (u_id, v_id, peso)
        custo_total: soma dos pesos das arestas selecionadas
    """
    grafo = criar_grafo_from_csv(caminho_csv, tamanho_csv, coluna_origem, coluna_destino)
    if not grafo:
        return [], 0

    adj, _ = _construir_adjacencia_nao_direcionada(grafo, peso_padrao)

    for v in grafo.values():
        v.setPai(None)
        v.setDis(None)  # MinHeapVertices interpreta None como +inf

    raiz_id = no_raiz if no_raiz is not None else next(iter(grafo.keys()))
    if raiz_id not in grafo:
        raise KeyError(f"Vértice raiz '{raiz_id}' não encontrado no grafo.")

    heap = MinHeapVertices()
    for v_id in grafo:
        dist_inicial = 0 if v_id == raiz_id else None
        grafo[v_id].setDis(dist_inicial)
        heap.inserir(v_id, dist_inicial)

    arestas_mst: list[tuple[str, str, int | float]] = []
    custo_total: int | float = 0

    while not heap.esta_vazio():
        extraido = heap.extrair_minimo()
        if extraido is None:
            break

        _, u_id = extraido
        u_no = grafo[u_id]

        # Se u tem pai definido e distância finita, adiciona a aresta que o conectou à MST
        pai_u = u_no.getPai()
        if pai_u is not None and u_no.getDis() is not None:
            arestas_mst.append((pai_u.getId(), u_id, u_no.getDis()))
            custo_total += u_no.getDis()

        for v_id, peso in adj[u_id]:
            if heap.contem(v_id):
                v_no = grafo[v_id]
                chave_atual = v_no.getDis()
                if chave_atual is None or peso < chave_atual:
                    v_no.setDis(peso)
                    v_no.setPai(u_no)
                    heap.atualizar_distancia(v_id, peso)

    return arestas_mst, custo_total


class _UnionFind:
    def __init__(self, elementos: list[str]) -> None:
        self.pai = {x: x for x in elementos}
        self.rank = {x: 0 for x in elementos}

    def find(self, x: str) -> str:
        while self.pai[x] != x:
            self.pai[x] = self.pai[self.pai[x]]
            x = self.pai[x]
        return x

    def union(self, a: str, b: str) -> bool:
        raiz_a = self.find(a)
        raiz_b = self.find(b)
        if raiz_a == raiz_b:
            return False

        if self.rank[raiz_a] < self.rank[raiz_b]:
            self.pai[raiz_a] = raiz_b
        elif self.rank[raiz_a] > self.rank[raiz_b]:
            self.pai[raiz_b] = raiz_a
        else:
            self.pai[raiz_b] = raiz_a
            self.rank[raiz_a] += 1
        return True


def kruskal_mst(
    caminho_csv: str,
    tamanho_csv: int,
    coluna_origem: str = "src",
    coluna_destino: str = "dst",
    peso_padrao: int | float = 1,
):
    """Algoritmo de Kruskal para Árvore/Floresta Geradora Mínima usando Union-Find.

    Retorna:
        arestas_mst: lista de tuplas (u_id, v_id, peso)
        custo_total: soma dos pesos das arestas selecionadas
    """
    grafo = criar_grafo_from_csv(caminho_csv, tamanho_csv, coluna_origem, coluna_destino)
    if not grafo:
        return [], 0

    _, arestas = _construir_adjacencia_nao_direcionada(grafo, peso_padrao)
    arestas.sort(key=lambda item: item[0])

    uf = _UnionFind(list(grafo.keys()))
    arestas_mst: list[tuple[str, str, int | float]] = []
    custo_total: int | float = 0

    for peso, u_id, v_id in arestas:
        if uf.union(u_id, v_id):
            arestas_mst.append((u_id, v_id, peso))
            custo_total += peso
            if len(arestas_mst) == len(grafo) - 1:
                break

    return arestas_mst, custo_total


if __name__ == "__main__":
    caminho = "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv"

    mst_prim, custo_prim = prim_mst(caminho, 10000, no_raiz="2")
    print(f"Prim -> arestas na MST: {len(mst_prim)} | custo total: {custo_prim}")

    mst_kruskal, custo_kruskal = kruskal_mst(caminho, 10000)
    print(f"Kruskal -> arestas na MST: {len(mst_kruskal)} | custo total: {custo_kruskal}")