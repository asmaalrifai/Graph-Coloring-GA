def load_dimacs_graph(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    edges = []
    num_nodes = 0

    for idx, line in enumerate(lines):
        parts = line.strip().split()
        if idx == 0:
            # First line: assume it's either just a number or a comment
            try:
                num_nodes = int(parts[0])
            except ValueError:
                raise ValueError(f"Invalid format in first line: expected number, got '{parts[0]}'")
        elif len(parts) == 2:
            try:
                u, v = map(int, parts)
                edges.append((u, v))
            except ValueError:
                continue  # skip lines that aren't valid edges

    return num_nodes, edges

