import tkinter as tk
import time
import random

# Definições de cores
WHITE_COLOR = "#FFFFFF"
BLACK_COLOR = "#000000"
QUEEN_COLORS = [
    "#FF0000",  # Vermelho
    "#0000FF",  # Azul
    "#008000",  # Verde
    "#FFA500",  # Laranja
    "#800080",  # Roxo
    "#00FFFF",  # Ciano
    "#FFC0CB",  # Rosa
    "#A52A2A",  # Marrom
    "#FFFF00",  # Amarelo
    "#00FF00"   # Lime
]

def draw_board_tkinter(canvas, N):
    """
    Desenha o tabuleiro de xadrez no Canvas do Tkinter.

    Args:
        canvas: Widget Canvas do Tkinter onde o tabuleiro será desenhado.
        N: Tamanho do tabuleiro (N x N).
    """
    tile_size = calculate_tile_size(canvas, N)
    canvas.delete("all")  # Limpa o canvas antes de desenhar

    for row in range(N):
        for col in range(N):
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            x1 = col * tile_size
            y1 = row * tile_size
            x2 = x1 + tile_size
            y2 = y1 + tile_size
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

def calculate_tile_size(canvas, N):
    """
    Calcula o tamanho de cada tile baseado no tamanho do canvas e N.

    Args:
        canvas: Widget Canvas do Tkinter.
        N: Tamanho do tabuleiro (N x N).

    Returns:
        Tamanho do tile em pixels.
    """
    canvas_width = int(canvas['width'])
    canvas_height = int(canvas['height'])
    tile_size = min(canvas_width, canvas_height) // N
    return tile_size

def animate_solution(canvas, chromosome, N):
    """
    Anima as rainhas movendo-se para suas posições finais.

    Args:
        canvas: Widget Canvas do Tkinter onde o tabuleiro será desenhado.
        chromosome: Objeto Chromosome que representa a solução.
        N: Tamanho do tabuleiro (N x N).
    """
    tile_size = calculate_tile_size(canvas, N)
    queens = []

    # Inicializa as rainhas em posições aleatórias
    for row in range(8):
        initial_col = random.randint(0, N-1)
        color = QUEEN_COLORS[row % len(QUEEN_COLORS)]
        queen = canvas.create_oval(
            initial_col * tile_size + 10,
            row * tile_size + 10,
            initial_col * tile_size + tile_size - 10,
            row * tile_size + tile_size - 10,
            fill=color
        )
        queens.append((row, initial_col, queen))

    canvas.update()

    # Move cada rainha para sua posição final
    for row, initial_col, queen in queens:
        final_col = chromosome.genes[row]
        dx = (final_col - initial_col) * tile_size
        steps = 20
        delay = 0.02  # Tempo entre passos em segundos

        for step in range(steps):
            canvas.move(queen, dx / steps, 0)
            canvas.update()
            time.sleep(delay)

def print_board_tkinter(chromosome, N, text_widget):
    """
    Imprime o tabuleiro no widget Text do Tkinter de forma formatada.

    Args:
        chromosome: Objeto Chromosome que representa a solução.
        N: Tamanho do tabuleiro (N x N).
        text_widget: Widget Text do Tkinter onde a solução será exibida.
    """
    text_widget.insert(tk.END, "\nSolução Encontrada:\n\n")
    for row in range(8):
        line = ['.'] * N
        line[chromosome.genes[row]] = 'Q'
        text_widget.insert(tk.END, " ".join(line) + "\n")
    text_widget.insert(tk.END, "\n")

def find_conflicting_queens(chromosome, N):
    """
    Identifica as rainhas que estão em conflito.

    Args:
        chromosome: Objeto Chromosome que representa a solução.
        N: Tamanho do tabuleiro (N x N).

    Returns:
        Lista de tuplas representando pares de rainhas em conflito.
    """
    conflicts = []
    for i in range(8):
        for j in range(i + 1, 8):
            if chromosome.genes[i] == chromosome.genes[j]:
                conflicts.append(((i + 1, chromosome.genes[i] + 1), (j + 1, chromosome.genes[j] + 1)))
            elif abs(chromosome.genes[i] - chromosome.genes[j]) == abs(i - j):
                conflicts.append(((i + 1, chromosome.genes[i] + 1), (j + 1, chromosome.genes[j] + 1)))
    return conflicts
