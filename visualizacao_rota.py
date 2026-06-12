import tkinter as tk

def visualizar_rota_horizontal(caminho, custo_total=None, titulo="Rota do A*"):
    janela = tk.Tk()
    janela.title(titulo)

    largura = 1200
    altura = 300
    canvas = tk.Canvas(janela, width=largura, height=altura, bg="white")
    canvas.pack()

    margem_x = 100
    y = altura // 2
    espaco = 180
    raio = 28

    posicoes = {}

    # posições dos vértices em linha horizontal
    for i, cidade in enumerate(caminho):
        x = margem_x + i * espaco
        posicoes[cidade] = (x, y)

    # desenha as setas entre as cidades
    for i in range(len(caminho) - 1):
        a = caminho[i]
        b = caminho[i + 1]

        x1, y1 = posicoes[a]
        x2, y2 = posicoes[b]

        canvas.create_line(
            x1 + raio, y1,
            x2 - raio, y2,
            fill="green",
            width=4,
            arrow=tk.LAST
        )

    # desenha os nós
    for i, cidade in enumerate(caminho):
        x, y = posicoes[cidade]

        if i == 0:
            cor = "dodgerblue"   # origem
        elif i == len(caminho) - 1:
            cor = "orange"       # destino
        else:
            cor = "lightgreen"   # intermediários

        canvas.create_oval(
            x - raio, y - raio,
            x + raio, y + raio,
            fill=cor,
            outline="black",
            width=2
        )

        canvas.create_text(
            x, y,
            text=cidade,
            font=("Arial", 11, "bold")
        )

    if custo_total is not None:
        canvas.create_text(
            largura // 2, 40,
            text=f"Custo total: {custo_total:.1f} km",
            font=("Arial", 14, "bold")
        )

    janela.mainloop()
