import matplotlib.pyplot as plt
import networkx as nx
import os

def save_coloring_image(num_nodes, edges, coloring, output_path):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    G.add_edges_from(edges)
    color_map = [coloring[node] for node in G.nodes]
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, node_color=color_map, with_labels=False, node_size=100, cmap=plt.cm.tab20)
    plt.title("Graph Coloring")
    plt.savefig(output_path)
    plt.close()

def save_coloring_frame(num_nodes, edges, coloring, gen_number, folder):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    G.add_edges_from(edges)
    color_map = [coloring[node] for node in G.nodes]
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, node_color=color_map, with_labels=False, node_size=100, cmap=plt.cm.tab20)
    plt.title(f"Generation {gen_number}")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"frame_{gen_number:03d}.png")
    plt.savefig(path)
    plt.close()