import os
import random
from graph_utils import load_dimacs_graph
from ga import GeneticAlgorithm
from visualization import save_coloring_image
from generate_gif import generate_gif

# Set a seed if you want reproducible results
# random.seed(42)

target_files = ["gc_500_9"]

best_results = {}

for file_name in target_files:
    if not os.path.exists(file_name):
        print(f"File not found: {file_name}")
        continue

    print(f"\nProcessing: {file_name}")
    num_nodes, edges = load_dimacs_graph(file_name)

    best_coloring = None
    best_color_count = float("inf")

    for run in range(1):  # Run multiple times to improve chances
        print(f"\nRun {run + 1}")
        ga = GeneticAlgorithm(
            num_nodes=num_nodes,
            edges=edges,
            pop_size=300,
            mutation_rate=0.03,
            max_gen=1500,
            tournament_k=9,
            crossover_type="Color Aware",
            mutation_mode="Adaptive",
        )

        # Run Genetic Algorithm
        coloring = ga.run()

        # Refine with Simulated Annealing
        coloring = ga.simulated_annealing(
            coloring, initial_temp=500.0, cooling_rate=0.90, max_iter=2000
        )

        color_count = len(set(coloring))
        print(f"     Used colors after SA: {color_count}")

        if color_count < best_color_count:
            best_color_count = color_count
            best_coloring = coloring[:]

    best_results[file_name] = best_color_count
    print(f"\nBest result for {file_name}: {best_color_count} colors")

    # Save PNG of best result
    output_image = f"best_pic_{file_name}.png"
    save_coloring_image(num_nodes, edges, best_coloring, output_image)
    print(f" Saved image: {output_image}")

# Generate GIF from last run frames
generate_gif("frames", "animation.gif", duration=300)
print("GIF created: animation.gif")

# Final summary
print("\nFINAL BEST RESULTS:")
for file_name, color_count in best_results.items():
    print(f"   {file_name}: {color_count} colors")
