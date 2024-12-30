import os
from collections import deque

def clear_console():
    if os.name == 'nt':  # For Windows systems
        _ = os.system('cls')
    else:  # For Mac and Linux systems
        _ = os.system('clear')

def simulate_falling_bytes(grid_size, filename, initial_max_bytes):
    memory = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    corrupted_coordinates = set()
    min_valid_path = float('inf')
    blocking_byte = None
    bytes_info = []

    with open(filename, 'r') as file:
        rows = [(int(x), int(y)) for x, y in (line.strip().split(',') for line in file)]

    for step, (x, y) in enumerate(rows, start=1):
        if 0 <= y < grid_size and 0 <= x < grid_size:  # Check (y, x) for bounds
            memory[y][x] = '#'
            corrupted_coordinates.add((x, y))
        else:
            print(f"Warning: Ignoring out-of-bounds coordinate ({x},{y})")

        if step % 10 == 0 or step == len(rows):
            clear_console()
            print(f"Processing byte {step}/{initial_max_bytes}...")

        start = (0, 0)
        end = (grid_size - 1, grid_size - 1)
        if not is_corrupted(memory, start[0], start[1]):
            shortest_path = bfs(memory, start, end)
            if shortest_path != float('inf'):
                if step == initial_max_bytes:
                    print(f"Shortest Path Length at {initial_max_bytes} bytes: {shortest_path}")
                    bytes_info.append(f"Shortest Path Length at {initial_max_bytes} bytes: {shortest_path}")
                min_valid_path = min(min_valid_path, shortest_path)
            else:
                if blocking_byte is None:
                    blocking_byte = (x, y)
                    print(f"Blocking byte found at step {step}: {blocking_byte}")

        else:
            bytes_info.append(f"Start position corrupted after {step} bytes.")

    if blocking_byte:
        bytes_info.append(f"First Blocking Byte Coordinates: {blocking_byte[0]},{blocking_byte[1]}")
    else:
        bytes_info.append("No blocking byte found.")

    final_path_info = min_valid_path if min_valid_path != float('inf') else "No valid path found."
    return final_path_info, bytes_info

def bfs(memory, start, end):
    queue = deque([(start, 0)])
    visited = set()
    visited.add(start)
    
    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) == end:
            return steps
        
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(memory) and 0 <= ny < len(memory[0]) and memory[nx][ny] != '#' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))
    
    return float('inf')

def is_corrupted(memory, x, y):
    return memory[x][y] == '#'

# Example usage
grid_size = 7 #71 for actual input
filename = 'day_18_input.txt'
initial_max_bytes = 12 # 1024 for actual input

final_min_path_length, bytes_info = simulate_falling_bytes(grid_size, filename, initial_max_bytes)
print("Final Minimum Valid Path Length:", final_min_path_length)

for info in bytes_info:
    print(info)