def parse_file_with_classification(file_path):
    """
    Parses the file and classifies each grid as either a lock or a key based on its structure.
    """
    with open(file_path, 'r') as f:
        lines = f.read().strip().split("\n")

    locks = []
    keys = []
    current_grid = []

    for line in lines:
        if not line.strip():  # Blank line indicates the end of a grid
            if current_grid:
                # Classify the grid as a lock or a key
                if current_grid[0] == "#####":  # Lock starts with a filled row
                    locks.append(current_grid)
                elif current_grid[-1] == "#####":  # Key ends with a filled row
                    keys.append(current_grid)
                current_grid = []
        else:
            current_grid.append(line)

    # Add the last grid (if any)
    if current_grid:
        if current_grid[0] == "#####":
            locks.append(current_grid)
        elif current_grid[-1] == "#####":
            keys.append(current_grid)

    return locks, keys

def parse_grid(schematic):
    """
    Converts a schematic into a 2D grid representation.
    '#' represents solid (filled), '.' represents empty.
    """
    return [list(row) for row in schematic]

def grids_fit(lock_grid, key_grid):
    """
    Checks if a key grid fits a lock grid without any overlaps.
    """
    for row_lock, row_key in zip(lock_grid, key_grid):
        for cell_lock, cell_key in zip(row_lock, row_key):
            # Overlap occurs if both the lock and key cell are '#'
            if cell_lock == '#' and cell_key == '#':
                return False
    return True

def count_fitting_pairs(locks, keys):
    """
    Counts the number of unique lock/key pairs that fit together.
    """
    fitting_pairs = 0

    for lock_idx, lock in enumerate(locks):
        lock_grid = parse_grid(lock)
        for key_idx, key in enumerate(keys):
            key_grid = parse_grid(key)
            if grids_fit(lock_grid, key_grid):
                fitting_pairs += 1

    return fitting_pairs

# Example usage
file_path = "day_25_input.txt"  # Replace with your file path
locks, keys = parse_file_with_classification(file_path)

# print("Parsed Locks:")
# for i, lock in enumerate(locks):
#     print(f"Lock {i}:\n" + "\n".join(lock))

# print("\nParsed Keys:")
# for i, key in enumerate(keys):
#     print(f"Key {i}:\n" + "\n".join(key))

# Count the number of fitting pairs
result = count_fitting_pairs(locks, keys)
print("Number of fitting pairs:", result)
