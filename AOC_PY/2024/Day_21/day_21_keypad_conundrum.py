import itertools
from functools import lru_cache

number = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2),
    "4": (1, 0), "5": (1, 1), "6": (1, 2),
    "1": (2, 0), "2": (2, 1), "3": (2, 2),
              "0": (3, 1), "A": (3, 2)
}

small = {
    "^": (0, 1), 
    "A": (0, 2),
    "<": (1, 0), 
    "v": (1, 1), ">": (1, 2)
}

def simulate(line, py, px, gapy, gapx):
    """Simulates a sequence of moves to check validity."""
    d = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1)
    }
    
    for c in line:
        if c == "A":
            continue
        
        dy, dx = d[c]
        py, px = py + dy, px + dx
        
        if py == gapy and px == gapx:
            return False
    
    return True

@lru_cache(maxsize=None)
def small_step(py, px, ny, nx, depth, max_depth):
    """Calculates the shortest path between two points using directional moves."""
    dy, dx = ny - py, nx - px
    best = float('inf')
    
    for perm in itertools.permutations(range(4)):
        move_sequence = generate_move_sequence(dy, dx, perm)
        if simulate(move_sequence + "A", py, px, *get_gap_position(depth)):
            best = min(best, walk_line(move_sequence + "A", depth + 1, max_depth))
    
    return best

def generate_move_sequence(dy, dx, perm):
    """Generates a move sequence based on the permutation."""
    moves = [
        '>' * abs(dx) if p == 0 and dx > 0 else
        'v' * abs(dy) if p == 1 and dy > 0 else
        '<' * abs(dx) if p == 2 and dx < 0 else
        '^' * abs(dy) if p == 3 and dy < 0 else ''
        for p in perm
    ]
    
    return ''.join(moves)

def get_gap_position(depth):
    """Returns the gap position based on the depth."""
    return (0, 0) if depth >= 0 else (3, 0)

def walk_line(line, depth, max_depth):

    if depth == max_depth:
        return len(line)
    
    table = small if depth >= 0 else number
    start_pos = table["A"]
    current_y, current_x = start_pos
    size = 0
    
    for move in line:
        next_y, next_x = table[move]
        size += small_step(current_y, current_x, next_y, next_x, depth, max_depth)
        current_y, current_x = next_y, next_x
    
    return size

def solve(data, max_depth):
    """Solves the problem for a given dataset and maximum depth."""
    ans = 0
    for line in data:
        n = walk_line(line, -1, max_depth)
        ans += n * int(line[:3])
    return ans

# Read data from file
def read_data_from_file(filename):
    with open(filename, 'r') as file:
        data = [line.strip() for line in file.readlines()]
    return data

data = read_data_from_file('day_21_input.txt')

print(solve(data, 2))
print(solve(data, 25))
