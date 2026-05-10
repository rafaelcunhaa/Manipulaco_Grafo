# Manipulação de Grafos

Projeto desenvolvido para implementar e explorar conceitos fundamentais da Teoria dos Grafos, incluindo criação, manipulação, análise e visualização interativa de grafos.

---

## Descrição

Este projeto permite trabalhar com diferentes operações e algoritmos relacionados a grafos, utilizando estruturas de dados baseadas em listas de adjacência.

O sistema possui funcionalidades para:

- Criação de grafos dirigidos e não dirigidos
- Manipulação de vértices e arestas
- Percursos em grafos
- Verificação de conexidade
- Fecho transitivo
- Coloração heurística de vértices
- Visualização gráfica interativa

O projeto foi desenvolvido com foco educacional, visando auxiliar no aprendizado de Estruturas de Dados e Algoritmos em Grafos.

---

#  Funcionalidades

## Manipulação de Grafos
- Adição de vértices
- Remoção de vértices
- Adição de arestas
- Remoção de arestas

## Representações
- Lista de adjacência
- Matriz de adjacência

## Algoritmos Implementados
- Busca em Largura (BFS)
- Busca em Profundidade (DFS)
- Verificação de conexidade
- Fecho transitivo direto
- Fecho transitivo inverso
- Coloração heurística de grafos

## Visualização Gráfica
- Interface gráfica interativa utilizando Tkinter
- Movimentação dos vértices com o mouse
- Visualização colorida dos grafos
- Atualização dinâmica das arestas

---

# Tecnologias Utilizadas

- **Linguagem:** Python
- **Paradigma:** Programação Estruturada
- **Bibliotecas utilizadas:**
  - `collections`
  - `tkinter`
  - `random`
  - `matplotlib`
  - `networkx`

---

# Estrutura do Projeto
```
Manipulaco_Grafo/
│ 
├── main.py          # Arquivo principal do projeto
└── README.md        # Documentação do projeto
```

# Como Executar
## 1️⃣ Clone o repositório
```
git clone https://github.com/rafaelcunhaa/Manipulaco_Grafo.git
```

## 2️⃣ Acesse a pasta do projeto
```
cd Manipulaco_Grafo
```
## 3️⃣ Instale as dependências
```
python -m pip install networkx matplotlib
```
## 4️⃣ Execute o projeto
```
python main.py
```

É necessário possuir o Python instalado na máquina.

# 📖 Exemplo de Uso
Entrada do usuário
```
Qual numeros terá no grafo?
A,B,C,D

Informe qual numero faz ligação com o A:
B,C

Informe qual numero faz ligação com o B:
A,D

Informe qual numero faz ligação com o C:
A,D

Informe qual numero faz ligação com o D:
B,C
```
```
Funcionalidades disponíveis no menu
1 = Criar matriz
2 = Varredura do grafo
3 = Adicionar vértice
4 = Adicionar ligação
5 = Remover vértice
6 = Remover ligação
7 = Verificar conexidade
8 = Fecho transitivo direto
9 = Fecho transitivo inverso
10 = Colorir grafo
11 = Visualizar grafo
12 = Autores
```
# Visualização Gráfica

O projeto possui uma interface gráfica interativa para visualização dos grafos.

Funcionalidades da interface:

- Movimentação dos vértices com o mouse
- Visualização das arestas em tempo real
- Coloração automática dos vértices

# 👨‍💻 Autores
- Rafael Cunha
- Gabriel Laus
- Guilherme Thomy
- Representação visual de grafos dirigidos e não dirigidos



