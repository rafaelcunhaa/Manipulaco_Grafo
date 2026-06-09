def Algoritmo_A(valores, tipo_grafo, inicio, fim):
    """
    Função para implementar o Algoritmo A* para encontrar o caminho mais curto entre dois vértices em um grafo.
    Utiliza uma fila de prioridade para explorar os vértices com base na soma do custo acumulado e da heurística.
    O resultado é o caminho mais curto do vértice de início ao vértice de destino, ou uma mensagem indicando que não há caminho.
    """
    # Implementação do Algoritmo A* aqui
    with open("distancias.json", "r", encoding="utf-8") as f:
        grafo = json.load(f)
    with open("ibge.json", "r", encoding="utf-8") as f:
        heuristicas = json.load(f)
    with open("capitais.json", "r", encoding="utf-8") as f:
        capitais = json.load(f)
    
    abertos = []
    heapq.heappush(abertos, (0 + heuristicas[inicio], 0, inicio, [inicio]))  # (f(n), g(n), vértice atual, caminho)

    fechados = set()

    custos_g = {}
    custos_g[inicio] = 0
    pais = {}

    while abertos:
        _, atual = heapq.heappop(abertos)

        fechados.append(atual)

        print("Visitando:", atual)
        print("Abertos:", [cidade for _, cidade in abertos])
        print("Fechados:", fechados)

        if atual == fim:
            caminho = []

            while atual in pais:
                caminho.append(atual)
                atual = pais[atual]
            caminho.append(inicio)
            caminho.reverse()

            return caminho, custos_g[fim]
        
        for vizinho, distancia in grafo[atual].items():
            novo_custo = custos_g[atual] + distancia

            if vizinho not in custos_g or novo_custo < custos_g[vizinho]:
                custos_g[vizinho] = novo_custo
                f_n = novo_custo + heuristicas[vizinho]
                heapq.heappush(abertos, (f_n, vizinho))
                pais[vizinho] = atual

    return None