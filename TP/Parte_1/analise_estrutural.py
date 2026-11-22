import polars as pl
import csv 
import matplotlib.pyplot as plt
import networkx as nx
import igraph as ig

def calcular_grau_por_vertice(caminho_entrada, separador_entrada, caminho_saida, separador_saida):

    arestas = pl.read_csv(
        caminho_entrada,
        separator=separador_entrada,  
        has_header=True,
        new_columns=["src", "dst"],
        schema_overrides={"src": pl.Int64, "dst": pl.Int64},
    )

    # Conta grau de saída e grau de entrada
    out_deg = (
        arestas.group_by("src")
        .len()
        .rename({"src": "vertice", "len": "out_degree"})
    )

    in_deg = (
        arestas.group_by("dst")
        .len()
        .rename({"dst": "vertice", "len": "in_degree"})
    )

    #  Vértices únicos aparecem, preenchendo zeros onde faltar
    todos_vertices = (
        pl.select(pl.concat([arestas["src"], arestas["dst"]]).alias("vertice"))
        .unique()
    )

    df_graus = (
        todos_vertices.join(out_deg, on="vertice", how="left")
        .join(in_deg, on="vertice", how="left")
        .with_columns([
            pl.col("out_degree").fill_null(0),
            pl.col("in_degree").fill_null(0),
        ])
        .sort("vertice", descending=False)
    )

    
    df_graus.write_csv(
            caminho_saida,
            separator=separador_saida,
            include_header=True,
        )

def calcular_grau_minimo_e_maximo(caminho_entrada, separador_entrada):

    df = pl.read_csv(
            caminho_entrada,
            separator=separador_entrada,  
            has_header=True,
            new_columns=["vertice", "in_degree", "out_degree"],
            schema_overrides={"src": pl.Int64, "dst": pl.Int64},
        )

    return df["in_degree"].min(), df["in_degree"].max(), df["out_degree"].min(), df["out_degree"].max()

def gerar_distribuicao(coluna):
    df = pl.read_csv(
                "Output/Parte1/vertices_graus.csv",
                separator="\t",  
                has_header=True,
                new_columns=["vertice", "in_degree", "out_degree"],
                schema_overrides={"src": pl.Int64, "dst": pl.Int64},
            )

    ocorrencias: dict[int, int]={}

    for linha in df[coluna]:
        ocorrencias[linha] = ocorrencias.get(linha, 0) + 1

    
    ocorrencias = dict(sorted(ocorrencias.items()))
    path_saida_csv = f'Output/Parte1/distribuicao_{coluna}.csv'
    with open(path_saida_csv, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f, delimiter="\t")
        escritor.writerow(["grau", "ocorrencia"])
        for grau, qtd in sorted(ocorrencias.items()):
            escritor.writerow([grau, qtd])

def calcular_grau_medio_e_densidade(coluna):

    df = pl.read_csv(
        f"Output/Parte1/distribuicao_{coluna}.csv",
        separator="\t",  
        has_header=True,
        new_columns=["grau", "ocorrencia"],
        schema_overrides={"grau": pl.Int64, "ocorrencia": pl.Int64},
    )
    somatorio_graus_por_ocorrencia = df.select((pl.col("grau")*pl.col("ocorrencia")).sum()).item()
    qtd_vertices = df.select((pl.col('ocorrencia')).sum()).item()

    densidade = 3309592/(qtd_vertices*(qtd_vertices-1))
    return somatorio_graus_por_ocorrencia/qtd_vertices, densidade


def desenhar_grafico_distribuicao(coluna):
    
    caminho_arquivo = f"Output/Parte1/Graficos/grafico_distribuicao_{coluna}.png"

    df = (
        pl.read_csv(
            f"Output/Parte1/distribuicao_{coluna}.csv",
            separator="\t",
            schema_overrides={"grau": pl.Float64, "ocorrencia": pl.Float64},
        )
        .drop_nulls(subset=["grau", "ocorrencia"])
        .sort("grau")
    )

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.4))

    # Esquerda: eixo X em symlog (permite grau = 0) e eixo Y em log
    axes[0].scatter(
        df["grau"],
        df["ocorrencia"],
        s=18,
        alpha=0.7,
        color="#1f77b4",
        edgecolors="none",
    )
    axes[0].set_xscale("symlog", linthresh=1)
    axes[0].set_yscale("log")
    axes[0].set_title(f"Distribuição de {coluna} (Eixo X Symlog / Eixo Y Log)")
    axes[0].set_xlabel("Grau de saída (grau)" if coluna == "out_degree" else "Grau de entrada (grau)")
    axes[0].set_ylabel("Ocorrência (log)")
    axes[0].grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.4)

    # Direita: escala linear completa (inclui grau = 0)
    axes[1].scatter(
        df["grau"],
        df["ocorrencia"],
        s=18,
        alpha=0.7,
        color="#d95f02",
        edgecolors="none",
    )
    axes[1].set_title(f"Distribuição de {coluna} (Escala Linear)")
    axes[1].set_xlabel("Grau de saída (grau)" if coluna == "out_degree" else "Grau de entrada (grau)")
    axes[1].set_ylabel("Ocorrência")
    axes[1].grid(True, linestyle="--", linewidth=0.5, alpha=0.4)

    plt.suptitle(
        f"Gráfico de Pontos — distribuicao_{coluna}.csv",
        fontsize=13,
        fontweight="bold",
    )
    plt.tight_layout()
    plt.savefig(caminho_arquivo, dpi=200)
    plt.show()


def calcular_n_cfc(
    caminho_entrada,
    caminho_arestas_maior_cfc: str = "Output/Parte1/maior_cfc_arestas.csv"
    
) -> tuple[int, set[str], int, int]:
    arestas = (
        pl.read_csv(
            caminho_entrada,
            has_header=True,
            separator="\t",
            new_columns=["src", "dst"],
        )
        .select(
            pl.col("src").cast(pl.String),
            pl.col("dst").cast(pl.String),
        )
        .drop_nulls()
        .unique()
    )

    grafo = nx.DiGraph()
    grafo.add_edges_from(arestas.iter_rows())

    cfcs = list(nx.strongly_connected_components(grafo))
    num_componentes = len(cfcs)

    if not cfcs:
        pl.DataFrame(schema={"src": pl.String, "dst": pl.String}).write_csv(
            caminho_arestas_maior_cfc,
            include_header=True,
            separator="\t",
        )
        return 0, set(), 0, 0

    maior_cfc = max(cfcs, key=len)
    lista_maior_scc = list(maior_cfc)

    arestas_maior_cfc = arestas.filter(
        pl.col("src").is_in(lista_maior_scc) & pl.col("dst").is_in(lista_maior_scc)
    )

    # Ordena por src e dst (numérico quando possível, mantendo src e dst como String)
    try:
        arestas_maior_cfc = (
            arestas_maior_cfc.with_columns(
                pl.col("src").cast(pl.Int64).alias("_src_ord"),
                pl.col("dst").cast(pl.Int64).alias("_dst_ord"),
            )
            .sort(["_src_ord", "_dst_ord"])
            .drop(["_src_ord", "_dst_ord"])
        )
    except pl.exceptions.InvalidOperationError:
        arestas_maior_cfc = arestas_maior_cfc.sort(["src", "dst"])

    arestas_maior_cfc.write_csv(
        caminho_arestas_maior_cfc,
        include_header=True,
        separator="\t",
    )

    qtd_vertices = len(maior_cfc)
    qtd_arestas = arestas_maior_cfc.height

    return num_componentes, maior_cfc, qtd_vertices, qtd_arestas


def visualizar_grafo_completo_de_csv(
    caminho_arquivo: str,
    n_linhas: int | None = None,
    caminho_imagem: str = "grafo_completo.png",
    layout_nome: str = "fr",
    coluna_origem: str = "src",
    coluna_destino: str = "dst",
    cabecalho: bool = True,
    separador: str = "\t",
):
    """Lê as arestas do arquivo com Polars (opcionalmente limitando a `n_linhas`
    linhas), monta o grafo direcionado inteiro no NetworkX e gera a visualização
    com `igraph`.
    """
    # 1. Lê o arquivo (limitando a quantidade de linhas se `n_linhas` for informado)
    if cabecalho:
        arestas = pl.read_csv(
            caminho_arquivo,
            separator=separador,
            n_rows=n_linhas,
        )
    else:
        arestas = pl.read_csv(
            caminho_arquivo,
            separator=separador,
            n_rows=n_linhas,
            has_header=False,
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

    if arestas.height == 0:
        raise ValueError("Nenhuma aresta válida encontrada no arquivo.")

    # 2. Monta o grafo direcionado completo das arestas lidas
    grafo_nx = nx.DiGraph()
    grafo_nx.add_edges_from(arestas.iter_rows())

    # 3. Converte para igraph e renderiza o grafo inteiro
    grafo_ig = ig.Graph.from_networkx(grafo_nx)

    rotulos = (
        [str(x) for x in grafo_ig.vs["_nx_name"]]
        if "_nx_name" in grafo_ig.vs.attributes()
        else [str(i) for i in range(grafo_ig.vcount())]
    )

    # Em grafos grandes, ocultar rótulos e usar nós/setas menores evita borrão total
    mostrar_rotulos = grafo_ig.vcount() <= 80
    layout = grafo_ig.layout(layout_nome)

    ig.plot(
        grafo_ig,
        target=caminho_imagem,
        layout=layout,
        bbox=(1600, 1200),
        margin=40,
        vertex_size=12 if mostrar_rotulos else 4,
        vertex_color="steelblue",
        vertex_label=rotulos if mostrar_rotulos else None,
        vertex_label_size=8,
        edge_arrow_size=0.2 if not mostrar_rotulos else 0.7,
        edge_color="rgba(120, 120, 120, 0.45)",
    )

    return grafo_ig

def calcular_diametro_raio_caminho_medio(
    caminho_csv: str = "Output/Parte1/maior_cfc_arestas.csv",
    coluna_origem: str = "src",
    coluna_destino: str = "dst",
    separador: str = "\t",
) -> tuple[int | None, int | None, float | None]:
    """Retorna (diametro, raio, comprimento_medio_caminhos) usando NetworkX."""
    arestas = (
        pl.read_csv(
            caminho_csv,
            has_header=True,
            separator=separador,
            schema_overrides={
                coluna_origem: pl.String,
                coluna_destino: pl.String,
            },
        )
        .select(coluna_origem, coluna_destino)
        .drop_nulls()
        .unique()
    )

    grafo = nx.DiGraph()
    grafo.add_edges_from(arestas.iter_rows())

    if grafo.number_of_nodes() == 0:
        return None, None, None

    if grafo.number_of_nodes() == 1:
        return 0, 0, 0.0

    diametro = nx.diameter(grafo)
    raio = nx.radius(grafo)
    comprimento_medio = nx.average_shortest_path_length(grafo)

    return diametro, raio, comprimento_medio


def calcular_clusterizacao_media(
    caminho_csv: str = "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
    coluna_origem: str = "src",
    coluna_destino: str = "dst",
    separador: str = "\t",
) -> float | None:

    arestas = (
        pl.read_csv(
            caminho_csv,
            has_header=True,
            separator=separador,
            schema_overrides={
                coluna_origem: pl.String,
                coluna_destino: pl.String,
            },
        )
        .select(coluna_origem, coluna_destino)
        .drop_nulls()
        .unique()
    )

    grafo = nx.DiGraph()
    grafo.add_edges_from(arestas.iter_rows())

    if grafo.number_of_nodes() == 0:
        return None

    return nx.average_clustering(grafo)


if __name__ == "__main__":
    print(calcular_clusterizacao_media())