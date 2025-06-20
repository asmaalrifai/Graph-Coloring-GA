import os
import random
from graph_utils import load_dimacs_graph
from ga import GeneticAlgorithm
from visualization import save_coloring_image
from generate_gif import generate_gif

random.seed()  # For reproducibility, use random.seed(42) if needed

target_files = ["gc_70_9", "gc_100_9", "gc_250_9", "gc_500_9"]

best_results = {}

for file_name in target_files:
    if not os.path.exists(file_name):
        print(f"⚠ File not found: {file_name}")
        continue

    print(f"\n🔍 Processing: {file_name}")
    num_nodes, edges = load_dimacs_graph(file_name)

    best_coloring = None
    best_color_count = float("inf")

    for run in range(5):  # Run 5 times per file
        print(f" ▶ Run {run + 1}")
        ga = GeneticAlgorithm(
            num_nodes=num_nodes,
            edges=edges,
            pop_size=150,
            mutation_rate=0.05,
            max_gen=2000,
            tournament_k=7,
            crossover_type="Color Aware",
            mutation_mode="Adaptive",
        )

        coloring = ga.run()
        coloring = ga.simulated_annealing(coloring)  # Apply SA to refine solution
        color_count = len(set(coloring))
        print(f"    ➤ Used colors after SA: {color_count}")

        if color_count < best_color_count:
            best_color_count = color_count
            best_coloring = coloring

    best_results[file_name] = best_color_count
    print(f"✅ Best for {file_name}: {best_color_count} colors")

    # Save image of best result
    output_image = f"best_pic_{file_name}.png"
    save_coloring_image(num_nodes, edges, best_coloring, output_image)

# Optional: Generate animation GIF from last run
generate_gif("frames", "animation.gif", duration=300)

# Summary
print("\n📊 FINAL BEST RESULTS:")
for file_name, color_count in best_results.items():
    print(f"   {file_name}: {color_count} colors")
