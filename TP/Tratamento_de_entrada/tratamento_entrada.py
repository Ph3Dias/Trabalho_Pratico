import polars as pl

def snap_temporal_para_snap_estatico(caminho_aresta, separador_entrada, caminho_saida, separador_saida, header_entrada=False):
    df_arestas = (
        pl.read_csv(
            caminho_aresta,
            separator=separador_entrada,
            comment_prefix="#",
            has_header=header_entrada,
            new_columns=["src", "dst", "epoch"],
            schema_overrides={"src": pl.Int64, "dst": pl.Int64, "epoch": pl.Int64},
        )
        # Remove o timestamp, elimina pares (src, dst) duplicados e ordena por src e dst
        .select(["src", "dst"])
        .unique(subset=["src", "dst"], maintain_order=False)
        .sort(["src", "dst"], descending=[False, False])
    )

    # Salva em arquivo .csv
    df_arestas.write_csv(
        caminho_saida,
        separator=separador_saida,
        include_header=True,
    )


def contar_vertices(caminho_aresta, separador_entrada, caminho_saida, separador_saida, n_linhas,header_entrada=True):

    # Função meramente utilizada para confirmar a quantidade de vértices fornecidas no site

    df = pl.read_csv(
        caminho_aresta,
        separator=separador_entrada,
        comment_prefix="#",
        has_header=header_entrada,
        new_columns=["src", "dst"],
        n_rows=n_linhas,
        schema_overrides={"src": pl.Int64, "dst": pl.Int64},
    )

    # Junta src e dst em uma única coluna, remove duplicatas e ordena em ordem crescente
    df_vertices = (
        pl.select(pl.concat([df["src"], df["dst"]]).alias("vertice"))
        .unique(subset=["vertice"], maintain_order=False)
        .sort("vertice", descending=False)
    )

    # Salva em arquivo .csv
    df_vertices.write_csv(
        caminho_saida,
        separator=separador_saida,
        include_header=True,
    )

    return df_vertices
if __name__== '__main__':



    df_vertices = contar_vertices(
        "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
        '\t',
        "Output/Tratamento_de_entrada/vertices_grafo_ordenado.csv",
        '\t', 10000
    )

    print(len(df_vertices))

    
