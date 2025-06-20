import random
import networkx as nx
from visualization import save_coloring_frame
from generate_gif import generate_gif


class GeneticAlgorithm:
    def __init__(
        self,
        num_nodes,
        edges,
        pop_size=300,
        mutation_rate=0.03,
        max_gen=1500,
        tournament_k=9,
        selection_type="Tournament",
        crossover_type="Color Aware",
        mutation_mode="Adaptive",
        log_fn=print,
    ):
        # Initialization of GA parameters and problem structure
        self.num_nodes = num_nodes
        self.edges = edges
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.max_gen = max_gen
        self.no_improve_count = 0
        self.best_fitness = float("inf")
        self.tournament_k = tournament_k
        self.selection_type = selection_type
        self.crossover_type = crossover_type
        self.mutation_mode = mutation_mode
        self.log = log_fn

    def initial_population(self):
        # Create initial random population of colorings
        return [
            [random.randint(0, self.num_nodes - 1) for _ in range(self.num_nodes)]
            for _ in range(self.pop_size)
        ]

    def fitness(self, coloring):
        # Calculate fitness as a combination of edge conflicts and color count
        conflicts = sum(1 for u, v in self.edges if coloring[u] == coloring[v])
        used_colors = len(set(coloring))
        return conflicts * 100 + used_colors

    def selection(self, population):
        # Select parents using either Tournament or Roulette selection
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
        # Perform crossover based on selected strategy
        if self.crossover_type == "Single Point":
            point = random.randint(0, self.num_nodes - 1)
            return p1[:point] + p2[point:]
        elif self.crossover_type == "Uniform":
            return [random.choice([a, b]) for a, b in zip(p1, p2)]
        elif self.crossover_type == "Color Aware":
            return self.color_aware_crossover(p1, p2)

    def mutate(self, coloring):
        # Mutate the coloring by changing a node's color (avoiding neighbors' colors)
        for i in range(self.num_nodes):
            if random.random() < self.mutation_rate:
                neighbor_colors = {coloring[v] for u, v in self.edges if u == i} | {
                    coloring[u] for u, v in self.edges if v == i
                }
                new_color = random.randint(0, self.num_nodes - 1)
                while new_color in neighbor_colors:
                    new_color = random.randint(0, self.num_nodes - 1)
                coloring[i] = new_color
        return coloring

    def local_search(self, coloring):
        # Simple repair mechanism: adjust colors to fix direct conflicts
        for u, v in self.edges:
            if coloring[u] == coloring[v]:
                coloring[v] = (coloring[v] + 1) % self.num_nodes
        return coloring

    def adapt_mutation(self, current_best):
        # Adapt mutation rate based on improvement history
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
        # Main evolutionary loop of the Genetic Algorithm
        population = self.initial_population()
        best_overall = None
        best_color_count = float("inf")

        # Precompute layout for consistent visualization
        G = nx.Graph()
        G.add_nodes_from(range(self.num_nodes))
        G.add_edges_from(self.edges)
        pos = nx.spring_layout(G, seed=42)

        for gen in range(self.max_gen):
            # Evaluate and sort population
            population = sorted(population, key=self.fitness)
            best = population[0]
            best_fit = self.fitness(best)
            used_colors = len(set(best))

            # Save best coloring found
            if used_colors < best_color_count:
                best_overall = best[:]
                best_color_count = used_colors

            # Save frame for visualization
            save_coloring_frame(
                self.num_nodes, self.edges, best, gen + 1, folder="frames", pos=pos
            )

            # Log current status
            self.log(
                f"Gen {gen+1}: Best fitness = {best_fit}, used colors = {used_colors}"
            )

            # Adapt mutation rate if needed
            self.adapt_mutation(best_fit)

            # Stop if perfect solution is found
            if best_fit == 0:
                self.log(f"Perfect solution found at generation {gen+1}")
                return best

            # Early stop if no progress and solution is acceptable
            if gen > 50 and used_colors <= 160 and self.no_improve_count > 20:
                self.log("Early stop: Good enough solution")
                break

            # Elitism + Diversity preservation
            elite_count = 10
            diverse_count = 5
            elites = population[:elite_count]
            diverse = random.sample(
                population[elite_count:],
                min(diverse_count, len(population) - elite_count),
            )

            # Generate new population
            new_population = elites + diverse
            while len(new_population) < self.pop_size:
                p1, p2 = self.selection(population)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                child = self.local_search(child)
                new_population.append(child)

            population = new_population

        return best_overall

    def generate_gif_from_frames(self, duration=300):
        # Generate animated GIF from saved frames
        try:
            generate_gif("frames", "animation.gif", duration=duration)
            self.log("GIF animation generated: animation.gif")
        except Exception as e:
            self.log(f"GIF generation failed: {e}")

    def color_aware_crossover(self, p1, p2):
        # Choose genes from the parent with fewer local conflicts
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
            child.append(c1 if conflicts_c1 < conflicts_c2 else c2)
        return child

    def simulated_annealing(
        self, coloring, initial_temp=500.0, cooling_rate=0.90, max_iter=2000
    ):
        # Refine coloring using Simulated Annealing to reduce colors post-GA
        def cost(c):
            return self.fitness(c) * 1000 + len(set(c))

        current = coloring[:]
        current_cost = cost(current)
        original_colors = len(set(current))
        temperature = initial_temp

        for _ in range(max_iter):
            if temperature < 1e-3:
                break

            # Create a neighbor by random color change
            neighbor = current[:]
            i = random.randint(0, self.num_nodes - 1)
            neighbor[i] = random.randint(0, self.num_nodes - 1)
            neighbor = self.local_search(neighbor)

            neighbor_cost = cost(neighbor)
            delta = neighbor_cost - current_cost

            # Accept new solution probabilistically
            if delta < 0 or random.random() < pow(2.71828, -delta / temperature):
                current = neighbor
                current_cost = neighbor_cost

            temperature *= cooling_rate

        improved_colors = len(set(current))
        self.log(
            f"\nSimulated Annealing Result:\n"
            f"    Original Colors: {original_colors}\n"
            f"    Improved Colors: {improved_colors}\n"
            f"    Improvement: {original_colors - improved_colors} fewer colors"
        )
        return current
