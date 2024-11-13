import random
import heapq

class Chromosome:
    def __init__(self, genes, N):
        """
        Inicializa um cromossomo com 8 genes representando as posições das rainhas.

        Args:
            genes: Lista de 8 inteiros representando a coluna de cada rainha nas linhas 0 a 7.
            N: Tamanho do tabuleiro (N x N).
        """
        self.genes = genes  # Lista de 8 colunas para as 8 linhas
        self.N = N
        self.fitness = 0
        self.conflicts = 0
        self.calculate_fitness()

    def calculate_fitness(self):
        """
        Calcula o número de conflitos e a aptidão do cromossomo.
        A aptidão é inversamente proporcional ao número de conflitos.
        """
        self.conflicts = 0
        for i in range(8):
            for j in range(i + 1, 8):
                if self.genes[i] == self.genes[j]:
                    self.conflicts += 1  # Conflito na mesma coluna
                elif abs(self.genes[i] - self.genes[j]) == abs(i - j):
                    self.conflicts += 1  # Conflito na diagonal
        self.fitness = 1 / (1 + self.conflicts)

    def __lt__(self, other):
        """
        Define a ordem baseada na aptidão para uso em estruturas como heap.

        Args:
            other: Outro cromossomo para comparação.

        Returns:
            True se este cromossomo tiver maior aptidão que o outro.
        """
        return self.fitness > other.fitness  # Maior fitness tem prioridade

class GeneticAlgorithm:
    def __init__(self, N, population_size=100, mutation_prob=0.05, crossover_prob=0.8, generations=1000, elite_size=5):
        """
        Inicializa o Algoritmo Genético para o problema das 8-Rainhas em um tabuleiro N x N.

        Args:
            N: Tamanho do tabuleiro (N x N).
            population_size: Número de cromossomos na população.
            mutation_prob: Probabilidade de mutação de um cromossomo.
            crossover_prob: Probabilidade de realizar crossover entre dois pais.
            generations: Número máximo de gerações a serem executadas.
            elite_size: Número de melhores cromossomos preservados em cada geração.
        """
        self.N = N  # Tamanho do tabuleiro (N x N)
        self.population_size = population_size
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.generations = generations
        self.elite_size = elite_size
        self.population = self.create_initial_population()
        self.best_chromosome = max(self.population, key=lambda c: c.fitness)
        self.no_improvement = 0
        self.conflicts_history = []  # Para plotagem do progresso

    def create_initial_population(self):
        """
        Gera uma população inicial aleatória de cromossomos.

        Returns:
            Lista de objetos Chromosome.
        """
        population = []
        for _ in range(self.population_size):
            genes = [random.randint(0, self.N - 1) for _ in range(8)]
            population.append(Chromosome(genes, self.N))
        return population

    def roulette_selection(self):
        """
        Seleciona um cromossomo usando o método de roleta.

        Returns:
            Objeto Chromosome selecionado.
        """
        fitness_sum = sum(c.fitness for c in self.population)
        selection_probs = [c.fitness / fitness_sum for c in self.population]
        selected = random.choices(self.population, weights=selection_probs, k=1)[0]
        return selected

    def tournament_selection(self, k=3):
        """
        Seleciona um cromossomo pelo método de torneio.

        Args:
            k: Número de cromossomos a participar do torneio.

        Returns:
            Objeto Chromosome selecionado.
        """
        selected = random.sample(self.population, k)
        return max(selected, key=lambda c: c.fitness)

    def crossover(self, parent1, parent2):
        """
        Realiza o crossover para gerar um filho a partir de dois pais.

        Args:
            parent1: Cromossomo pai 1.
            parent2: Cromossomo pai 2.

        Returns:
            Objeto Chromosome filho.
        """
        child_genes = parent1.genes.copy()
        if random.random() < self.crossover_prob:
            # Escolher pontos de crossover
            start, end = sorted(random.sample(range(8), 2))
            child_genes[start:end + 1] = parent2.genes[start:end + 1]
        return Chromosome(child_genes, self.N)

    def mutate(self, chromosome):
        """
        Aplica mutação ao cromossomo trocando a coluna de uma rainha.

        Args:
            chromosome: Objeto Chromosome a ser mutado.
        """
        for i in range(8):
            if random.random() < self.mutation_prob:
                chromosome.genes[i] = random.randint(0, self.N - 1)
        chromosome.calculate_fitness()

    def evolve_population(self):
        """
        Evolui a população para a próxima geração.
        """
        new_population = []
        # Elitismo: preserva os melhores cromossomos
        elites = heapq.nlargest(self.elite_size, self.population, key=lambda c: c.fitness)
        new_population.extend(elites)

        # Geração dos novos indivíduos
        while len(new_population) < self.population_size:
            parent1 = self.tournament_selection()
            parent2 = self.roulette_selection()
            child = self.crossover(parent1, parent2)
            self.mutate(child)
            new_population.append(child)

        # Atualiza a população
        self.population = new_population
        self.update_best_chromosome()

    def update_best_chromosome(self):
        """
        Atualiza o melhor cromossomo encontrado.
        """
        current_best = max(self.population, key=lambda c: c.fitness)
        if current_best.fitness > self.best_chromosome.fitness:
            self.best_chromosome = current_best
            self.no_improvement = 0
        else:
            self.no_improvement += 1
            if self.no_improvement >= 100:
                # Aumenta a taxa de mutação para promover diversidade
                self.mutation_prob = min(self.mutation_prob * 1.1, 0.5)

    def run(self, callback=None):
        """
        Executa o algoritmo genético e retorna o melhor cromossomo encontrado.

        Args:
            callback: Função a ser chamada após cada geração, para atualizar a GUI.

        Returns:
            Objeto Chromosome com a melhor solução.
        """
        for generation in range(1, self.generations + 1):
            self.evolve_population()
            self.conflicts_history.append(self.best_chromosome.conflicts)
            print(f"Geração {generation}: Melhor Aptidão = {self.best_chromosome.fitness:.4f}, Conflitos = {self.best_chromosome.conflicts}")

            # Chama o callback para atualizar a GUI
            if callback:
                callback(generation, self.best_chromosome.fitness, self.best_chromosome.conflicts)

            # Condição de parada: solução sem conflitos
            if self.best_chromosome.conflicts == 0:
                print(f"Solução encontrada na geração {generation}!")
                break

        return self.best_chromosome
