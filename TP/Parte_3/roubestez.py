import random
import networkx as nx
import polars as pl


def testar_robustez_remocao(
    caminho_csv: str = "Output/Parte1/maior_cfc_arestas.csv",
    fracao: float = 0.05,
    seed: int = 42,
) -> dict:
    df = (
        pl.read_csv(
            caminho_csv,
            has_header=True,
            separator="\t",
            schema_overrides={"src": pl.String, "dst": pl.String},
        )
        .select("src", "dst")
        .drop_nulls()
        .unique()
    )

    G = nx.DiGraph()
    G.add_edges_from(df.iter_rows())
    n_inicial = G.number_of_nodes()
    if n_inicial == 0:
        return {}

    def tamanho_maior_wcc(grafo: nx.DiGraph) -> int:
        if grafo.number_of_nodes() == 0:
            return 0
        return max(len(c) for c in nx.weakly_connected_components(grafo))

    k_remover = max(1, int(round(n_inicial * fracao)))
    wcc_inicial = tamanho_maior_wcc(G)

    # 3a. Remoção aleatória de 5%
    rng = random.Random(seed)
    nos_aleatorios = rng.sample(list(G.nodes()), k=min(k_remover, n_inicial))
    G_aleat = G.copy()
    G_aleat.remove_nodes_from(nos_aleatorios)
    wcc_aleat = tamanho_maior_wcc(G_aleat)

    # 3b. Remoção dos 5% mais centrais (por centralidade de grau total)
    centralidade = nx.degree_centrality(G)
    nos_centrais = [
        no
        for no, _ in sorted(
            centralidade.items(), key=lambda item: item[1], reverse=True
        )[:k_remover]
    ]
    G_centrais = G.copy()
    G_centrais.remove_nodes_from(nos_centrais)
    wcc_centrais = tamanho_maior_wcc(G_centrais)

    return {
        "n_inicial": n_inicial,
        "nos_removidos": k_remover,
        "maior_wcc_inicial": wcc_inicial,
        "maior_wcc_apos_aleatoria_5pct": wcc_aleat,
        "fracao_preservada_aleatoria": wcc_aleat / wcc_inicial,
        "maior_wcc_apos_centrais_5pct": wcc_centrais,
        "fracao_preservada_centrais": wcc_centrais / wcc_inicial,
    }


if __name__ == "__main__":
    print(testar_robustez_remocao())