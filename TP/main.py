from Tratamento_de_entrada.tratamento_entrada import *
from Parte_1.analise_estrutural import *
from Parte_2.arvore_geradora_minima import *
from Parte_2.bfs import *
from Parte_2.bellman_ford import *
from Parte_2.dfs import *
from Parte_2.dijkstra import *
from Parte_2.floyd_warshall import *
from Parte_2.minheap import *
from Parte_2.no import *
from Parte_2.tarjan import *
from Parte_2.verificacao_eulerianidade import *
from Parte_3 import *

mostrar_menu= True
while True:
    if mostrar_menu:
        print("Selecione o algoritmo digitando o número correspondente:")
        print(
            "1 - Realizar tratamento no grafo de entrada (wiki-talk-temporal.txt)\n"
            + "Obs: o tempo de execução desse método pode demorar bastante, então utilize apenas "
            + "quando os arquivos csv básicos de entrada não estiverem presentes na pasta Output"
        )
        print("2 - Árvore Geradora Mínima (Aplicada no Grafo Completo Wiki-Talk)")
        print("3 - Bellman-Ford (bellman_ford)")
        print("4 - Busca em Largura / BFS (bfs)")
        print("5 - Busca em Profundidade / DFS (dfs)")
        print("6 - Dijkstra (dijkstra)")
        print("7 - Floyd-Warshall (floyd_warshall)")
        print("8 - Componentes Fortemente Conexas / Tarjan (tarjan)")
        print("0 - Sair")
        print()
        mostrar_menu = False

    
    opcao = input("Digite sua escolha: ").strip()
    if opcao == "0":
        break


    match opcao:
        case "h":
            mostrar_menu= True
        case "1":
            snap_temporal_para_snap_estatico(
                    "Dataset/wiki-talk-temporal.txt",
                    ' ',
                    "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
                    '\t')
            print("Confira a pasta Output/Tratamento_de_entrada/")

        
            df_vertices = contar_vertices(
                                "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
                                '\t',
                                "Output/Tratamento_de_entrada/vertices_grafo_ordenado.csv",
                                '\t'
                            )

            print("Confira a pasta Output/Tratamento_de_entrada/")
        
            calcular_grau_por_vertice(
                "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
                "\t",
                "Output/Parte1/graus_vertices.csv",
                "\t")

            print("Confira a pasta Output/Parte1/")


            in_deg_min, in_deg_max, out_deg_min, out_deg_max = calcular_grau_minimo_e_maximo(
                "Output/Parte1/vertices_graus.csv","\t")

            print(f"Mínimo In-degree {in_deg_min}\n Máximo In-degree {in_deg_max}\n, Mínimo Out-degree {out_deg_min}\n Máximo Out-degree{out_deg_max}")

        
            gerar_distribuicao("in_degree")
            gerar_distribuicao("out_degree")


        
            grau_med_in, desindade_in = calcular_grau_medio_e_densidade("in_degree")
            grau_med_out,densidade_out = calcular_grau_medio_e_densidade("out_degree")

            print(f"Grau médio de Entrada {grau_med_in}\nGrau médio de Saída {grau_med_out}")
            print(desindade_in)
            print("Confira a pasta Output/Parte1")

            desenhar_grafico_distribuicao("in_degree")
            desenhar_grafico_distribuicao("out_degree")

            print("Confira a pasta Output/Graficos")

            num_cfc, maior_cfc, vertices, arestas = calcular_n_cfc(
               "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
               "Output/Parte1/maior_cfc_arestas.csv")

            print(
               f"Número de CFC {num_cfc}\n"+
               f"Qtd de vértices do maior CFC {vertices}\n"+
               f"Qtd de arestas do maior CFC {arestas}"
            )

            visualizar_grafo_completo_de_csv(
               "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
               3000,
               "Output/Parte1/Graficos/grafo_completo.png")

            diametro, raio, caminho_medio =calcular_diametro_raio_caminho_medio()

            print(f"Diametro {diametro}\nRaio {raio}\nCaminho médio {caminho_medio}")
            print(f"Clusterização média {calcular_clusterizacao_media()}")
        case "2":
            caminho = "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv"
            
            mst_prim, custo_prim = prim_mst(caminho, None, no_raiz="2")
            
            print()
            print("================================================")
            print(f"Prim -> arestas na MST: {len(mst_prim)} | custo total: {custo_prim}")
        
            mst_kruskal, custo_kruskal = kruskal_mst(caminho, None)
            print()
            print(f"Kruskal -> arestas na MST: {len(mst_kruskal)} | custo total: {custo_kruskal}")
            print("================================================")
            print()
        case "3":
            print(
                "A raíz e o vértice alvo devem pertencer ao grafo, consulte antes o arquivo"+
                " Output/Parte_1/maior_cfc_arestas.csv"
                )

            raiz = input("Insira o id do vértice raíz: ")
            

            ctrl, grafo =(bellman_ford_forcado("Output/Parte1/maior_cfc_arestas.csv", 10000, raiz))
            if ctrl:
                print("Grafo sem ciclos negativos")
            else:
                print("Grafo com ciclos negativos")
        case "4":
            print(
                "A raíz e o vértice alvo devem pertencer ao grafo, consulte antes o arquivo"+
                "Output/Parte_1/arestas_ordenadas_estaticas.csv"
                )
            
            raiz = input("Insira o id do vértice raíz: ")

            arvore = busca_em_largura(
                "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
                None,
                raiz,
                None)
        case "5":
            print(
                "A raíz e o vértice alvo devem pertencer ao grafo, consulte antes o arquivo"+
                "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv"
                )

            raiz = input("Insira o id do vértice raíz: ")
            
            grafo = busca_em_profundidade_iterativa(
                "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
                None)
            
        case "6":
            raiz = input("Insira o ID do vértice raíz: ")
            grafo = dijkstra_forcado(
                "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
                None,
                raiz)
        case "7":
            qtd_arestas = int(input("Insira a quantidade de arestas (para usar todas, insira -1): "))
            if qtd_arestas == -1:
                qtd_arestas = None
            ids, matriz = floyd_warshall_forcado(
                "Output/Parte1/maior_cfc_arestas.csv",
                qtd_arestas)
        case "8":
            cfcs, grafo = tarjan_com_dfs(
                    "Output/Tratamento_de_entrada/arestas_ordenadas_estaticas.csv",
                    None
                )
            print(f"Total de CFCs: {len(cfcs)}")
    


    print("Para reexibir o menu, insira h")