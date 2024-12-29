from collections import deque

# Function to read grid from a text file
def read_grid_from_file(file_path):
    """Reads the grid from a file and returns it as a list of lists."""
    with open(file_path, 'r') as file:
        grid = [list(line.strip()) for line in file if line.strip()]
    return grid

# Function to find positions of antennas
def find_positions(grid):
    """Finds positions of antennas in the grid and returns them as a dictionary."""
    positions = {}
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell not in ('.', '#'):  # If it's an antenna (not a '.' or '#')
                positions.setdefault(cell, []).append((row_idx, col_idx))
    return positions

# Function to calculate potential antinodes for two antennas
def calculate_antinode_positions_1(a1, a2):
    """Calculates potential antinodes for a pair of antennas."""
    x1, y1 = a1
    x2, y2 = a2
    dx, dy = x2 - x1, y2 - y1
    return [(x1 - dx, y1 - dy), (x2 + dx, y2 + dy)]

# Function to verify if an antinode is valid
def is_valid_antinode(a1, a2, anode):
    """Checks if an antinode position is valid."""
    x1, y1 = a1
    x2, y2 = a2
    xa, ya = anode
    d1 = abs(x1 - xa) + abs(y1 - ya)
    d2 = abs(x2 - xa) + abs(y2 - ya)
    return d1 == 2 * d2 or d2 == 2 * d1

# Function to count unique antinode positions (Method 1)
def count_antinode_positions_1(grid):
    """Counts unique antinode positions based on antenna pairs."""
    positions = find_positions(grid)
    antinodes = set()
    for antennas in positions.values():
        for i in range(len(antennas)):
            for j in range(i + 1, len(antennas)):
                a1, a2 = antennas[i], antennas[j]
                possible_antinodes = calculate_antinode_positions_1(a1, a2)
                for anode in possible_antinodes:
                    x, y = anode
                    if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and is_valid_antinode(a1, a2, anode):
                        antinodes.add(anode)
    return antinodes

# Function to calculate potential antinodes for antennas
def calculate_antinode_positions_2(positions, grid):
    """Calculates all potential antinode positions for all antennas."""
    antinodes = set()
    for antennas in positions.values():
        for i in range(len(antennas)):
            for j in range(i + 1, len(antennas)):
                a1, a2 = antennas[i], antennas[j]
                x1, y1 = a1
                x2, y2 = a2
                dx, dy = x2 - x1, y2 - y1
                for k in range(1, len(grid) + len(grid[0])):
                    antinode1 = (x1 - k * dx, y1 - k * dy)
                    antinode2 = (x2 + k * dx, y2 + k * dy)
                    if 0 <= antinode1[0] < len(grid) and 0 <= antinode1[1] < len(grid[0]):
                        antinodes.add(antinode1)
                    if 0 <= antinode2[0] < len(grid) and 0 <= antinode2[1] < len(grid[0]):
                        antinodes.add(antinode2)
                antinodes.add(a1)
                antinodes.add(a2)
    return antinodes


# Function to count unique antinode positions (Method 2)
def count_antinode_positions_2(grid):
    """Counts unique antinode positions based on all potential positions."""
    positions = find_positions(grid)
    antinodes = calculate_antinode_positions_2(positions, grid)
    return antinodes

# Overlay antinodes on the grid for visualization
def overlay_antinodes(grid, antinodes):
    """Overlays antinodes on the grid for visualization."""
    visual_grid = [row.copy() for row in grid]
    for x, y in antinodes:
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and visual_grid[x][y] == '.':
            visual_grid[x][y] = '#'
    return visual_grid

# Function to print the grid
def print_grid(grid):
    """Prints the grid."""
    for row in grid:
        print(''.join(row))

# Main execution
if __name__ == "__main__":
    file_path = "day_8_input.txt"  # Replace with your actual file path
    grid = read_grid_from_file(file_path)
    
    antinodes_set_1 = count_antinode_positions_1(grid)
    antinodes_set_2 = count_antinode_positions_2(grid)
    visualized_grid = overlay_antinodes(grid, antinodes_set_2)

    print("Overlayed Grid with Antinodes:")
    print_grid(visualized_grid)

    print("Number of unique antinode pos 1:", len(antinodes_set_1))
    print("Number of unique antinode pos 2:", len(antinodes_set_2))
