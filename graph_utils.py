def load_dimacs_graph(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    edges = []
    num_nodes = 0

    for idx, line in enumerate(lines):
        parts = line.strip().split()
        if not parts or parts[0].startswith("c"):  # Skip comment lines
            continue
        if idx == 0:
            try:
                num_nodes = int(parts[0])
            except ValueError:
                raise ValueError(f"Invalid format in first line: '{line}'")
        elif len(parts) == 2:
            try:
                u, v = map(int, parts)
                edges.append((u, v))
            except ValueError:
                continue

    return num_nodes, edges
