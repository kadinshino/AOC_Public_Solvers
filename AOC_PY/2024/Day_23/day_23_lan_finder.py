from itertools import combinations

def parse_and_create_adjacency_list(file_path):
    adjacency_list = {}
    with open(file_path, 'r') as file:
        for line in file:
            a, b = line.strip().split('-')
            adjacency_list.setdefault(a, set()).add(b)
            adjacency_list.setdefault(b, set()).add(a)
    return adjacency_list

def find_triangles(adjacency_list):
    triangles = []
    for a, b_set in adjacency_list.items():
        for b in b_set:
            if b > a:  # Avoid duplicate triangles by ensuring order (a < b)
                for c in b_set.intersection(adjacency_list[b]):
                    if c > b:  # Ensure order (b < c) to avoid duplicates
                        triangles.append((a, b, c))
    return triangles

def filter_triangles(triangles):
    return [triangle for triangle in triangles if any(node.startswith('t') for node in triangle)]

def prune_graph(graph, min_degree=2): #  Prune nodes with degree less than the minimum degree threshold.
    return {node: neighbors for node, neighbors in graph.items() if len(neighbors) >= min_degree}

def bron_kerbosch(graph, R, P, X, cliques):
    """
    Bron–Kerbosch algorithm for finding maximal cliques.
    R: Set of nodes already in the clique
    P: Set of nodes that can still be added to the clique
    X: Set of nodes that cannot be added to the clique
    cliques: List to store maximal cliques
    """
    if not P and not X:
        cliques.append(R)
        return
    
    for node in list(P):
        bron_kerbosch(
            graph,
            R.union({node}),
            P.intersection(graph[node]),
            X.intersection(graph[node]),
            cliques
        )
        P.remove(node)
        X.add(node)

def find_max_clique(graph): # Finds the largest clique in the graph using Bron–Kerbosch.

    cliques = []
    bron_kerbosch(graph, set(), set(graph.keys()), set(), cliques)
    
    # Find the largest clique
    max_clique = max(cliques, key=len, default=set())
    return max_clique

def optimize_and_find_clique(file_path): # Complete workflow: read file, create adjacency list, prune, and find the largest clique.
 
    adjacency_list = parse_and_create_adjacency_list(file_path)  # Parse the connections from the file and create adjacency list.

    # Find all triangles in the graph
    triangles = find_triangles(adjacency_list)
    filtered_triangles = filter_triangles(triangles)

    pruned_graph = prune_graph(adjacency_list, min_degree=2)     # Prune the graph to reduce unnecessary computations.
    max_clique = find_max_clique(pruned_graph)                   # Find the largest clique in the graph.
    sorted_clique = sorted(max_clique)                           # Sort the nodes of the largest clique alphabetically.
    password = ','.join(sorted_clique)                           # Join them with commas to form the password.

    # Return results.
    return len(filtered_triangles), max_clique, password

# Path to the input file.
file_path = 'day_23_input.txt'

# Execute the optimized workflow.
result = optimize_and_find_clique(file_path)

# Print the results.
print(f"Number of filtered triangles: {result[0]}")
print(f"Largest clique: {result[1]}")
print(f"Password: {result[2]}")
