import random
from visualization import save_coloring_frame
from generate_gif import generate_gif


class GeneticAlgorithm:
    def __init__(
        self,
        num_nodes,
        edges,
        pop_size=100,
        mutation_rate=0.1,
        max_gen=1000,
        tournament_k=5,
        selection_type="Tournament",
        crossover_type="Single Point",
        mutation_mode="Adaptive",
        log_fn=print,
    ):
        self.num_nodes = num_nodes
        self.edges = edges
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.max_gen = max_gen
        self.no_improve_count = 0  # For adaptive mutation -> advanced feature
        self.best_fitness = float("inf")
        self.tournament_k = tournament_k
        self.selection_type = selection_type
        self.crossover_type = crossover_type
        self.mutation_mode = mutation_mode
        self.log = log_fn

    def initial_population(self):
        return [
            [random.randint(0, self.num_nodes - 1) for _ in range(self.num_nodes)]
            for _ in range(self.pop_size)
        ]

    def fitness(self, coloring):
        conflicts = sum(1 for u, v in self.edges if coloring[u] == coloring[v])
        used_colors = len(set(coloring))
        return conflicts * 100 + used_colors

    def selection(self, population):
        if self.selection_type == "Tournament":
            selected = []
            for _ in range(2):
                tournament = random.sample(population, self.tournament_k)
                best = min(tournament, key=self.fitness)
                selected.append(best)
            return selected
        elif self.selection_type == "Roulette":
            total = sum(1 / (1 + self.fitness(ind)) for ind in population)
            probs = [(1 / (1 + self.fitness(ind))) / total for ind in population]
            return random.choices(population, weights=probs, k=2)

    def crossover(self, p1, p2):
        if self.crossover_type == "Single Point":
            point = random.randint(0, self.num_nodes - 1)
            return p1[:point] + p2[point:]
        elif self.crossover_type == "Uniform":
            return [random.choice([a, b]) for a, b in zip(p1, p2)]
        elif self.crossover_type == "Color Aware":
            return self.color_aware_crossover(p1, p2)

    def mutate(self, coloring):
        for i in range(self.num_nodes):
            if random.random() < self.mutation_rate:
                colors_used = list(set(coloring))
                coloring[i] = random.choice(colors_used)

        return coloring

    def local_search(self, coloring):
        for u, v in self.edges:
            if coloring[u] == coloring[v]:
                coloring[v] = (coloring[v] + 1) % self.num_nodes
        return coloring

    def adapt_mutation(self, current_best):
        if self.mutation_mode == "Fixed":
            return
        if current_best == self.best_fitness:
            self.no_improve_count += 1
        else:
            self.no_improve_count = 0
            self.best_fitness = current_best

        if self.no_improve_count > 10:
            self.mutation_rate = min(1.0, self.mutation_rate * 1.5)
        else:
            self.mutation_rate = max(0.01, self.mutation_rate * 0.95)

    def run(self):
        population = self.initial_population()

        for gen in range(self.max_gen):
            population = sorted(population, key=self.fitness)
            best = population[0]
            best_fit = self.fitness(best)
            used_colors = len(set(best))
            save_coloring_frame(
                self.num_nodes, self.edges, best, gen + 1, folder="frames"
            )
            self.log(
                f"Gen {gen+1}: Best fitness = {best_fit}, used colors = {used_colors}"
            )

            self.adapt_mutation(best_fit)

            if best_fit == 0:
                self.log(f"✅ Perfect solution found at generation {gen+1}")
                return best

            elite_count = 10
            diverse_count = 5

            elites = population[:elite_count]
            diverse = random.sample(
                population[elite_count:],
                min(diverse_count, len(population) - elite_count),
            )
            new_population = elites + diverse
            while len(new_population) < self.pop_size:
                p1, p2 = self.selection(population)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                child = self.local_search(child)
                new_population.append(child)

            population = new_population

        return population[0]

    def generate_gif_from_frames(self, duration=300):
        try:
            generate_gif("frames", "animation.gif", duration=duration)
            self.log("🌀 GIF animation generated: animation.gif")
        except Exception as e:
            self.log(f"❌ GIF generation failed: {e}")

    def color_aware_crossover(self, p1, p2):
        child = []
        for i in range(self.num_nodes):
            c1 = p1[i]
            c2 = p2[i]

            conflicts_c1 = sum(
                1 for u, v in self.edges if (u == i or v == i) and (p1[u] == p1[v])
            )
            conflicts_c2 = sum(
                1 for u, v in self.edges if (u == i or v == i) and (p2[u] == p2[v])
            )

            if conflicts_c1 < conflicts_c2:
                child.append(c1)
            else:
                child.append(c2)
        return child

    def simulated_annealing(
        self, coloring, initial_temp=100.0, cooling_rate=0.95, max_iter=1000
    ):
        def cost(c):
            return self.fitness(c) * 1000 + len(set(c))

        current = coloring[:]
        current_cost = cost(current)
        original_colors = len(set(current))
        temperature = initial_temp

        for _ in range(max_iter):
            if temperature < 1e-3:
                break

            neighbor = current[:]
            i = random.randint(0, self.num_nodes - 1)
            neighbor[i] = random.randint(0, self.num_nodes - 1)
            neighbor = self.local_search(neighbor)

            neighbor_cost = cost(neighbor)
            delta = neighbor_cost - current_cost

            if delta < 0 or random.random() < pow(2.71828, -delta / temperature):
                current = neighbor
                current_cost = neighbor_cost

            temperature *= cooling_rate

        improved_colors = len(set(current))
        self.log(
            f"\n❄️ Simulated Annealing Result:\n"
            f"   ➤ Original Colors: {original_colors}\n"
            f"   ➤ Improved Colors: {improved_colors}\n"
            f"   ➤ Improvement: {original_colors - improved_colors} fewer colors"
        )
        return current
