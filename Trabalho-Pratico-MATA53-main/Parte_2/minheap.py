class MinHeapVertices:
    """Min-heap de pares [distancia, id_vertice] com rastreamento de índice
    para atualizar a distância de um vértice diretamente no heap.
    Interpreta `None` como distância infinita (+inf) nas comparações.
    """

    def __init__(self) -> None:
        self.heap: list[list[int | float | str | None]] = []
        self.posicoes: dict[str, int] = {}

    @staticmethod
    def _chave_distancia(distancia: int | float | None) -> float:
        return float("inf") if distancia is None else float(distancia)

    def esta_vazio(self) -> bool:
        return len(self.heap) == 0

    def contem(self, id_vertice: str) -> bool:
        return id_vertice in self.posicoes

    def _trocar(self, i: int, j: int) -> None:
        id_i = str(self.heap[i][1])
        id_j = str(self.heap[j][1])
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.posicoes[id_i] = j
        self.posicoes[id_j] = i

    def _subir(self, idx: int) -> None:
        while idx > 0:
            pai = (idx - 1) // 2
            dist_atual = self._chave_distancia(self.heap[idx][0])  # type: ignore[arg-type]
            dist_pai = self._chave_distancia(self.heap[pai][0])   # type: ignore[arg-type]
            if dist_atual < dist_pai:
                self._trocar(idx, pai)
                idx = pai
            else:
                break

    def _descer(self, idx: int) -> None:
        tamanho = len(self.heap)
        while True:
            menor = idx
            esq = 2 * idx + 1
            dir = 2 * idx + 2

            dist_menor = self._chave_distancia(self.heap[menor][0])  # type: ignore[arg-type]
            if esq < tamanho:
                dist_esq = self._chave_distancia(self.heap[esq][0])  # type: ignore[arg-type]
                if dist_esq < dist_menor:
                    menor = esq
                    dist_menor = dist_esq

            if dir < tamanho:
                dist_dir = self._chave_distancia(self.heap[dir][0])  # type: ignore[arg-type]
                if dist_dir < dist_menor:
                    menor = dir

            if menor != idx:
                self._trocar(idx, menor)
                idx = menor
            else:
                break

    def atualizar_distancia(self, id_vertice: str, nova_distancia: int | float | None) -> None:
        if id_vertice not in self.posicoes:
            return
        idx = self.posicoes[id_vertice]
        dist_antiga = self._chave_distancia(self.heap[idx][0])  # type: ignore[arg-type]
        dist_nova = self._chave_distancia(nova_distancia)
        self.heap[idx][0] = nova_distancia

        if dist_nova < dist_antiga:
            self._subir(idx)
        elif dist_nova > dist_antiga:
            self._descer(idx)

    def inserir(self, id_vertice: str, distancia: int | float | None) -> None:
        if id_vertice in self.posicoes:
            self.atualizar_distancia(id_vertice, distancia)
            return
        idx = len(self.heap)
        self.heap.append([distancia, id_vertice])
        self.posicoes[id_vertice] = idx
        self._subir(idx)

    def extrair_minimo(self) -> tuple[int | float | None, str] | None:
        if not self.heap:
            return None

        min_dist, min_id = self.heap[0][0], str(self.heap[0][1])
        ultimo_idx = len(self.heap) - 1

        if ultimo_idx == 0:
            self.heap.pop()
            del self.posicoes[min_id]
        else:
            ultimo_item = self.heap.pop()
            self.heap[0] = ultimo_item
            self.posicoes[str(ultimo_item[1])] = 0
            del self.posicoes[min_id]
            self._descer(0)

        return min_dist, min_id