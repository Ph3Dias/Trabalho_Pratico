from collections import deque
import math
import random


def _extrair_adjacencia_nao_direcionada(grafo) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = {}
    itens = grafo.values() if hasattr(grafo, "values") else grafo.items()

    nos_ids = set()
    bruto: dict[str, list[str]] = {}

    for item in itens:
        if hasattr(item, "getId") and hasattr(item, "getAdj"):
            u_id = item.getId()
            vizinhos = list(item.getAdj())
        else:
            u_id, vizinhos = item
        nos_ids.add(u_id)
        bruto[u_id] = vizinhos

    for u_id in nos_ids:
        adj[u_id] = set()

    for u_id, vizinhos in bruto.items():
        for v_id in vizinhos:
            if v_id in nos_ids and v_id != u_id:
                adj[u_id].add(v_id)
                adj[v_id].add(u_id)

    return adj


def calcular_clustering_medio(adj: dict[str, set[str]], amostra_nos: int | None = None, seed: int = 42) -> float:

    nos = list(adj.keys())
    if not nos:
        return 0.0

    if amostra_nos is not None and amostra_nos < len(nos):
        rng = random.Random(seed)
        nos = rng.sample(nos, amostra_nos)

    soma_c = 0.0
    contados = 0

    for u in nos:
        viz = list(adj[u])
        k = len(viz)
        if k < 2:
            soma_c += 0.0
            contados += 1
            continue

        ligacoes_entre_vizinhos = 0
        for i in range(k):
            vi = viz[i]
            adj_vi = adj[vi]
            for j in range(i + 1, k):
                if viz[j] in adj_vi:
                    ligacoes_entre_vizinhos += 1

        max_ligacoes = k * (k - 1) / 2
        soma_c += ligacoes_entre_vizinhos / max_ligacoes
        contados += 1

    return soma_c / contados if contados > 0 else 0.0


def calcular_caminho_medio_bfs(adj: dict[str, set[str]], amostra_origens: int | None = 200, seed: int = 42) -> float:

    nos = list(adj.keys())
    n = len(nos)
    if n < 2:
        return 0.0

    if amostra_origens is not None and amostra_origens < n:
        rng = random.Random(seed)
        origens = rng.sample(nos, amostra_origens)
    else:
        origens = nos

    soma_distancias = 0
    total_pares = 0

    for origem in origens:
        distancias = {origem: 0}
        fila = deque([origem])

        while fila:
            atual = fila.popleft()
            d_atual = distancias[atual]
            for viz in adj[atual]:
                if viz not in distancias:
                    distancias[viz] = d_atual + 1
                    fila.append(viz)

        for destino, dist in distancias.items():
            if destino != origem:
                soma_distancias += dist
                total_pares += 1

    return soma_distancias / total_pares if total_pares > 0 else 0.0


def calcular_small_world(
    grafo,
    amostra_clustering: int | None = 5000,
    amostra_bfs: int | None = 200,
    seed: int = 42,
) -> dict[str, float | int | bool]:

    adj = _extrair_adjacencia_nao_direcionada(grafo)
    n = len(adj)
    if n < 2:
        return {
            "N": n,
            "grau_medio": 0.0,
            "C": 0.0,
            "L": 0.0,
            "C_rand": 0.0,
            "L_rand": 0.0,
            "sigma": 0.0,
            "indicio_small_world": False,
        }

    grau_medio = sum(len(viz) for viz in adj.values()) / n
    c_real = calcular_clustering_medio(adj, amostra_nos=amostra_clustering, seed=seed)
    l_real = calcular_caminho_medio_bfs(adj, amostra_origens=amostra_bfs, seed=seed)

    c_rand = (grau_medio / n) if n > 0 else 0.0
    l_rand = (math.log(n) / math.log(grau_medio)) if grau_medio > 1 else 0.0

    if c_rand > 0 and l_rand > 0 and l_real > 0:
        sigma = (c_real / c_rand) / (l_real / l_rand)
    else:
        sigma = 0.0

    indicio = (c_real > c_rand) and (sigma > 1.0)

    return {
        "N": n,
        "grau_medio": grau_medio,
        "C": c_real,
        "L": l_real,
        "C_rand": c_rand,
        "L_rand": l_rand,
        "sigma": sigma,
        "indicio_small_world": indicio,
    }


if __name__ == "__main__":

    grafo_exemplo = {
        "A": ["B", "C", "D"],
        "B": ["A", "C", "E"],
        "C": ["A", "B", "D"],
        "D": ["A", "C", "F"],
        "E": ["B", "F"],
        "F": ["D", "E"],
    }
    resultado = calcular_small_world(grafo_exemplo, amostra_clustering=None, amostra_bfs=None)
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")