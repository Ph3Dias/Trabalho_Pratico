from collections import deque
import random
import polars as pl


def carregar_adjacencia_csv(
    caminho_csv: str = "Output/Parte1/maior_cfc_arestas.csv",
    separador: str = "\t",
) -> tuple[list[str], dict[str, set[str]]]:
    df = (
        pl.read_csv(
            caminho_csv,
            has_header=True,
            separator=separador,
            schema_overrides={"src": pl.String, "dst": pl.String},
        )
        .select("src", "dst")
        .drop_nulls()
        .unique()
    )

    nos_set: set[str] = set()
    adj: dict[str, set[str]] = {}

    for src, dst in df.iter_rows():
        nos_set.add(src)
        nos_set.add(dst)
        adj.setdefault(src, set()).add(dst)
        adj.setdefault(dst, set())

    nos = sorted(nos_set)
    for v in nos:
        adj.setdefault(v, set())
    return nos, adj


def clusterizacao_media_manual(nos: list[str], adj: dict[str, set[str]]) -> float:
    """Coeficiente de clusterização local médio sobre a vizinhança não direcionada
    induzida (útil para comparação rápida sem biblioteca pronta).
    """
    if not nos:
        return 0.0

    nao_dir: dict[str, set[str]] = {v: set() for v in nos}
    for u, vizs in adj.items():
        for v in vizs:
            if u != v:
                nao_dir[u].add(v)
                nao_dir[v].add(u)

    soma_c = 0.0
    for v in nos:
        viz = list(nao_dir[v])
        k = len(viz)
        if k < 2:
            continue
        ligacoes = 0
        for i in range(k):
            u = viz[i]
            for j in range(i + 1, k):
                if viz[j] in nao_dir[u]:
                    ligacoes += 1
        soma_c += (2.0 * ligacoes) / (k * (k - 1))

    return soma_c / len(nos)


def caminho_medio_bfs_manual(
    nos: list[str],
    adj: dict[str, set[str]],
    amostra_origens: int | None = None,
    seed: int = 42,
) -> float | None:
    """Calcula a distância média dos caminhos mais curtos (BFS).
    Se `amostra_origens` for definido, aproxima por amostragem de fontes.
    """
    n = len(nos)
    if n <= 1:
        return 0.0

    origens = nos
    if amostra_origens is not None and amostra_origens < n:
        rng = random.Random(seed)
        origens = rng.sample(nos, amostra_origens)

    soma_distancias = 0
    total_pares_alcancaveis = 0

    for origem in origens:
        dist: dict[str, int] = {origem: 0}
        fila: deque[str] = deque([origem])
        while fila:
            atual = fila.popleft()
            d_atual = dist[atual]
            for prox in adj[atual]:
                if prox not in dist:
                    dist[prox] = d_atual + 1
                    fila.append(prox)

        for destino, d in dist.items():
            if destino != origem:
                soma_distancias += d
                total_pares_alcancaveis += 1

    if total_pares_alcancaveis == 0:
        return None
    return soma_distancias / total_pares_alcancaveis


def avaliar_small_world_manual(
    caminho_csv: str = "Output/Parte1/maior_cfc_arestas.csv",
    amostra_origens: int | None = 500,
    num_aleatorios: int = 3,
    seed: int = 42,
) -> dict:
    nos, adj = carregar_adjacencia_csv(caminho_csv)
    n = len(nos)
    arestas_dir = [(u, v) for u, vizs in adj.items() for v in vizs]
    m = len(arestas_dir)

    c_real = clusterizacao_media_manual(nos, adj)
    l_real = caminho_medio_bfs_manual(nos, adj, amostra_origens=amostra_origens, seed=seed)

    rng = random.Random(seed)
    c_rand_list: list[float] = []
    l_rand_list: list[float] = []

    for _ in range(num_aleatorios):
        adj_rand: dict[str, set[str]] = {v: set() for v in nos}
        adicionadas = 0
        tentativas = 0
        max_tentativas = max(m * 10, 100)
        while adicionadas < m and tentativas < max_tentativas:
            u = rng.choice(nos)
            v = rng.choice(nos)
            tentativas += 1
            if u != v and v not in adj_rand[u]:
                adj_rand[u].add(v)
                adicionadas += 1

        c_rand_list.append(clusterizacao_media_manual(nos, adj_rand))
        l_rand = caminho_medio_bfs_manual(nos, adj_rand, amostra_origens=amostra_origens, seed=seed)
        if l_rand is not None:
            l_rand_list.append(l_rand)

    c_rand = sum(c_rand_list) / len(c_rand_list) if c_rand_list else 0.0
    l_rand = sum(l_rand_list) / len(l_rand_list) if l_rand_list else None

    sigma = None
    if l_real and l_rand and c_rand > 0:
        sigma = (c_real / c_rand) / (l_real / l_rand)

    return {
        "n_vertices": n,
        "n_arestas": m,
        "C_real": c_real,
        "L_real": l_real,
        "C_aleatorio_medio": c_rand,
        "L_aleatorio_medio": l_rand,
        "sigma_small_world": sigma,
        "indicio_small_world": bool(sigma is not None and sigma > 1.0 and c_real > c_rand),
    }


if __name__ == "__main__":
    print(avaliar_small_world_manual())