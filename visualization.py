def save_coloring_image(num_nodes, edges, coloring, output_path, pos=None):
    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    G.add_edges_from(edges)
    color_map = [coloring[node] for node in G.nodes]

    if pos is None:
        pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 8))
    nx.draw(
        G,
        pos,
        node_color=color_map,
        with_labels=False,
        node_size=100,
        cmap=plt.cm.tab20,
    )
    plt.title("Graph Coloring")
    plt.savefig(output_path)
    plt.close()

    return pos  # Return pos if used as initial layout


def save_coloring_frame(num_nodes, edges, coloring, gen_number, folder, pos):
    import matplotlib.pyplot as plt
    import networkx as nx
    import os

    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    G.add_edges_from(edges)
    color_map = [coloring[node] for node in G.nodes]

    plt.figure(figsize=(10, 8))
    nx.draw(
        G,
        pos,
        node_color=color_map,
        with_labels=False,
        node_size=100,
        cmap=plt.cm.tab20,
    )
    plt.title(f"Generation {gen_number}")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"frame_{gen_number:03d}.png")
    plt.savefig(path)
    plt.close()
