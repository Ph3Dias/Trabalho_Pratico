from Parte_2.no import no
from Parte_2.bfs import criar_grafo_from_csv

def floyd_warshall_forcado(
    caminho_csv,
    tamanho_csv,
    coluna_origem="src",
    coluna_destino="dst",
    peso_padrao = 1
):

    # Floyd-Warshall in-place
    grafo = criar_grafo_from_csv(caminho_csv, tamanho_csv, coluna_origem, coluna_destino)
    ids = list(grafo.keys())

    lista_id_indice = {vert_id: idx for idx, vert_id in enumerate(ids)}
    n = len(ids)
    
    inf = float("inf")

    
    matriz_d = [[inf] * n for _ in range(n)]
    
    for i in range(n):
        matriz_d[i][i] = 0

    for u_id, u_no in grafo.items():
        i = lista_id_indice[u_id]
        for v_id in u_no.getAdj():

            j = lista_id_indice[v_id]
            if peso_padrao < matriz_d[i][j]:
                matriz_d[i][j] = peso_padrao

    for k in range(n):
        dist_k = matriz_d[k]
        for i in range(n):
            dik = matriz_d[i][k]
            if dik == inf:
                continue
            dist_i = matriz_d[i]
            for j in range(n):
                dkj = dist_k[j]
                if dkj != inf and dik + dkj < dist_i[j]:
                    dist_i[j] = dik + dkj


    return ids, matriz_d


if __name__ == '__main__':
    ids, matriz = floyd_warshall_forcado("Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv", 1000)
    print(matriz)

    
    