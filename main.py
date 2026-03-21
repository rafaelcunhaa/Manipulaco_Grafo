import collections
import shutil

#SITUAÇÃO: FUNCIONANDO
def pedir_valores():
    """
    Função para pedir para o usuario valores para a criação do grafo
    enquanto ele indica os valores e suas ligações o codigo faz a separação
    a partir de cada "," digitada pelo usuario e guardada em uma lista
    e para as ligações é feito a separação igual as vertices mas quando 
    as ligações são inseridas é feito um dicionario para cada vertice.
    
    """      
    mapa = {}
    total_numeros = input("Qual numeros terá no grafo? (Ex:0,1):").strip() #strip() remove os espaços em branco no inicio e no final da string, garantindo que a entrada do usuário seja processada corretamente mesmo que haja espaços acidentais.
    total_numeros_separados = total_numeros.split(",")
    for i in range(len(total_numeros_separados)):
        valor_agora = total_numeros_separados[i]
        valor = input(f"Informe qual numero faz ligação com o {valor_agora} (Ex:0,1):").strip()
        if valor == "":
            mapa[valor_agora] = []
        else:    
            valor_separado = valor.split(",")
            mapa[valor_agora] = valor_separado
        
    
    return mapa


#SITUAÇÃO: FUNCIONANDO
def criar_Matriz(valores):
    """
    Cria uma matriz dirigida a partir dos valores indicados pelo usuario na função pedir_valores().
    
    """    
    vertices = list(valores.keys())
    n = len(vertices)
    
    matriz = [[0 for _ in range(n)] for _ in range(n)]# cria uma matriz de adjacência inicializada com zeros, onde n é o número de vértices no grafo. 
    
    
    for v in valores:
        for proximo in valores[v]:
            if proximo not in vertices:
                print(f"Erro: {proximo} não existe no grafo")
                continue
            i = vertices.index(v)
            j = vertices.index(proximo)

            matriz[i][j] = 1
            



    return matriz

    

#SITUAÇÃO: FUNCIONANDO
def varredura_Grafo_DFS(valores,valor_inicial):
    """
    Percorre o grafo usando DFS (Depth First Search — busca em profundidade).
    Utiliza uma pilha (LIFO): a cada iteração remove o último elemento, e se
    ainda não foi visitado, marca-o e adiciona seus adjacentes no topo da pilha.

    """  
    visitados = set()
    vertices = list(valores.keys()) # retornar uma visualização de todas as chaves
    pilha = [vertices[valor_inicial]]
        
    while pilha or len(visitados) < len(vertices):
        
        if not pilha:#
            for j in vertices:
                if j not in visitados:
                    pilha.append(j)
                    break
                
        
        vertice = pilha.pop()
       
        if vertice not in visitados:
           print("Visitando:", vertice)
           visitados.add(vertice)
           yield vertice # o yield é utilizado para criar um gerador, permitindo que a função retorne um valor e pause sua execução, retomando de onde parou na próxima chamada. Isso é útil para iterar sobre os vértices visitados durante a varredura do grafo, permitindo que o código que chama a função processe cada vértice à medida que é visitado, em vez de esperar que a função retorne uma lista completa de vértices visitados no final da execução.
           
           for i in valores[vertice]:
               if i not in visitados:
                   pilha.append(i)
                   

#SITUAÇÃO: FUNCIONANDO
def varredura_Grafo_BFS(valores,valor_inicial):
    """
    Percorre o grafo usando BFS (Breadth First Search — busca em largura).
    Utiliza uma fila (FIFO): a cada iteração remove o primeiro elemento, e se
    ainda não foi visitado, marca-o e adiciona seus adjacentes no final da fila.

    """
    visitados = set()
    vertices = list(valores.keys())
    fila = collections.deque([vertices[valor_inicial]]) # deque é uma fila de duas pontas 
    nao_conexo = False
        
    while fila or len(visitados) < len(vertices):
        
        if not fila:
            for j in vertices:
                if j not in visitados:
                    fila.append(j)
                    nao_conexo = True
                    break
        vertice = fila.popleft()
       
        if vertice not in visitados:
           print("Visitando:", vertice)
           visitados.add(vertice)
           yield vertice
           
           for i in valores[vertice]:
               if i not in visitados:
                   fila.append(i)
    return nao_conexo               

           

#SITUAÇÃO: FUNCIONANDO
def adicionar_vertice(valores,tipo_grafo):
    """
    Função para adicionar um valor ao grafo dirigido, solicitando o valor e suas ligações.
    O valor é adicionado ao dicionário do grafo, e as ligações são atualizadas
    apenas na direção especificada pelo usuário.
    """
    nova_vertice = input("Digite o valor da vertice: ").strip()
    if nova_vertice not in valores:
        ligacoes = input(f"Digite as ligações para a vertice {nova_vertice} (Ex:0,1): ").strip()

        if ligacoes == "":
            valores[nova_vertice] = []
        ligacoes_separadas = ligacoes.split(",")    

        if tipo_grafo == 1:
            valores[nova_vertice] = ligacoes_separadas

        elif tipo_grafo == 2:  

            valores[nova_vertice] = ligacoes_separadas
            for v in ligacoes_separadas:
                if v in valores:
                    if nova_vertice not in valores[v]:
                        valores[v].append(nova_vertice)    
    else:
        print("Valor digitado já existe no grafo")
        return       
    return "Vertice adicionada com sucesso" 


#SITUAÇÃO: FUNCIONANDO
def adicionar_ligacao(valores,tipo_grafo):
    """
    Função para adicionar uma ligação entre dois vértices em um grafo.
    Solicita os vértices de origem e destino, e atualiza o dicionário do grafo,
    caso o grafo for direcionado só adiciona a vertice para a ligação nova, caso
    seja não dircecional adiciona para os dois a ligação.

    """
    vertice_alterar = input("Digite a vertice que deseja alterar: ").strip()
    if vertice_alterar not in valores:
        print(f"{vertice_alterar} não existe no grafo")
        return
    
    ligacao_nova = input(f"Digite a ligacao nova da vertice {vertice_alterar}: ").strip()

    if ligacao_nova not in valores:
        print(f"{ligacao_nova} não existe no grafo")
        return
    
    if ligacao_nova in valores[vertice_alterar]:
        print("Valor digitado já existe na vertice")
        return
    
    if tipo_grafo == 1:
        valores[vertice_alterar].append(ligacao_nova)
        print("Ligação adicionada com sucesso")
    elif tipo_grafo == 2:
        valores[vertice_alterar].append(ligacao_nova)
        valores[ligacao_nova].append(vertice_alterar)
        print("Ligação adicionada com sucesso")




    return "Ligação adicionada com sucesso"    


#SITUAÇÃO: FUNCIONANDO
def remove_vertice(valores):
    """
    Função para remover um vértice de um grafo, solicitando o vértice a ser removido.
    O vértice é removido do dicionário do grafo, e todas as ligações associadas a ele
    são atualizadas, removendo o vértice de quaisquer listas de adjacência onde ele apareça.
    """
    vertice = input("Digite a vertice que quer remover: ").strip()
    if vertice not in valores:
        print("A vertice informada não foi encontrada")
        return
    del valores[vertice]
    print(f"Vertice removida \n \
           █████████\n \
           █▄█████▄█\n \
           █▼▼▼▼▼\n \
           █\n \
            {vertice}\n \
           █▲▲▲▲▲\n \
           █████████\n \
           ██ ██")

    for i in valores:
        if vertice in valores[i]:
            valores[i].remove(vertice)


#SITUAÇÃO: FUNCIONANDO
def remove_ligacao(valores,tipo_grafo):
    """
    Função para remover uma ligação entre dois vértices em um grafo.
    Solicita os vértices de origem e destino, e atualiza o dicionário do grafo,
    caso o grafo for direcionado só remove a vertice para a ligação nova, caso
    seja não dircecional remove para os dois a ligação.
    """
    vertice = input("Digite a vetice que está essa ligacao").strip()
    if vertice not in valores:
        print("Vertice não encontrada")
        return
    
    ligacao = input("Digite a ligacao para deletar: ").strip()

    if ligacao not in valores:
        print(f"{ligacao} não existe no grafo")
        return
    
    # Verifica se a ligação existe
    if ligacao not in valores[vertice]:
        print("Ligação não existe")
        return
    
    if tipo_grafo == 1:
         valores[vertice].remove(ligacao)
         print("Ligação removida com sucesso")
         print(f"Ligação removida \n \
           █████████\n \
           █▄█████▄█\n \
           █▼▼▼▼▼\n \
           █\n \
            {vertice}\n \
           █▲▲▲▲▲\n \
           █████████\n \
           ██ ██")

    elif tipo_grafo == 2:
         valores[vertice].remove(ligacao)
        # remove o inverso também
         if vertice in valores[ligacao]:
            valores[ligacao].remove(vertice)
            print(f"Vertice removida \n \
                █████████\n \
                █▄█████▄█\n \
                █▼▼▼▼▼\n \
                █\n \
                 {vertice}\n \
                █▲▲▲▲▲\n \
                █████████\n \
                ██ ██")

         print("Ligação removida com sucesso")    


            

#SITUAÇÃO: FUNCIONANDO*
def conexo_ou_desconexo(valores, tipo_grafo):
    """
    Função para verificar se um grafo é conexo ou desconexo.
    Para grafos não dirigidos (tipo_grafo == 2), usa a lógica de componentes desconexos.
    Para grafos dirigidos (tipo_grafo == 1), verifica se todos os vértices são alcançáveis a partir do primeiro vértice,
    pois um grafo dirigido é considerado conexo se houver um caminho entre qualquer par de vértices,
    ou seja, se todos os vértices forem alcançáveis a partir de um vértice inicial. 
    Se algum vértice não for alcançável, o grafo é considerado desconexo.
    """
    if tipo_grafo == 2:
        gen = varredura_Grafo_BFS(valores, 0)
        for _ in gen: # o "_" é utilizado pois não é necessário usar o valor atual do item durante a iteração(só servira para imprimir)
            pass
        try:
            nao_conexo = next(gen)# next() é utilizado para obter o próximo item de um iterador. No contexto do código, next(gen) é usado para verificar se há mais vértices a serem visitados após a varredura BFS. Se houver mais vértices, isso indica que o grafo é desconexo, e a variável nao_conexo será definida como True. Se não houver mais vértices, isso significa que todos os vértices foram visitados durante a varredura, e o grafo é conexo.
        except StopIteration as e: # StopIteration é uma exceção que é levantada para indicar que um iterador não tem mais itens para fornecer. 
            nao_conexo = e.value
        
        if nao_conexo:
            print("O grafo é desconexo")
        else:
            print("O grafo é conexo")
    elif tipo_grafo == 1:
        # Para grafos dirigidos, verifica se todos são alcançáveis a partir do primeiro vértice
        visitados = set()
        fila = collections.deque([list(valores.keys())[0]]) # cria uma fila para BFS, iniciando com o primeiro vértice do grafo
        
        while fila:
            atual = fila.popleft()# popleft() é utilizado para remover e retornar o primeiro elemento da fila.
            if atual not in visitados:
                visitados.add(atual)
                for adj in valores[atual]:
                    if adj not in visitados:
                        fila.append(adj)
        
        if len(visitados) == len(valores):
            print("O grafo é conexo")
        else:
            print("O grafo é desconexo")


#SITUAÇÃO: NÃO FUNCIONANDO, FUNCIONANDO PARA GRAFOS CONEXOS, NÃO FUNCIONANDO PARA GRAFOS NÃO CONEXOS
def fecho_trasitivo_direto(valores):
    """
    Função para calcular o fecho transitivo direto de um vértice em um grafo.
    Solicita o vértice para o usuário e utiliza a função varredura_Grafo_BFS
    para encontrar todos os vértices alcançáveis a partir do vértice inicial.
    """
    vertice = input("Digite a vertice para calcular o fecho transitivo direto: ").strip()

    if vertice not in valores:
        print("Vertice não encontrada")
        return
    
    vertices = list(valores.keys())# lista de vértices do grafo, obtida a partir das chaves do dicionário valores. Essa lista é usada para encontrar o índice do vértice inicial, que é necessário para iniciar a varredura BFS a partir do vértice correto.
    indice = vertices.index(vertice)# encontra o índice do vértice inicial na lista de vértices, para que a varredura BFS possa começar a partir desse vértice específico. O índice é usado para acessar o vértice correto na estrutura de dados do grafo durante a varredura.
    
    visitados = set()# set pois não permite elementos duplicados e tem operações de busca eficientes
    for v in varredura_Grafo_BFS(valores, indice):# o for é para percorrer os vértices visitados durante a varredura BFS, e a cada vértice visitado, ele é adicionado ao conjunto de visitados. Isso permite que o código mantenha um registro de todos os vértices que foram alcançados a partir do vértice inicial durante a varredura do grafo.
        visitados.add(v)
    
    visitados.discard(vertice)  # Remove o vértice inicial do conjunto de visitados
    print(f"Fecho transitivo direto de {vertice}: {visitados}")
    


#SITUAÇÃO: FUNCIONANDO MAS TEM QUE TESTAR MELHOR PARA GRAFOS NÃO CONEXOS
def fecho_trasitivo_inverso(valores):
    """
    Função para calcular o fecho transitivo inverso de um vértice em um grafo.
    Solicita o vértice para o usuário e utiliza BFS no grafo invertido
    para encontrar todos os vértices que podem alcançar o vértice inicial.
    """
    vertice = input("Digite a vertice para calcular o fecho transitivo inverso: ").strip()
    if vertice not in valores:
        print("Vertice não encontrada")
        return
    
    # Cria o grafo invertido
    invertido = {v: [] for v in valores}
    for v in valores:
        for vizinho in valores[v]:
            invertido[vizinho].append(v)
    
    # Usa BFS no grafo invertido, similar à varredura_Grafo_BFS
    visitados = set()
    fila = collections.deque([vertice]) # collections.deque é utilizado para criar uma fila eficiente para a BFS, permitindo adicionar e remover elementos de forma rápida. A fila é inicializada com o vértice para o qual queremos calcular o fecho transitivo inverso, e a BFS irá explorar todos os vértices que podem alcançar esse vértice no grafo invertido.
    
    # O loop while continua enquanto houver vértices na fila para explorar. A cada iteração, o vértice atual é removido da fila usando popleft(), e se ainda não foi visitado, ele é marcado como visitado e seus adjacentes no grafo invertido são adicionados à fila para serem explorados posteriormente. Isso permite que a BFS encontre todos os vértices que podem alcançar o vértice inicial no grafo original, que correspondem aos vértices alcançáveis a partir do vértice inicial no grafo invertido.
    while fila:
        atual = fila.popleft()
        if atual not in visitados:
            visitados.add(atual)
            for adjacente in invertido[atual]:
                if adjacente not in visitados:
                    fila.append(adjacente)
    
    visitados.discard(vertice)  # Remove o vértice inicial do conjunto de visitados
    print(f"Fecho transitivo inverso de {vertice}: {visitados}")                
    
def print_centralizado(texto):
    largura = shutil.get_terminal_size().columns
    for linha in texto.split("\n"):
        print(linha.center(largura))

def mostrar_desenhos():
    nome1 = "Gabriel Laus"
    nome2 = "Rafael"
    nome3 = "Guilherme Thomy"

    desenho1 = [
        "───▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄───",
        "───█▒▒░░░░░░░░░▒▒█───",
        "────█░░█░░░░░█░░█────",
        "─▄▄──█░░░▀█▀░░░█──▄▄─",
        "█░░█─▀▄░░░░░░░▄▀─█░░█"
    ]

    desenho2 = [
        "▒▒▒▒▒▒▐███████▌",
        "▒▒▒▒▒▒▐░▀░▀░▀░▌",
        "▒▒▒▒▒▒▐▄▄▄▄▄▄▄▌",
        "▄▀▀▀█▒▐░▀▀▄▀▀░▌▒█▀▀▀▄",
        "▌▌▌▌▐▒▄▌░▄▄▄░▐▄▒▌▐▐▐▐"
    ]

    desenho3 = [
        "──────▄▀▄─────▄▀▄",
        "─────▄█░░▀▀▀▀▀░░█▄",
        "─▄▄──█░░░░░░░░░░░█──▄▄",
        "█▄▄█─█░░▀░░┬░░▀░░█─█▄▄█"
    ]

    # Ajustar tamanhos (para alinhar)
    max_linhas = max(len(desenho1), len(desenho2), len(desenho3))

    while len(desenho1) < max_linhas:
        desenho1.append(" " * len(desenho1[0]))
    while len(desenho2) < max_linhas:
        desenho2.append(" " * len(desenho2[0]))
    while len(desenho3) < max_linhas:
        desenho3.append(" " * len(desenho3[0]))

    print("Disiplina de Grafos - UNIVALI\n")
    print("Professor: Rudimar Dazzi\n")
    # Print nomes centralizados
    print(f"{nome1:^25}{nome2:^50}{nome3:^40}") 

    # Print desenhos lado a lado
    for i in range(max_linhas):
        print(f"{desenho1[i]:40}{desenho2[i]:40}{desenho3[i]:40}")
def menu():
    """
    Menu que inicializa pedindo os valores dos vértices para o usuário,
    solicitando que, a cada valor, insira o caractere "," para haver
    a separação no código. Após isso, entra em um loop while onde será
    perguntado ao usuário se ele quer buscar algum valor específico.
    Caso queira (inserir 1), é solicitado o valor que deseja procurar.
    Em seguida, as varreduras DFS e BFS são executadas para encontrar esse vértice.
    Caso não encontre, o resultado será: Valor {valor_procurado} NÃO foi encontrado no DFS.
    Caso contrário, será impresso: Valor {valor_procurado} existe no grafo.
    Após isso, é feita novamente a pergunta ao usuário. Caso ele não queira
    (inserir 0), o código imprime a varredura (DFS e BFS) de todo o grafo
    e cria as matrizes direcionada e não direcionada.
    """
    try:
        menu = """
            █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
            █░░╦─╦╔╗╦─╔╗╔╗╔╦╗╔╗░░█
            █░░║║║╠─║─║─║║║║║╠─░░█
            █░░╚╩╝╚╝╚╝╚╝╚╝╩─╩╚╝░░█
            █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
        """
        print_centralizado(menu)
        valores = pedir_valores()
        tipo_grafo = int(input("O grafo é dirigido ou não dirigido? (1 = dirigida, 2 = não dirigida): "))
        valor_inicial = 0
        vertices = list(valores.keys())
        ascii_grafo = r"""
         ██████╗ ██████╗  █████╗ ███████╗ ██████╗ 
        ██╔════╝ ██╔══██╗██╔══██╗██╔════╝██╔═══██╗
        ██║  ███╗██████╔╝███████║█████╗  ██║   ██║
        ██║   ██║██╔══██╗██╔══██║██╔══╝  ██║   ██║
        ╚██████╔╝██║  ██║██║  ██║██║     ╚██████╔╝
         ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ 
        """
        while True: 
            #print("===================================================================================================================================================================================\n")       
            print_centralizado(ascii_grafo)
            #print("===================================================================================================================================================================================\n")
            print("O que deseja fazer? \n 1 = Criar matriz \n 2 = Varredura do grafo \n 3 = Adicionar vertice \n 4 = Adicionar ligação \n 5 = Remover vertice \n 6 = Remover ligação \n 7 = Verificar se o grafo é conexo ou desconexo \n 8 = Fecho transitivo direto \n 9 = Fecho transitivo inverso \n 10 = Autores")
            valor_case = int(input("Opção: "))
            match valor_case:

                #CRIAÇÃO DA MATRIZ
                case 1:
                    print("================== Matriz do Grafo =================\n")
                    if tipo_grafo == 1:
                        matriz_dirigida = criar_Matriz(valores)
                        print("   ", "  ".join(vertices))

                        for i, linha in enumerate(matriz_dirigida):#enumerate() é utilizado para obter o índice e o valor de cada item em uma lista durante a iteração. No contexto do código, for i, linha in enumerate(matriz_dirigida) permite iterar sobre cada linha da matriz de adjacência, onde i é o índice da linha (correspondente ao vértice) e linha é a própria linha da matriz. Isso é útil para imprimir a matriz de forma organizada, associando cada linha ao vértice correspondente.
                            print(vertices[i], linha)

                    elif tipo_grafo == 2:
                        matriz_nao_dirigida = criar_Matriz(valores)
                        print("   ", "  ".join(vertices))

                        for i, linha in enumerate(matriz_nao_dirigida):
                            print(vertices[i], linha)        
                    else:
                        print("Valor invalida")
                        continue           
                    print("\n====================================================\n")             
                
                #VARREDURA DO GRAFO
                case 2:
                    varredura = int(input("Queres preocurar um valor ou queres fazer uma varredura geral DFS ou BFS(1 = procurar valor especifico, 2 = DFS, 3 = BFS)"))
                    if varredura == 1:
                        valor_procurado = input("Qual valor queres preocurar: ")
                        if valor_procurado not in valores:
                            print(f"Valor {valor_procurado} não está no grafo")
                            continue
                
                        print("\n================= DFS =================\n")
                
                        if any(v == valor_procurado for v in varredura_Grafo_DFS(valores,valor_inicial)):# any() consome o gerador e para assim que encontrar o valor TRUE ou FALSE
                    
                            print(f"\n           Valor {valor_procurado} existe no grafo")
                        else:
                    
                            print(f"\n           Valor {valor_procurado} NÃO foi encontrado no DFS")
                    
                        print("\n=======================================\n")
                
                
                        print("\n================= BFS =================\n")
                        if any(v == valor_procurado for v in varredura_Grafo_BFS(valores,valor_inicial)):# mesma coisa do DFS 
                    
                            print(f"\n           Valor {valor_procurado} existe no grafo")
                            continue    
                    
                        else:
                    
                            print(f"\n           Valor {valor_procurado} NÃO foi encontrado no BFS")   
                            continue    
                        print("\n=======================================\n")

                    elif varredura == 2:
                        print("\n====================Varredura do Grafo DFS (Geral)===========================\n   ")
                        for _ in varredura_Grafo_DFS(valores,valor_inicial): # o "_" é utilizado pois não é necessário usar o valor atual do item durante a iteração(só servira para imprimir)
                            pass
    
                        print("\n==============================================================================\n") 
                        continue

                    elif varredura == 3:
                        print("\n=====================Varredura do Grafo BFS (Geral)========================\n    ")
                
                        for _ in varredura_Grafo_BFS(valores,valor_inicial): # o "_" é utilizado pois não é necessário usar o valor atual do item durante a iteração(só servira para imprimir)
                            pass
                
                        print("\n============================================================================\n")
                        continue


                #ADICIONAR VERTICE 
                case 3:
                    print("================== Adicionar Vertice =================\n")
                    adicionar_vertice(valores,tipo_grafo)
                    vertices = list(valores.keys())
                    print("\n====================================================\n")
                #    
                case 4:
                    print("================== Adicionar Ligação =================\n")
                    adicionar_ligacao(valores,tipo_grafo)
                    vertices = list(valores.keys())
                    print("\n====================================================\n")
                #
                case 5:
                    print("================== Remover Vertice =================\n")
                    remove_vertice(valores)
                    vertices = list(valores.keys())
                    print("\n====================================================\n")
                #
                case 6:
                    print("================== Remover Ligação =================\n") 
                    remove_ligacao(valores,tipo_grafo)
                    vertices = list(valores.keys())
                    print("\n====================================================\n")   
                #
                case 7:
                    print("================== Verificar se o grafo é conexo ou desconexo =================\n")
                    conexo_ou_desconexo(valores,tipo_grafo)
                    print("\n====================================================\n")
                #
                case 8:
                    print("================== Fecho Transitivo Direto =================\n")
                    fecho_trasitivo_direto(valores)
                    print("\n====================================================\n")
                #
                case 9:
                    print("================== Fecho Transitivo Inverso =================\n")
                    fecho_trasitivo_inverso(valores)
                    print("\n====================================================\n")
                #
                case 10:
                    print("================== Autores =================\n")
                    mostrar_desenhos()
                    print("\n====================================================\n")
                case _:
                    print("Valor inserido invalido ")                                

        
    except ValueError:
     print("Error: Numero inserido invalido.")
    except Exception as e:
     print(f"Ocorreu um erro: {e}")
    finally:
     print("Execution finished.")


menu()
    
    
