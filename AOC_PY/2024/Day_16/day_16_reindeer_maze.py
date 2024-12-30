import numpy as np
import heapq
from collections import deque

# Directions: N, E, S, W
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
TURN_COST = 1000  # Cost for turning left or right
PATH_MARKER = 'O'  # Marker for paths in the maze

def load_maze(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
    return np.array([list(row) for row in lines])

def physarum(grid, start, end):
    height, width = grid.shape
    costs = {}
    pq = [(0, (start, 1))]  # Start facing East (1)
    costs[(start, 1)] = 0

    while pq:
        cost, (pos, d) = heapq.heappop(pq)
        x, y = pos

        # Skip states already processed with a lower cost
        if costs.get((pos, d), float('inf')) < cost:
            continue

        # Move forward
        dx, dy = DIRECTIONS[d]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < height and 0 <= new_y < width and grid[new_x, new_y] != '#':
            next_state = ((new_x, new_y), d)
            new_cost = cost + 1
            if new_cost < costs.get(next_state, float('inf')):
                costs[next_state] = new_cost
                heapq.heappush(pq, (new_cost, next_state))

        # Turn left and right
        for nd in [(d - 1) % 4, (d + 1) % 4]:
            next_state = (pos, nd)
            new_cost = cost + TURN_COST
            if new_cost < costs.get(next_state, float('inf')):
                costs[next_state] = new_cost
                heapq.heappush(pq, (new_cost, next_state))

    # Find the minimum cost to reach the end in any direction
    return min(costs.get((end, d), float('inf')) for d in range(4)), costs

def outposts_observed(grid, start, end, costs):
    min_end_cost, costs = physarum(grid, start, end)

    q = deque()
    visited_tiles = set()

    # Add all end states with minimum cost
    for d in range(4):
        state = (end, d)
        if costs.get(state, float('inf')) == min_end_cost:
            q.append(state)
            visited_tiles.add(end)

    height, width = grid.shape

    # Backtrack to find all tiles in shortest paths
    while q:
        (x, y), d = q.popleft()
        current_cost = costs[((x, y), d)]

        # Backtrack for forward moves
        dx, dy = DIRECTIONS[d]
        prev_x, prev_y = x - dx, y - dy
        if 0 <= prev_x < height and 0 <= prev_y < width and grid[prev_x, prev_y] != '#':
            prev_state = ((prev_x, prev_y), d)
            if costs.get(prev_state) == current_cost - 1:
                q.append(prev_state)
                visited_tiles.add((prev_x, prev_y))

        # Backtrack for turns
        turn_cost = current_cost - TURN_COST
        for nd in [(d - 1) % 4, (d + 1) % 4]:
            prev_state = ((x, y), nd)
            if costs.get(prev_state) == turn_cost:
                q.append(prev_state)
                visited_tiles.add((x, y))

    return visited_tiles

def print_maze_with_paths(grid, visited_tiles):
    display_grid = np.array(grid, dtype=str)
    for x, y in visited_tiles:
        if display_grid[x, y] not in ['S', 'E']:
            display_grid[x, y] = PATH_MARKER

    for row in display_grid:
        print("".join(row))

# Main execution
file_path = 'day_16_input.txt'  # Replace with your file path
grid = load_maze(file_path)
start = tuple(np.argwhere(grid == 'S')[0])
end = tuple(np.argwhere(grid == 'E')[0])

min_score, costs = physarum(grid, start, end)
print("Part 1: Lowest possible score is", min_score)
visited_tiles = outposts_observed(grid, start, end, costs)
print("Part 2: Number of tiles on the cheapest path:", len(visited_tiles))
# print_maze_with_paths(grid, visited_tiles)
