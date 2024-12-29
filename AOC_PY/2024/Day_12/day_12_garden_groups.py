from typing import List, Set

def load_flower_beds(filename: str) -> List[List[str]]:
    with open(filename, 'r') as file:
        grid = [list(line.strip()) for line in file.readlines()]
    return grid

def in_bounds(x: int, y: int, grid: List[List[str]]) -> bool:
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def check(region: Set[tuple[int, int]], i: int, j: int) -> bool:
    return (i, j) in region

def flood_fill(grid: List[List[str]], i: int, j: int, target: str, visited: List[List[bool]]) -> Set[tuple[int, int]]:
    """Flood fill function for finding all cells in a grid of the same flower type as the cell at position (i, j)."""
    stack = [(i, j)]
    region: Set[tuple[int, int]] = set()

    while stack:
        x, y = stack.pop()

        if visited[x][y]:
            continue

        visited[x][y] = True
        region.add((x, y))

        # Check neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny, grid) and not visited[nx][ny] and grid[nx][ny] == target:
                stack.append((nx, ny))

    return region

def calculate_total_price(grid: List[List[str]], method: str) -> int:
    if method not in ['corners', 'ides']:
        raise ValueError("Method must be either 'corners' or 'ides'")

    visited: List[List[bool]] = [[False] * len(grid[0]) for _ in range(len(grid))]
    regions: List[Set[tuple[int, int]]] = []

    # Identify regions by performing flood-fill for each unvisited cell
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not visited[i][j]:
                region = flood_fill(grid, i, j, grid[i][j], visited)
                regions.append(region)

    # Calculate total price based on the method specified
    total = 0
    for region in regions:
        nregion: int = len(region)

        if method == 'corners':
            corners = 0
            for i, j in region:
                west = check(region, i - 1, j)
                east = check(region, i + 1, j)
                north = check(region, i, j - 1)
                south = check(region, i, j + 1)

                not_ns = (not north) + (not south)

                # Count corners
                corners += (not west and not_ns) + (not east and not_ns)

                if north:
                    corners += (west and not check(region, i - 1, j - 1))
                    corners += (east and not check(region, i + 1, j - 1))
                if south:
                    corners += (west and not check(region, i - 1, j + 1))
                    corners += (east and not check(region, i + 1, j + 1))

            total += (nregion * corners)

        elif method == 'ides':
            sides = 0
            for i, j in region:
                sides += sum(
                    not in_bounds(i + di, j + dj, grid) or (i + di, j + dj) not in region
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                )
            total += nregion * sides

    return total

filename = 'day_12_input.txt'
grid = load_flower_beds(filename)

print(f"Total price without discount: {calculate_total_price(grid, method='ides')}")
print(f"Total price with discount: {calculate_total_price(grid, method='corners')}")

