import heapq
import json
from visualizacao_rota import visualizar_rota_horizontal

# ===========================================================================
#  UTILITÁRIOS DE CARREGAMENTO
# ===========================================================================

def carregar_grafo_vizinhos():
    with open("distancias.json", "r", encoding="utf-8") as f:
        distancias = json.load(f)

    with open("capitais_vizinhas.json", "r", encoding="utf-8") as f:
        vizinhos = json.load(f)

    grafo = {}

    for cidade in vizinhos:
        grafo[cidade] = {}

        for vizinho in vizinhos[cidade]:

            chave1 = f"{cidade}:{vizinho}"
            chave2 = f"{vizinho}:{cidade}"

            if chave1 in distancias:
                grafo[cidade][vizinho] = distancias[chave1]

            elif chave2 in distancias:
                grafo[cidade][vizinho] = distancias[chave2]

    return grafo

def _carregar_arquivos():
    """
    Carrega e retorna (grafo_nested, heuristicas) a partir dos JSONs.

    distancias.json  → chaves no formato "CidadeA:CidadeB": km_por_estrada
    ibge.json        → dict aninhado  {cidade: {destino: km_linha_reta}}

    Retorna grafo como dict aninhado {origem: {destino: custo}}.
    Distâncias são espelhadas (não-dirigido) para garantir conectividade total.
    """
    
    with open("ibge.json", "r", encoding="utf-8") as f:
        heuristicas = json.load(f)

    grafo = carregar_grafo_vizinhos()

    return grafo, heuristicas


def _aplicar_congestionamento(grafo: dict, congestionamentos: dict) -> dict:
    """
    Retorna uma CÓPIA do grafo com os pesos dos trechos multiplicados
    pelos fatores de congestionamento informados.

    congestionamentos: dict  {(cidade_a, cidade_b): fator_float}
    O espelhamento (b→a) é feito automaticamente.
    """
    import copy
    grafo_c = copy.deepcopy(grafo) # para não alterar o grafo original

    for (a, b), fator in congestionamentos.items():
        if a in grafo_c and b in grafo_c[a]:
            grafo_c[a][b] = round(grafo_c[a][b] * fator)
        if b in grafo_c and a in grafo_c[b]:
            grafo_c[b][a] = round(grafo_c[b][a] * fator)

    return grafo_c


# ===========================================================================
#  NÚCLEO DO ALGORITMO A*
# ===========================================================================

def _astar_core(grafo: dict, heuristicas: dict, inicio: str, fim: str):
    """
    Executa o A* e retorna (caminho, custo_total, log_passos).

    log_passos: lista de dicts com snapshot de cada iteração para exibição.

    A heurística h(n) = ibge[n][fim]  (distância em linha reta até o destino).
    É admissível pois linha reta ≤ distância real por estrada.
    """
    if inicio not in grafo:
        return None, 0, []
    if fim not in grafo:
        return None, 0, []
    if inicio == fim:
        return [inicio], 0, []

    # heap: (f_n, g_n, vertice_atual, caminho_acumulado)
    abertos_heap = []
    h_inicio = heuristicas.get(inicio, {}).get(fim, 0)
    heapq.heappush(abertos_heap, (h_inicio, 0, inicio, [inicio]))

    # Dicionário para rastrear os nós ainda na fila (para impressão limpa)
    abertos_set = {inicio}

    fechados = []          # lista ordenada de visita (para o relatório)
    fechados_set = set()   # para checagem O(1)

    custos_g = {inicio: 0}
    pais = {}

    log_passos = []        # histórico para exibição posterior
    passo = 0

    while abertos_heap:
        f_atual, g_atual, atual, caminho = heapq.heappop(abertos_heap)
        abertos_set.discard(atual) # remove do set de abertos

        # Nó já processado com custo melhor → ignorar
        if atual in fechados_set:
            continue

        fechados.append(atual)
        fechados_set.add(atual)

        # ---- Snapshot para relatório ----
        passo += 1
        log_passos.append({
            "passo":    passo,
            "visitado": atual,
            "g":        g_atual,
            "h":        round(heuristicas.get(atual, {}).get(fim, 0), 1),
            "f":        round(f_atual, 1),
            "abertos":  sorted(abertos_set),
            "fechados": list(fechados),
        })

        # ---- Chegamos ao destino ----
        if atual == fim:
            return caminho, g_atual, log_passos

        # ---- Expandir vizinhos ----
        for vizinho, distancia in grafo.get(atual, {}).items():
            if vizinho in fechados_set:
                continue

            novo_g = custos_g[atual] + distancia

            if vizinho not in custos_g or novo_g < custos_g[vizinho]:
                custos_g[vizinho] = novo_g
                h_viz = heuristicas.get(vizinho, {}).get(fim, 0)
                f_viz = novo_g + h_viz
                pais[vizinho] = atual
                heapq.heappush(abertos_heap, (f_viz, novo_g, vizinho, caminho + [vizinho]))
                abertos_set.add(vizinho)

    print("\nPais:")
    for filho, pai in pais.items():
        print(f"{filho} <- {pai}")
    return None, 0, log_passos   # sem caminho possível


# ===========================================================================
#  EXIBIÇÃO DOS RESULTADOS
# ===========================================================================

def _exibir_resultado(cenario: str, caminho, custo: int, log_passos: list,
                      inicio: str, fim: str):
    """Imprime de forma estruturada o resultado de um cenário."""
    largura = 70
    print("\n" + "=" * largura)
    print(f"  CENÁRIO: {cenario}".center(largura))
    print(f"  Rota: {inicio}  →  {fim}".center(largura))
    print("=" * largura)

    if not caminho:
        print(f"\n  ✗ Não foi encontrado caminho de {inicio} até {fim}.")
        return

    # ---- Listas de Abertos / Fechados por passo ----
    print("\n  HISTÓRICO DE ITERAÇÕES:")
    print(f"  {'Passo':<6} {'Visitado':<22} {'g(n)':>7} {'h(n)':>7} {'f(n)':>7}")
    print("  " + "-" * 53)
    for p in log_passos:
        print(f"  {p['passo']:<6} {p['visitado']:<22} "
              f"{p['g']:>7}  {p['h']:>7}  {p['f']:>7}")
        print(f"         Abertos  : {p['abertos']}")
        print(f"         Fechados : {p['fechados']}")
        print()

    # ---- Caminho e custo final ----
    print("  CAMINHO ENCONTRADO:")
    print("  " + "  →  ".join(caminho))
    print(f"\n  Custo total : {custo} km")
    print(f"  Nº de paradas: {len(caminho) - 1} trecho(s)")
    print("=" * largura + "\n")


def _comparar_cenarios(caminho_normal, custo_normal,
                       caminho_cong,   custo_cong,
                       inicio: str,    fim: str,
                       congestionamentos: dict):
    """Exibe comparação lado a lado dos dois cenários."""
    largura = 70
    print("\n" + "=" * largura)
    print("  COMPARAÇÃO ENTRE CENÁRIOS".center(largura))
    print("=" * largura)

    print(f"\n  Rota buscada: {inicio}  →  {fim}\n")

    # Trechos congestionados nesta rota
    trechos_afetados = []
    if caminho_cong:
        for i in range(len(caminho_cong) - 1):
            a, b = caminho_cong[i], caminho_cong[i + 1]
            if (a, b) in congestionamentos or (b, a) in congestionamentos:
                fator = congestionamentos.get((a, b), congestionamentos.get((b, a)))
                trechos_afetados.append((a, b, fator))

    # Diferença de percurso
    print(f"  {'NORMAL':^33} | {'CONGESTIONAMENTO':^33}")
    print("  " + "-" * 69)

    rota_n = "  →  ".join(caminho_normal) if caminho_normal else "Sem rota"
    rota_c = "  →  ".join(caminho_cong)   if caminho_cong   else "Sem rota"
    print(f"  {rota_n}")
    print(f"  Custo: {custo_normal} km")
    print()
    print(f"  {rota_c}")
    print(f"  Custo (congestionado): {custo_cong} km")

    if caminho_normal and caminho_cong:
        rotas_iguais = (caminho_normal == caminho_cong)
        print()
        if rotas_iguais:
            print("O congestionamento NÃO alterou o caminho escolhido.")
            print(f"    Porém o custo percebido aumentou de {custo_normal} "
                  f"→ {custo_cong} km (+{custo_cong - custo_normal} km)")
        else:
            print("  O congestionamento ALTEROU o caminho:")
            nos_s = set(caminho_normal)
            nos_c = set(caminho_cong)
            evitados  = nos_s - nos_c
            adicionados = nos_c - nos_s
            if evitados:
                print(f"    Nós EVITADOS no congestionamento : {sorted(evitados)}")
            if adicionados:
                print(f"    Nós ADICIONADOS pelo desvio      : {sorted(adicionados)}")

    if trechos_afetados:
        print("\n  Trechos com trânsito pesado nesta rota:")
        for a, b, fator in trechos_afetados:
            print(f"    {a} → {b}  (fator {fator}x)")
    else:
        print("\n  Nenhum trecho congestionado faz parte desta rota.")

    print("=" * largura + "\n")


# ===========================================================================
#  INTERFACE COM O USUÁRIO
# ===========================================================================

def _listar_capitais(grafo: dict):
    """Lista as capitais na ordem definida em capitais.json."""
    try:
        with open("capitais.json", "r", encoding="utf-8") as f:
            capitais = json.load(f)
        # Garante que só lista cidades que existem no grafo carregado
        capitais = [c for c in capitais if c in grafo]
    except FileNotFoundError:
        # Fallback: ordem alfabética caso o arquivo não esteja presente
        capitais = sorted(grafo.keys())
    print("\n  Capitais disponíveis:")
    for i, c in enumerate(capitais, 1):
        print(f"    {i:>2}. {c}")
    return capitais


def _escolher_capital(grafo: dict, rotulo: str) -> str:
    """Pede ao usuário que escolha uma capital, por número ou nome."""
    capitais = _listar_capitais(grafo)
    while True:
        entrada = input(f"\n  Digite o número ou nome da capital de {rotulo}: ").strip()
        # Por número
        if entrada.isdigit():
            idx = int(entrada) - 1
            if 0 <= idx < len(capitais):
                return capitais[idx]
            print("Número inválido.")
            continue
        # Por nome (case-insensitive)
        entrada_norm = entrada.lower()
        matches = [c for c in capitais if c.lower() == entrada_norm]
        if matches:
            return matches[0]
        # Busca parcial amigável
        parciais = [c for c in capitais if entrada_norm in c.lower()]
        if len(parciais) == 1:
            confirmacao = input(f"  Você quis dizer '{parciais[0]}'? (s/n): ").strip().lower()
            if confirmacao == "s":
                return parciais[0]
        elif len(parciais) > 1:
            print(f"  Encontrei várias: {parciais}. Seja mais específico.")
        else:
            print("  Capital não encontrada. Tente novamente.")


def _menu_congestionamento(grafo: dict) -> dict:
    """
    Permite ao usuário personalizar os trechos de congestionamento
    ou usar o conjunto padrão (baseado nas rodovias mais movimentadas do Brasil).
    """
    # Trechos padrão — rodovias BR-116, BR-040, BR-060 (sul/sudeste)
    PADROES = {
        ("São Paulo",      "Rio de Janeiro"):   3.0,
        ("Rio de Janeiro", "São Paulo"):        3.0,
        ("São Paulo",      "Curitiba"):         2.5,
        ("Curitiba",       "São Paulo"):        2.5,
        ("Rio de Janeiro", "Belo Horizonte"):   2.0,
        ("Belo Horizonte", "Rio de Janeiro"):   2.0,
        ("Brasília",       "Goiânia"):          2.0,
        ("Goiânia",        "Brasília"):         2.0,
    }

    print("\n  ┌─────────────────────────────────────────┐")
    print("  │     CONFIGURAÇÃO DE CONGESTIONAMENTO    │")
    print("  └─────────────────────────────────────────┘")
    print("\n  Trechos padrão de congestionamento:")
    for i, ((a, b), f) in enumerate(PADROES.items(), 1):
        print(f"    {i}. {a} → {b}  ({f}x mais lento)")
    print()
    opcao = input("  Usar trechos padrão? (s = sim / n = personalizar): ").strip().lower()
    if opcao != "n":
        return PADROES

    # Personalização
    congestionamentos = {}
    print("\n  Digite os trechos (ENTER em branco para encerrar):")
    while True:
        a = input("  Cidade de origem do trecho (ENTER para finalizar): ").strip()
        if not a:
            break
        if a not in grafo:
            print(f" '{a}' não encontrado no grafo.")
            continue
        b = input("  Cidade de destino do trecho: ").strip()
        if b not in grafo:
            print(f" '{b}' não encontrado no grafo.")
            continue
        try:
            fator = float(input(f"  Fator de congestionamento (ex: 2.5): "))
            if fator < 1:
                print("  Fator deve ser ≥ 1.")
                continue
        except ValueError:
            print("  Fator inválido.")
            continue
        congestionamentos[(a, b)] = fator
        congestionamentos[(b, a)] = fator
        print(f"  Trecho {a} ↔ {b} adicionado (fator {fator}x)")

    return congestionamentos if congestionamentos else PADROES


# ===========================================================================
#  PONTO DE ENTRADA PRINCIPAL
# ===========================================================================

def Algoritmo_A():
    """
    Ponto de entrada chamado pelo menu principal (main.py).
    Os parâmetros `valores` e `tipo_grafo` são recebidos do menu mas não
    são usados pelo A* — ele usa seus próprios arquivos JSON com distâncias
    reais entre capitais brasileiras.

    Se `inicio` e `fim` já foram informados pelo menu, usa-os diretamente.
    Caso contrário, pede interativamente ao usuário.
    """
    print("\n" + "█" * 70)
    print("  ALGORITMO A* — OTIMIZAÇÃO DE ROTAS ENTRE CAPITAIS BRASILEIRAS")
    print("█" * 70)

    # ---- Carregar dados ----
    try:
        grafo, heuristicas = _carregar_arquivos()

        print(len(grafo["Aracajú"]))
        print(grafo["Aracajú"].keys())
    except FileNotFoundError as e:
        print(f"\n  ERRO: Arquivo não encontrado → {e}")
        print("  Certifique-se de que distancias.json e ibge.json estão na mesma pasta.")
        return None

    # ---- Escolher origem e destino ----
    cidade_inicio = _escolher_capital(grafo, "ORIGEM")

    cidade_fim = _escolher_capital(grafo, "DESTINO")

    if cidade_inicio == cidade_fim:
        print("\n  Origem e destino são iguais — sem necessidade de rota.")
        return [cidade_inicio], 0

    # ---- Cenário 1: Normal ----
    print(f"\n  Calculando rota normal: {cidade_inicio} → {cidade_fim} ...")
    caminho_n, custo_n, log_n = _astar_core(grafo, heuristicas, cidade_inicio, cidade_fim)
    _exibir_resultado("NORMAL", caminho_n, custo_n, log_n, cidade_inicio, cidade_fim)
    print("\nDEBUG CAMINHO:")
    print(caminho_n)
    print("Quantidade de cidades:", len(caminho_n))

    visualizar_rota_horizontal(
    caminho_n,
    custo_n,
    titulo="Cenário Normal"
    )

    # ---- Configurar congestionamentos ----
    congestionamentos = _menu_congestionamento(grafo)

    # ---- Cenário 2: Congestionamento ----
    grafo_c = _aplicar_congestionamento(grafo, congestionamentos)
    print(f"\n  Calculando rota com congestionamento: {cidade_inicio} → {cidade_fim} ...")
    caminho_c, custo_c, log_c = _astar_core(grafo_c, heuristicas, cidade_inicio, cidade_fim)
    _exibir_resultado("CONGESTIONAMENTO", caminho_c, custo_c, log_c, cidade_inicio, cidade_fim)

    visualizar_rota_horizontal(
    caminho_c,
    custo_c,
    titulo="Cenário com Congestionamento"
)

    # ---- Comparação ----
    _comparar_cenarios(caminho_n, custo_n, caminho_c, custo_c,
                       cidade_inicio, cidade_fim, congestionamentos)

    # Retornar no formato esperado pelo menu principal
    if caminho_n:
        return caminho_n, custo_n
    return None
