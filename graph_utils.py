def load_dimacs_graph(file_path):
    # Open the input file and read all lines
    with open(file_path, "r") as f:
        lines = f.readlines()

    edges = []
    num_nodes = 0

    for idx, line in enumerate(lines):
        parts = line.strip().split()

        # Skip empty lines or comment lines (starting with 'c')
        if not parts or parts[0].startswith("c"):
            continue

        # First line contains the number of nodes
        if idx == 0:
            try:
                num_nodes = int(parts[0])
            except ValueError:
                raise ValueError(f"Invalid format in first line: '{line}'")

        # All other lines represent edges as pairs of integers
        elif len(parts) == 2:
            try:
                u, v = map(int, parts)
                edges.append((u, v))
            except ValueError:
                continue  # Skip invalid edge lines

    return num_nodes, edges
