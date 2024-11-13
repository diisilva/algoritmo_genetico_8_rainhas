import tkinter as tk
from tkinter import ttk, messagebox
from genetic_algorithm import GeneticAlgorithm
from helpers import draw_board_tkinter, animate_solution, print_board_tkinter, find_conflicting_queens
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo Genético - Problema das 8-Rainhas em Tabuleiro N x N")

        # Configuração do layout usando grid
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=2)  # Aumenta o espaço para o tabuleiro
        self.root.rowconfigure(2, weight=1)  # Diminui o espaço para o gráfico

        # Frame para os controles
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky="NSEW")

       # Labels e Entradas para parâmetros com valores padrão
        # Linha 0: Tamanho do Tabuleiro (N)
        ttk.Label(control_frame, text="Tamanho do Tabuleiro (N):").grid(row=0, column=0, sticky="W", pady=2)
        self.n_entry = ttk.Entry(control_frame, width=10)
        self.n_entry.insert(0, "8")  # Valor padrão
        self.n_entry.grid(row=0, column=1, sticky="W", pady=2)
        ttk.Label(control_frame, text="Define o tamanho do tabuleiro NxN (mínimo 8).").grid(row=0, column=2, sticky="W", padx=5, pady=2)

        # Linha 1: Tamanho da População
        ttk.Label(control_frame, text="Tamanho da População:").grid(row=1, column=0, sticky="W", pady=2)
        self.population_entry = ttk.Entry(control_frame, width=10)
        self.population_entry.insert(0, "125")  # Valor padrão
        self.population_entry.grid(row=1, column=1, sticky="W", pady=2)
        ttk.Label(control_frame, text="Número de indivíduos na população inicial.").grid(row=1, column=2, sticky="W", padx=5, pady=2)

        # Linha 2: Probabilidade de Mutação
        ttk.Label(control_frame, text="Probabilidade de Mutação:").grid(row=2, column=0, sticky="W", pady=2)
        self.mutation_entry = ttk.Entry(control_frame, width=10)
        self.mutation_entry.insert(0, "0.05")  # Valor padrão
        self.mutation_entry.grid(row=2, column=1, sticky="W", pady=2)
        ttk.Label(control_frame, text="Chance de alterar genes durante a mutação.").grid(row=2, column=2, sticky="W", padx=5, pady=2)

        # Linha 3: Probabilidade de Crossover
        ttk.Label(control_frame, text="Probabilidade de Crossover:").grid(row=3, column=0, sticky="W", pady=2)
        self.crossover_entry = ttk.Entry(control_frame, width=10)
        self.crossover_entry.insert(0, "0.7")  # Valor padrão
        self.crossover_entry.grid(row=3, column=1, sticky="W", pady=2)
        ttk.Label(control_frame, text="Chance de combinar genes entre pais.").grid(row=3, column=2, sticky="W", padx=5, pady=2)

        # Linha 4: Número de Gerações
        ttk.Label(control_frame, text="Número de Gerações:").grid(row=4, column=0, sticky="W", pady=2)
        self.generations_entry = ttk.Entry(control_frame, width=10)
        self.generations_entry.insert(0, "125")  # Valor padrão
        self.generations_entry.grid(row=4, column=1, sticky="W", pady=2)
        ttk.Label(control_frame, text="Máximo de iterações do algoritmo.").grid(row=4, column=2, sticky="W", padx=5, pady=2)

        # Linha 5: Elite Size
        ttk.Label(control_frame, text="Elite Size:").grid(row=5, column=0, sticky="W", pady=2)
        self.elite_entry = ttk.Entry(control_frame, width=10)
        self.elite_entry.insert(0, "5")  # Valor padrão
        self.elite_entry.grid(row=5, column=1, sticky="W", pady=2)
        ttk.Label(control_frame, text="Número de melhores indivíduos preservados a cada geração.").grid(row=5, column=2, sticky="W", padx=5, pady=2)

        # Botão para iniciar o Algoritmo Genético
        self.start_button = ttk.Button(control_frame, text="Iniciar Algoritmo", command=self.start_algorithm)
        self.start_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Botão About
        self.about_button = ttk.Button(control_frame, text="About", command=self.show_about)
        self.about_button.grid(row=7, column=0, columnspan=2, pady=5)

        # Frame para exibir a solução no console, agora abaixo do control_frame
        solution_frame = ttk.Frame(self.root, padding="10")
        solution_frame.grid(row=1, column=0, sticky="NSEW")
        solution_frame.columnconfigure(0, weight=1)
        solution_frame.rowconfigure(1, weight=1)
        ttk.Label(solution_frame, text="Solução no Console:").grid(row=0, column=0, sticky="W")
        self.text_widget = tk.Text(solution_frame, height=10, width=40)  # Ajuste a largura conforme necessário
        self.text_widget.grid(row=1, column=0, sticky="NSEW")

        # Frame para o tabuleiro de xadrez (Aumentado para ocupar mais espaço)
        board_frame = ttk.Frame(self.root, padding="10")
        board_frame.grid(row=0, column=1, rowspan=2, sticky="NSEW")  # Expandindo para ocupar duas linhas
        board_frame.columnconfigure(0, weight=1)
        board_frame.rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(board_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="NSEW")

        # Frame para o gráfico de progresso (Diminuído para ocupar menos espaço)
        graph_frame = ttk.Frame(self.root, padding="10")
        graph_frame.grid(row=2, column=1, sticky="NSEW")
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)
        self.figure, self.ax = plt.subplots(figsize=(5, 2.5))  # Diminuindo o tamanho do gráfico
        self.ax.set_title("Progresso do Algoritmo Genético")
        self.ax.set_xlabel("Geração")
        self.ax.set_ylabel("Número de Conflitos")
        self.ax.grid(True)
        self.line, = self.ax.plot([], [], 'r-')
        self.canvas_fig = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas_fig.draw()
        self.canvas_fig.get_tk_widget().grid(row=0, column=0, sticky="NSEW")

    def show_about(self):
        """
        Exibe uma janela pop-up com informações sobre o aplicativo.
        """
        about_text = (
            "Algoritmo Genético para o Problema das 8-Rainhas em Tabuleiro N x N\n\n"
            "Este aplicativo utiliza um poderoso Algoritmo Genético para resolver o clássico Problema das 8-Rainhas. "
            "O objetivo é posicionar 8 rainhas em um tabuleiro N x N de maneira que nenhuma rainha possa atacar outra, "
            "ou seja, nenhuma rainha está na mesma linha, coluna ou diagonal de outra.\n\n"
            "Características Principais:\n"
            "- **Seleção Estratégica:** Combinação eficiente dos métodos de Seleção por Torneio e Roleta para escolher os melhores indivíduos da população.\n"
            "- **Crossover Adaptado:** Implementação de crossover específico para 8 genes, garantindo a recombinação eficaz das soluções.\n"
            "- **Mutação Inteligente:** Aplicação de mutações por troca de genes para introduzir diversidade genética e evitar a convergência prematura.\n"
            "- **Visualização Gráfica:** Monitoramento em tempo real do progresso do algoritmo através de gráficos dinâmicos que mostram a evolução dos conflitos.\n"
            "- **Animação das Soluções:** Animação das rainhas movendo-se suavemente para suas posições finais quando uma solução válida é encontrada.\n"
            "- **Verificação de Validade:** Validação automática das soluções para garantir que nenhuma rainha está em posição de ataque, proporcionando confiança nos resultados obtidos.\n"
            "- **Interface Intuitiva:** Design amigável e responsivo, facilitando a interação e configuração dos parâmetros do algoritmo.\n"
        )

        messagebox.showinfo("About", about_text)

    def start_algorithm(self):
        try:
            # Obter parâmetros do usuário com valores padrão
            N = int(self.n_entry.get())
            population_size = int(self.population_entry.get())
            mutation_prob = float(self.mutation_entry.get())
            crossover_prob = float(self.crossover_entry.get())
            generations = int(self.generations_entry.get())
            elite_size = int(self.elite_entry.get())

            if N < 8:
                messagebox.showerror("Erro", "O tamanho do tabuleiro deve ser pelo menos 8.")
                return

            # Atualizar variáveis
            self.N = N
            self.population_size = population_size
            self.mutation_prob = mutation_prob
            self.crossover_prob = crossover_prob
            self.generations = generations
            self.elite_size = elite_size

            # Ajustar o tamanho do Canvas baseado em N (limite máximo de tamanho)
            max_canvas_size = 600
            tile_size = calculate_tile_size(self.canvas, self.N, max_canvas_size)
            canvas_size = tile_size * self.N
            self.canvas.config(width=canvas_size, height=canvas_size)

            # Desenhar o tabuleiro inicial
            draw_board_tkinter(self.canvas, self.N)

            # Limpar gráfico e texto
            self.ax.cla()
            self.ax.set_title("Progresso do Algoritmo Genético")
            self.ax.set_xlabel("Geração")
            self.ax.set_ylabel("Número de Conflitos")
            self.ax.grid(True)
            self.line, = self.ax.plot([], [], 'r-')
            self.canvas_fig.draw()

            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert(tk.END, "Detalhes das Gerações:\n\n")

            # Desabilitar o botão enquanto o algoritmo está rodando
            self.start_button.config(state=tk.DISABLED)

            # Executar o algoritmo genético em uma nova thread
            thread = threading.Thread(target=self.run_genetic_algorithm)
            thread.start()

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos para todos os parâmetros.")

    def run_genetic_algorithm(self):
        # Instanciar o Algoritmo Genético
        ga = GeneticAlgorithm(
            N=self.N,
            population_size=self.population_size,
            mutation_prob=self.mutation_prob,
            crossover_prob=self.crossover_prob,
            generations=self.generations,
            elite_size=self.elite_size
        )

        # Função de callback para atualizar a GUI após cada geração
        def callback(generation, fitness, conflicts):
            # Atualizar gráfico
            self.ax.cla()
            self.ax.set_title("Progresso do Algoritmo Genético")
            self.ax.set_xlabel("Geração")
            self.ax.set_ylabel("Número de Conflitos")
            self.ax.grid(True)
            self.ax.plot(range(1, generation + 1), ga.conflicts_history, 'r-')
            self.canvas_fig.draw()

            # Atualizar o console de solução com detalhes por geração
            self.text_widget.insert(tk.END, f"Geração {generation}: Melhor Aptidão = {fitness:.4f}, Conflitos = {conflicts}\n")
            self.text_widget.see(tk.END)

        # Executar o Algoritmo Genético
        best_solution = ga.run(callback=callback)

        # Atualizar o gráfico final
        self.ax.cla()
        self.ax.set_title("Progresso do Algoritmo Genético")
        self.ax.set_xlabel("Geração")
        self.ax.set_ylabel("Número de Conflitos")
        self.ax.grid(True)
        self.ax.plot(range(1, len(ga.conflicts_history) + 1), ga.conflicts_history, 'r-')
        self.canvas_fig.draw()

        # Verificar se a solução é válida
        if best_solution.conflicts == 0:
            # Animar a solução encontrada
            animate_solution(self.canvas, best_solution, self.N)

            # Exibir a solução no console
            print_board_tkinter(best_solution, self.N, self.text_widget)
        else:
            # Encontrar rainhas conflitantes
            conflicts = find_conflicting_queens(best_solution, self.N)
            conflict_msg = "Nenhuma solução válida encontrada com os parâmetros fornecidos.\n\nRainhas em conflito:\n"
            for (queen1, queen2) in conflicts:
                conflict_msg += f"Rainha {queen1[0]} (Coluna {queen1[1]}) <--> Rainha {queen2[0]} (Coluna {queen2[1]})\n"

            # Exibir a mensagem no widget Text
            self.text_widget.insert(tk.END, conflict_msg)
            self.text_widget.see(tk.END)

            # Exibir uma mensagem de aviso na GUI
            messagebox.showwarning("Aviso", "Não foi possível encontrar uma solução válida com os parâmetros fornecidos.\n"
                                            "Considere ajustar os parâmetros e tentar novamente.")

        # Reabilitar o botão
        self.start_button.config(state=tk.NORMAL)

    def on_closing(self):
        """
        Função para lidar com o fechamento da janela.
        """
        self.root.destroy()

def calculate_tile_size(canvas, N, max_size):
    """
    Calcula o tamanho de cada tile baseado no tamanho máximo permitido.

    Args:
        canvas: Widget Canvas do Tkinter.
        N: Tamanho do tabuleiro (N x N).
        max_size: Tamanho máximo do canvas em pixels.

    Returns:
        Tamanho do tile em pixels.
    """
    tile_size = max_size // N
    return tile_size

def main():
    root = tk.Tk()
    app = NQueensGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
