import polars as pl
from Parte_2.no import no
from collections import deque
from Parte_2.bfs import criar_grafo_from_csv, arvore_predecessores


def tarjan_com_dfs(
    caminho_csv,
    tamanho_csv,
    coluna_origem="src",
    coluna_destino="dst",
):
    grafo = criar_grafo_from_csv(caminho_csv, tamanho_csv, coluna_origem, coluna_destino)

    tempo = 0
    indices: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    pilha: list[str] = []
    na_pilha: set[str] = set()
    componentes: list[list[str]] = []

    for no_atual in grafo.values():
        no_atual.setCor("branco")
        no_atual.setPai(None)

    for raiz in grafo.values():
        if raiz.getCor() != "branco":
            continue

        tempo += 1
        raiz_id = raiz.getId()
        raiz.setInicio(tempo)
        raiz.setCor("cinza")

        indices[raiz_id] = tempo
        lowlink[raiz_id] = tempo

        pilha.append(raiz_id)
        na_pilha.add(raiz_id)

        # Cada item é (no_atual, iterador_de_vizinhos)
        pilha_dfs = [(raiz, iter(raiz.getAdj()))]

        while pilha_dfs:
            u, adj_iter = pilha_dfs[-1]
            u_id = u.getId()

            try:
                v_id = next(adj_iter)
                if v_id not in grafo:
                    continue

                v = grafo[v_id]
                if v.getCor() == "branco":
                    tempo += 1
                    v.setInicio(tempo)
                    v.setCor("cinza")
                    v.setPai(u)

                    indices[v_id] = tempo
                    lowlink[v_id] = tempo

                    pilha.append(v_id)
                    na_pilha.add(v_id)

                    pilha_dfs.append((v, iter(v.getAdj())))
                elif v_id in na_pilha:
                    if indices[v_id] < lowlink[u_id]:
                        lowlink[u_id] = indices[v_id]

            except StopIteration:
                pilha_dfs.pop()

                tempo += 1
                u.setFim(tempo)
                u.setCor("preto")

                if pilha_dfs:
                    pai_no, _ = pilha_dfs[-1]
                    pai_id = pai_no.getId()
                    if lowlink[u_id] < lowlink[pai_id]:
                        lowlink[pai_id] = lowlink[u_id]

                if lowlink[u_id] == indices[u_id]:
                    cfc: list[str] = []
                    while True:
                        w_id = pilha.pop()
                        na_pilha.remove(w_id)
                        cfc.append(w_id)
                        if w_id == u_id:
                            break
                    componentes.append(cfc)

    return componentes, grafo


if __name__ == "__main__":
    cfcs, grafo = tarjan_com_dfs(
        "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
        1000000,
    )
    print(f"Total de CFCs: {len(cfcs)}")
    print("Maiores CFCs:", sorted(cfcs, key=len, reverse=True)[:5])