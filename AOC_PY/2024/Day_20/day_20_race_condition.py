import heapq

def load_graph_from_file(file_path):
    """Load the graph from a text file and represent it as a dictionary."""
    with open(file_path, 'r') as file:
        return {(x, y): c for y, line in enumerate(file.read().splitlines()) for x, c in enumerate(line)}

def bfs(rt, start):
    """Find the shortest path using BFS."""
    queue = [(start, 0)]
    visited = set()
    dist = {start: 0}
    
    while queue:
        pos, d = heapq.heappop(queue)
        if pos in visited:
            continue
        visited.add(pos)
        
        x, y = pos
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nxy = (x + dx, y + dy)
            if rt.get(nxy, '#') != '#' and nxy not in visited:
                new_dist = d + 1
                if nxy not in dist or new_dist < dist[nxy]:
                    dist[nxy] = new_dist
                    heapq.heappush(queue, (nxy, new_dist))
    
    return dist

def find_cheats(rt):
    """Find cheats and calculate the results."""
    # Locate the start and end positions
    start = next(pos for pos, c in rt.items() if c == 'S')
    end = next(pos for pos, c in rt.items() if c == 'E')

    # Traverse the optimal path using BFS
    dist_from_start = bfs(rt, start)
    
    # Extract the path
    path = [end]
    while path[-1] != start:
        x, y = path[-1]
        min_dist = float('inf')
        next_pos = None
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nxy = (x + dx, y + dy)
            if dist_from_start.get(nxy, float('inf')) < min_dist and rt.get(nxy, '#') != '#' and nxy not in path:
                next_pos = nxy
                min_dist = dist_from_start[nxy]
        if next_pos is None:
            break
        path.append(next_pos)
    path.reverse()

    # Convert the path to a dictionary with distances
    path_dict = {loc: dist for dist, loc in enumerate(path)}

    # Find cheats
    p1 = 0  # Cheats saving exactly 2 picoseconds
    p2 = 0  # Total cheats saving at least 100 picoseconds

    for sx, sy in path_dict:
        for dx in range(-20, 21):
            for dy in range(-20, 21):
                cheat = abs(dx) + abs(dy)
                if cheat < 2 or cheat > 20:
                    continue
                nxy = (sx + dx, sy + dy)
                if nxy in path_dict:
                    time_saved = path_dict[nxy] - path_dict[sx, sy] - cheat
                    if time_saved >= 100:
                        p2 += 1
                        if cheat == 2:
                            p1 += 1

    print(f"Cheats saving exactly 2 picoseconds: {p1}")
    print(f"Total cheats saving at least 100 picoseconds: {p2}")
    
    return p1, p2

if __name__ == "__main__":
    file_path = "input.txt"  # Replace with your input file
    rt = load_graph_from_file(file_path)
    find_cheats(rt)
