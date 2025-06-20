import os
from graph_utils import load_dimacs_graph
from ga import GeneticAlgorithm
from visualization import save_coloring_image
from generate_gif import generate_gif
# Search for files starting with "gc_"
for file_name in os.listdir():
    if file_name.startswith("gc_"):
        try:
            print(f"🔍 Processing: {file_name}")
            num_nodes, edges = load_dimacs_graph(file_name)

            # ✅ Start Genetic Algorithm with tournament_k = 7
            ga = GeneticAlgorithm(
                num_nodes=num_nodes,
                edges=edges,
                pop_size=100,
                mutation_rate=0.1,
                max_gen=1000,
                tournament_k=7  # 🔥 Turnuva boyutu burada
            )

            coloring = ga.run()

            # Create output image
            output_image = f"pic_{file_name}.png"
            save_coloring_image(num_nodes, edges, coloring, output_image)

            print(f"✅ Done: {file_name} ➜ {output_image} with {len(set(coloring))} colors\n")

        except Exception as e:
            print(f"❌ Error in {file_name}: {e}\n")



generate_gif("frames", "animation.gif", duration=300)
