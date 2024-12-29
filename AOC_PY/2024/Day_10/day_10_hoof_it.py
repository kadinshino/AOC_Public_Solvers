from collections import deque

# Function to read map data from a file
def read_map_from_file(file_path):
    with open(file_path, 'r') as file:
        map_data = file.read().strip().split('\n')
    return map_data

# Read the map from the file
map_data = read_map_from_file('day_10_input.txt')

# Convert map into a 2D grid (list of lists)
grid = [list(row) for row in map_data]

# Define directions for moving in 4 directions: up, down, left, right
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Helper function to check if a position is valid (inside grid and not blocked)
def is_valid(x, y, prev_value):
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        cell_value = grid[x][y]
        return cell_value.isdigit() and int(cell_value) == prev_value + 1
    return False

# BFS function to explore from a given starting point and count distinct trails leading to '9'
def bfs(start_x, start_y):
    queue = deque([(start_x, start_y, 0, [])])
    trails = set()
    while queue:
        x, y, current_value, path = queue.popleft()
        if grid[x][y] == '9':
            trails.add(tuple(path + [(x, y)]))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, current_value):
                queue.append((nx, ny, current_value + 1, path + [(x, y)]))
    return len(trails)

# BFS function to explore from a given starting point and count distinct '9's reachable
def bfs_count_nines(start_x, start_y):
    visited = set()
    queue = deque([(start_x, start_y, 0)])
    visited.add((start_x, start_y))
    distinct_trails = 0

    while queue:
        x, y, current_value = queue.popleft()
        if grid[x][y] == '9':
            distinct_trails += 1
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, current_value) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, int(grid[nx][ny])))

    return distinct_trails

# Main function to find all trailheads and their ratings (distinct trails leading to '9')
def find_trail_ratings():
    trailheads = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '0':
                rating = bfs(i, j)
                if rating > 0:
                    trailheads.append((i, j, rating))
    return trailheads

# Main function to find all trailheads and count distinct '9's reachable
def find_distinct_trails():
    trailheads = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '0':
                rating = bfs_count_nines(i, j)
                if rating > 0:
                    trailheads.append((i, j, rating))
    return trailheads

# Run the function and get the trailhead data
trailheads_ratings = find_trail_ratings()
trailheads_distinct_trails = find_distinct_trails()

# Calculate the sum of ratings (distinct trails leading to '9')
sum_of_ratings = sum(trailhead[2] for trailhead in trailheads_ratings)
sum_of_distinct_trails = sum(trailhead[2] for trailhead in trailheads_distinct_trails)

# Output for the first result: print each trailhead with its rating
for trailhead in trailheads_ratings:
    print(f"Trailhead at ({trailhead[0]}, {trailhead[1]}) with a rating of {trailhead[2]}")

# Second output: sum of the ratings of all trailheads
print(f"Sum of the ratings of all trailheads: {sum_of_ratings}")

# Output for the second result: print the distinct trail count
print(f"Total distinct trail counts: {sum_of_distinct_trails}")

