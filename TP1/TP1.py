from collections import deque
import sys
import heapq
import time


PUZZLE_SIZE = 3
OBJETIVO = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]


def encontrar_vazio(estado):
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                return i, j


def gerar_filhos(estado):
    filhos = []
    i, j = encontrar_vazio(estado)

    movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # possíveis movimentos

    for di, dj in movimentos:
        ni, nj = i + di, j + dj

        if 0 <= ni < 3 and 0 <= nj < 3:
            # cópia do estado atual para não modificar o original
            filho = [list(row) for row in estado]
            # 0 vai para ua nova posição
            filho[i][j], filho[ni][nj] = filho[ni][nj], filho[i][j]
            filhos.append(filho)

    return filhos


def criar_matriz(valores):
    matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    contador = 0

    for i in range(PUZZLE_SIZE):
        for j in range(PUZZLE_SIZE):
            try:
                matriz[i][j] = int(valores[contador])
                contador += 1
            except ValueError:
                print("Por favor, forneça apenas números válidos.")
                return None

    matriz_tupla = tuple(map(tuple, matriz))
    return matriz_tupla


def bfs(estado_inicial):
    visitados = set()
    # Fila para a busca, iniciada com o estado inicial e um caminho vazio
    fila = deque([(estado_inicial, [])])

    while fila:
        estado, caminho = fila.popleft()

        if estado == OBJETIVO:
            return caminho

        # Conversão da lista de listas em uma tupla de tuplas para torná-la hashable
        visitados.add(tuple(map(tuple, estado)))

        for filho in gerar_filhos(estado):
            if tuple(map(tuple, filho)) not in visitados:
                fila.append((filho, caminho + [filho]))


class dfs_visitados:
    def __init__(self):
        self.prof_set = [set()]

    def add(self, elem, prof):
        if len(self.prof_set) >= prof + 1:
            self.prof_set[prof].add(elem)
        else:
            self.prof_set.append(set())
            self.prof_set[prof].add(elem)

    def tem_elemento(self, elem, prof):
        for i in range(prof):
            if elem in self.prof_set[i]:
                return True
        return False


def dfs_limitado(estado, caminho, limite, visitados):
    # Converte a lista de listas em uma tupla de tuplas
    estado_tupla = tuple(map(tuple, estado))

    if estado_tupla == tuple(map(tuple, OBJETIVO)):
        return caminho

    if limite == 0:
        return None

    for filho in gerar_filhos(estado):
        # Converte o filho em uma tupla de tuplas
        filho_tupla = tuple(map(tuple, filho))
        if not visitados.tem_elemento(filho_tupla, len(caminho)):
            novo_caminho = caminho + [filho]
            visitados.add(filho_tupla, len(novo_caminho))
            resultado = dfs_limitado(
                filho, novo_caminho, limite - 1, visitados)
            if resultado is not None:
                return resultado


def ids(estado_inicial):
    limite = 0

    while True:
        resultado = dfs_limitado(
            estado_inicial, [], limite, dfs_visitados())

        if resultado is not None:
            return resultado

        limite += 1


def ucs(estado_inicial):
    visitados = set()
    fila = [(0, estado_inicial, [])]

    while fila:
        custo, estado, caminho = heapq.heappop(fila)

        if estado == OBJETIVO:
            return caminho

        visitados.add(tuple(map(tuple, estado)))

        for filho in gerar_filhos(estado):
            if tuple(map(tuple, filho)) not in visitados:
                novo_custo = custo + 1  # Aumento consecutivo no custo
                heapq.heappush(fila, (novo_custo, filho, caminho + [filho]))


def manhattan(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a, b))


def heuristica1(estado):
    lista = []
    for x in range(3):
        for y in range(3):
            elemento = estado[x][y]
            if elemento == 0:
                xCorr = 2
                yCorr = 2
            else:
                xCorr = (elemento-1) // 3
                yCorr = (elemento-1) % 3

            if (xCorr == x and yCorr == y):
                lista.append(0)
            else:
                lista.append(manhattan([x, y], [xCorr, yCorr]))
    return lista


def a_star(estado_inicial):
    g = 0
    h = heuristica1(estado_inicial)
    visitados = set()

    f = g + sum(h)

    fila = [(f, g, estado_inicial, [])]
    while fila:
        f, g, estado, caminho = heapq.heappop(fila)

        if estado == OBJETIVO:
            return caminho

        visitados.add(tuple(map(tuple, estado)))

        i = 0
        for filho in gerar_filhos(estado):
            if tuple(map(tuple, filho)) not in visitados:
                h = heuristica1(estado)
                # Aumento consecutivo no custo, usando a heuristica
                f = g + 1 + sum(h)
                heapq.heappush(fila, (f, g+1, filho, caminho + [filho]))
                i = i + 1


def heuristica2(estado):
    cont = 0
    for x in range(3):
        for y in range(3):
            elemento = estado[x][y]
            if elemento == 0:
                xCorr = 2
                yCorr = 2
            else:
                xCorr = (elemento-1) // 3
                yCorr = (elemento-1) % 3

            if (xCorr != x or yCorr != y):
                cont = cont + 1
    return cont


def greedy_best_first_search(estado_inicial):
    h = heuristica2(estado_inicial)
    visitados = set()
    f = h
    fila = [(f, estado_inicial, [])]
    while fila:
        f, estado, caminho = heapq.heappop(fila)

        if estado == OBJETIVO:
            return caminho

        visitados.add(tuple(map(tuple, estado)))

        i = 0
        for filho in gerar_filhos(estado):
            if tuple(map(tuple, filho)) not in visitados:
                h = heuristica2(estado)
                # Aumento consecutivo no custo, usando a heuristica
                f = h
                heapq.heappush(fila, (f, filho, caminho + [filho]))
                i = i + 1


def hill_climbing(estado_inicial):
    caminho = []
    estado = estado_inicial
    while True:
        vizinhos = gerar_filhos(estado)
        melhor_vizinho = min(
            vizinhos, key=lambda estado: sum(heuristica1(estado)))
        if sum(heuristica1(melhor_vizinho)) >= sum(heuristica1(estado)):
            caminho.append(estado)
            return caminho

        estado = melhor_vizinho
        caminho.append(estado)


# MAIN

inicio = time.time()

if len(sys.argv) < 11 or len(sys.argv) > 12:
    sys.exit("Quantidade inválida de parâmetros, siga o formato:\n<algoritmo> ex: B, I, U, A, G, H\n<entrada> ex: 1 2 3 4 0 5 6 7 8\n<PRINT> (Parâmetro opicional)\n")

algoritmo = sys.argv[1]
if algoritmo not in ["B", "I", "U", "A", "G", "H"]:
    sys.exit(
        "O parâmetro <algoritmo> não é válido, tente usar um desses: B, I, U, A, G, H\n")

valores = sys.argv[2:11]

mostrar = False
if len(sys.argv) > 11:
    assert (sys.argv[-1] == "PRINT")
    mostrar = True

matriz = criar_matriz(valores)

if matriz == tuple(map(tuple, OBJETIVO)):
    print("0")
elif matriz:
    if algoritmo == "B":
        caminho_solucao = bfs(matriz)
    elif algoritmo == "I":
        caminho_solucao = ids(matriz)
    elif algoritmo == "U":
        caminho_solucao = ucs(matriz)
    elif algoritmo == "A":
        caminho_solucao = a_star(matriz)
    elif algoritmo == "G":
        caminho_solucao = greedy_best_first_search(matriz)
    elif algoritmo == "H":
        caminho_solucao = hill_climbing(matriz)
    else:
        print("Erro: verificar input")

    if caminho_solucao:
        print(len(caminho_solucao))
        if mostrar:
            for passo in caminho_solucao:
                print("\n".join([" ".join(map(str, linha))
                      for linha in passo]))
                print(" ")
    else:
        print("Não foi possível encontrar uma solução.")
else:
    print("Erro desconhecido")

fim = time.time()
tempo_decorrido = fim - inicio
#print(f'O programa {algoritmo} levou {tempo_decorrido:.5f} segundos para ser executado. {len(caminho_solucao)}')