import polars as pl
from Parte_2.no import no
from collections import deque
from Parte_2.bfs import criar_grafo_from_csv, arvore_predecessores


def busca_em_profundidade_iterativa(
    caminho_csv,
    tamanho_csv,
    coluna_origem="src",
    coluna_destino="dst",
):
    grafo = criar_grafo_from_csv(caminho_csv, tamanho_csv, coluna_origem, coluna_destino)

    for vertice in grafo.values():
        vertice.setCor("branco")
        vertice.setPai(None)

    tempo = 0

    for raiz in grafo.values():
        if raiz.getCor() != "branco":
            continue

        tempo += 1
        raiz.setInicio(tempo)
        raiz.setCor("cinza")

        # Cada elemento da pilha guarda (vertice_atual, iterador_dos_vizinhos)
        pilha = [(raiz, iter(raiz.getAdj()))]

        while pilha:
            u, vizinhos = pilha[-1]

            try:
                v_id = next(vizinhos)
                v = grafo[v_id]

                if v.getCor() == "branco":
                    v.setPai(u)
                    tempo += 1
                    v.setInicio(tempo)
                    v.setCor("cinza")
                    pilha.append((v, iter(v.getAdj())))

            except StopIteration:
                # Todos os adjacentes de 'u' foram explorados: finaliza 'u'
                pilha.pop()
                tempo += 1
                u.setFim(tempo)
                u.setCor("preto")

    return grafo

def reconstruir_caminho(grafo, origem_id, destino_id):
    if origem_id not in grafo or destino_id not in grafo:
        return None

    origem = grafo[origem_id]
    atual = grafo[destino_id]
    caminho = []

    while atual is not None:
        caminho.append(atual)
        if atual is origem:
            break
        atual = atual.getPai()

    # Se não chegamos até 'origem', não há caminho na árvore DFS a partir dela
    if not caminho or caminho[-1] is not origem:
        return None

    caminho.reverse()
    return caminho


def imprimir_caminho(grafo, origem_id, destino_id):
    caminho = reconstruir_caminho(grafo, origem_id, destino_id)
    if caminho is None:
        print(f"Não há caminho de '{origem_id}' até '{destino_id}' na árvore DFS.")
        return

    # Se sua classe 'no' tiver getId() ou getValor(), use o método correspondente;
    # caso contrário, ajuste conforme os atributos/métodos de 'no'.
    rotulos = [str(getattr(n, "id", getattr(n, "getId", lambda: n)())) for n in caminho]
    print(" -> ".join(rotulos))

if __name__ == "__main__":
    grafo = busca_em_profundidade_iterativa("Output/Parte1/maior_cfc_arestas.csv", None)
    imprimir_caminho(grafo, "2", "1138648")