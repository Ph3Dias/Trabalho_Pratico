from collections import deque
import polars as pl
from Parte_2.bfs import criar_grafo_from_csv


def _carregar_mapa_graus(
    caminho_csv: str,
    coluna_vertice: str,
    coluna_grau: str,
    tamanho_csv: int | None = None,
) -> dict[str, int]:
    
    df = pl.read_csv(caminho_csv, separator="\t", dtypes={coluna_vertice: pl.Utf8})
    if tamanho_csv is not None:
        df = df.slice(0, tamanho_csv)

    mapa: dict[str, int] = {}
    for vertice, grau in zip(df[coluna_vertice].to_list(), df[coluna_grau].to_list()):
        if vertice is None or grau is None:
            continue
        v_id = str(vertice)
        mapa[v_id] = mapa.get(v_id, 0) + int(grau)
    return mapa


def _eh_fortemente_conexo_ativos(
    vertices_ativos: set[str],
    adj_dir: dict[str, list[str]],
) -> bool:

    if len(vertices_ativos) <= 1:
        return True

    inicio = next(iter(vertices_ativos))

    def alcancaveis(origem: str, grafo_adj: dict[str, list[str]]) -> set[str]:
        visitados: set[str] = {origem}
        fila: deque[str] = deque([origem])
        while fila:
            atual = fila.popleft()
            for prox in grafo_adj.get(atual, ()):
                if prox in vertices_ativos and prox not in visitados:
                    visitados.add(prox)
                    fila.append(prox)
        return visitados

    if len(alcancaveis(inicio, adj_dir)) != len(vertices_ativos):
        return False

    adj_rev: dict[str, list[str]] = {v: [] for v in vertices_ativos}
    for u in vertices_ativos:
        for v in adj_dir.get(u, ()):
            if v in vertices_ativos:
                adj_rev[v].append(u)

    return len(alcancaveis(inicio, adj_rev)) == len(vertices_ativos)


def _eh_fracamente_conexo_ativos(
    vertices_ativos: set[str],
    adj_dir: dict[str, list[str]],
) -> bool:

    if len(vertices_ativos) <= 1:
        return True

    adj_nao_dir: dict[str, set[str]] = {v: set() for v in vertices_ativos}
    for u in vertices_ativos:
        for v in adj_dir.get(u, ()):
            if v in vertices_ativos and u != v:
                adj_nao_dir[u].add(v)
                adj_nao_dir[v].add(u)

    inicio = next(iter(vertices_ativos))
    visitados: set[str] = {inicio}
    fila: deque[str] = deque([inicio])

    while fila:
        atual = fila.popleft()
        for prox in adj_nao_dir[atual]:
            if prox not in visitados:
                visitados.add(prox)
                fila.append(prox)

    return len(visitados) == len(vertices_ativos)


def verificar_eulerianidade_por_graus(
    caminho_csv_grau_entrada: str,
    caminho_csv_grau_saida: str,
    caminho_csv_arestas: str,
    tamanho_csv_arestas: int,
    coluna_vertice_entrada: str = "vertice",
    coluna_grau_entrada: str = "grau_entrada",
    coluna_vertice_saida: str = "vertice",
    coluna_grau_saida: str = "grau_saida",
    coluna_origem: str = "src",
    coluna_destino: str = "dst",
    tamanho_csv_graus: int | None = None,
) -> dict:

    grau_entrada = _carregar_mapa_graus(
        caminho_csv_grau_entrada,
        coluna_vertice_entrada,
        coluna_grau_entrada,
        tamanho_csv_graus,
    )
    grau_saida = _carregar_mapa_graus(
        caminho_csv_grau_saida,
        coluna_vertice_saida,
        coluna_grau_saida,
        tamanho_csv_graus,
    )

    grafo = criar_grafo_from_csv(
        caminho_csv_arestas,
        tamanho_csv_arestas,
        coluna_origem,
        coluna_destino,
    )

    todos_vertices = set(grau_entrada) | set(grau_saida) | set(grafo.keys())
    if not todos_vertices:
        return {
            "tipo": "vazio",
            "tem_circuito": False,
            "tem_caminho": False,
            "detalhes": "Nenhum vértice encontrado.",
        }

    g_in = {v: grau_entrada.get(v, 0) for v in todos_vertices}
    g_out = {v: grau_saida.get(v, 0) for v in todos_vertices}

    total_grau_entrada = sum(g_in.values())
    total_grau_saida = sum(g_out.values())

    if total_grau_entrada == 0 and total_grau_saida == 0:
        return {
            "tipo": "vazio",
            "tem_circuito": False,
            "tem_caminho": False,
            "detalhes": "Grafo sem arestas (todos os graus de entrada e saída são 0).",
        }

    if total_grau_entrada != total_grau_saida:
        return {
            "tipo": "nao_euleriano",
            "tem_circuito": False,
            "tem_caminho": False,
            "detalhes": (
                f"Soma dos graus de entrada ({total_grau_entrada}) difere da soma "
                f"dos graus de saída ({total_grau_saida})."
            ),
        }

    adj_dir: dict[str, list[str]] = {v: [] for v in todos_vertices}
    for u_id, u_no in grafo.items():
        if u_id in adj_dir:
            adj_dir[u_id] = [v_id for v_id in u_no.getAdj() if v_id in adj_dir]

    vertices_ativos = {v for v in todos_vertices if g_in[v] > 0 or g_out[v] > 0}

    # 1. Circuito euleriano
    if all(g_in[v] == g_out[v] for v in todos_vertices):
        if _eh_fortemente_conexo_ativos(vertices_ativos, adj_dir):
            return {
                "tipo": "circuito_euleriano",
                "tem_circuito": True,
                "tem_caminho": True,
                "detalhes": "Todos os vértices têm grau de entrada igual ao grau de saída e os vértices ativos são fortemente conexos.",
            }
        return {
            "tipo": "nao_euleriano",
            "tem_circuito": False,
            "tem_caminho": False,
            "detalhes": "Os graus são balanceados, mas os vértices ativos não formam uma única componente fortemente conexa.",
        }

    # 2. Caminho euleriano
    inicios: list[str] = []
    fins: list[str] = []
    for v in todos_vertices:
        diff = g_out[v] - g_in[v]
        if diff == 1:
            inicios.append(v)
        elif diff == -1:
            fins.append(v)
        elif diff != 0:
            return {
                "tipo": "nao_euleriano",
                "tem_circuito": False,
                "tem_caminho": False,
                "detalhes": f"Vértice '{v}' tem diferença grau_saida - grau_entrada = {diff} (esperado -1, 0 ou +1).",
            }

    if len(inicios) == 1 and len(fins) == 1:
        if _eh_fracamente_conexo_ativos(vertices_ativos, adj_dir):
            return {
                "tipo": "caminho_euleriano",
                "tem_circuito": False,
                "tem_caminho": True,
                "detalhes": f"Caminho euleriano possível iniciando em '{inicios[0]}' e terminando em '{fins[0]}'.",
            }
        return {
            "tipo": "nao_euleriano",
            "tem_circuito": False,
            "tem_caminho": False,
            "detalhes": "As diferenças de grau indicam caminho euleriano, mas os vértices ativos não são fracamente conexos.",
        }

    return {
        "tipo": "nao_euleriano",
        "tem_circuito": False,
        "tem_caminho": False,
        "detalhes": f"Encontrados {len(inicios)} vértices com (out - in = +1) e {len(fins)} com (out - in = -1) (esperado 1 e 1).",
    }