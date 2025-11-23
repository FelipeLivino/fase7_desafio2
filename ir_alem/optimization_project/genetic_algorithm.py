import random
import copy
import time

class GeneticAlgorithm:
    """
        Algoritmo Genético para o Problema da Mochila (Otimização FarmTech).

        Argumentos:
        items (lista): Lista de dicionários com 'custo' e 'produtividade'.
        budget (int): Custo máximo permitido.
        pop_size (int): Tamanho da população.
        generations (int): Número de gerações a serem executadas.
        mutation_rate (float): Probabilidade de mutação por gene.
        selection_method (str): 'roleta' ou 'torneio'.
        crossover_method (str): 'ponto_único' ou 'uniforme'.
        mutation_method (str): 'inversão_de_bits' ou 'troca'.
        elitism_count (int): Número de indivíduos com melhor desempenho a serem mantidos.
        seed (int): Semente aleatória.
    """
    def __init__(self, items, budget, 
                 pop_size=100, 
                 generations=50, 
                 mutation_rate=0.01,
                 selection_method='roulette',
                 crossover_method='single_point',
                 mutation_method='bit_flip',
                 elitism_count=2,
                 seed=None):
        
        self.items = items
        self.budget = budget
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.selection_method = selection_method
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self.elitism_count = elitism_count
        
        if seed is not None:
            random.seed(seed)
            
        self.num_genes = len(items)
        self.population = []
        self.best_solution = None
        self.best_fitness = 0
        self.history = [] # Para acompanhar o progresso

    def _initialize_population(self):
        """Gera uma população inicial aleatória."""
        self.population = []
        for _ in range(self.pop_size):
            # sequência binária aleatória
            chromosome = [random.randint(0, 1) for _ in range(self.num_genes)]
            self.population.append(chromosome)

    def _calculate_fitness(self, chromosome):
        """
        Calcula a aptidão (produtividade total).
        Retorna 0 se o custo exceder o orçamento.
        """
        total_cost = 0
        total_prod = 0
        for i, gene in enumerate(chromosome):
            if gene == 1:
                total_cost += self.items[i]['cost']
                total_prod += self.items[i]['productivity']
        
        if total_cost > self.budget:
            return 0 # Penalidade por soluções inválidas
        return total_prod

    def _selection_roulette(self, fitnesses):
        total_fitness = sum(fitnesses)
        if total_fitness == 0:
            return random.choice(self.population)
            
        pick = random.uniform(0, total_fitness)
        current = 0
        for i, fitness in enumerate(fitnesses):
            current += fitness
            if current > pick:
                return self.population[i]
        return self.population[-1]

    def _selection_tournament(self, fitnesses, k=3):
        # # Selecione k indivíduos aleatórios
        indices = random.sample(range(self.pop_size), k)
        best_idx = indices[0]
        for idx in indices:
            if fitnesses[idx] > fitnesses[best_idx]:
                best_idx = idx
        return self.population[best_idx]

    def _crossover_single_point(self, parent1, parent2):
        if random.random() > 0.8: # Probabilidade de cruzamento (geralmente alta)
            return parent1, parent2
            
        point = random.randint(1, self.num_genes - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    def _crossover_uniform(self, parent1, parent2):
        child1 = []
        child2 = []
        for i in range(self.num_genes):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        return child1, child2

    def _mutation_bit_flip(self, chromosome):
        for i in range(self.num_genes):
            if random.random() < self.mutation_rate:
                chromosome[i] = 1 - chromosome[i]
        return chromosome

    def _mutation_swap(self, chromosome):
        # Isso é mais comum em problemas de permutação (TSP), mas também pode adicionar diversidade aqui.
        # Para binário, basta trocar 0s e 1s em posições diferentes.
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(self.num_genes), 2)
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return chromosome

    def run(self):
        start_time = time.time()
        self._initialize_population()
        
        for gen in range(self.generations):
            fitnesses = [self._calculate_fitness(ind) for ind in self.population]
            
            # Encontre a melhor solução da geração atual
            max_fitness = max(fitnesses)
            if max_fitness > self.best_fitness:
                self.best_fitness = max_fitness
                best_idx = fitnesses.index(max_fitness)
                self.best_solution = copy.deepcopy(self.population[best_idx])
            
            self.history.append({
                'generation': gen,
                'best_fitness': self.best_fitness,
                'avg_fitness': sum(fitnesses) / len(fitnesses)
            })
            
            # Elitismo
            sorted_indices = sorted(range(len(fitnesses)), key=lambda k: fitnesses[k], reverse=True)
            new_population = [self.population[i] for i in sorted_indices[:self.elitism_count]]
            
            # Criar uma nova geração
            while len(new_population) < self.pop_size:
                if self.selection_method == 'tournament':
                    p1 = self._selection_tournament(fitnesses)
                    p2 = self._selection_tournament(fitnesses)
                else:
                    p1 = self._selection_roulette(fitnesses)
                    p2 = self._selection_roulette(fitnesses)
                
                # Crossover
                if self.crossover_method == 'uniform':
                    c1, c2 = self._crossover_uniform(p1, p2)
                else: 
                    c1, c2 = self._crossover_single_point(p1, p2)
                
                # Mutação
                if self.mutation_method == 'swap':
                    c1 = self._mutation_swap(c1)
                    c2 = self._mutation_swap(c2)
                else: 
                    c1 = self._mutation_bit_flip(c1)
                    c2 = self._mutation_bit_flip(c2)
                
                new_population.extend([c1, c2])
            
            self.population = new_population[:self.pop_size]
            
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            'best_solution': self.best_solution,
            'best_fitness': self.best_fitness,
            'history': self.history,
            'execution_time': execution_time
        }
