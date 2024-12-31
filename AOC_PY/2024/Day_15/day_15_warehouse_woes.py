from collections import deque
import os

# Constants
GPS_MULTIPLIER = 100
BPT = 2  # BOX_POSITION_OFFSET

# Symbols
robot = '@'
box = 'O'
wall = '#'
open_space = '.'

class Vec:
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def __add__(self, other):
        return Vec(self.r + other.r, self.c + other.c)

    def __eq__(self, other):
        return (self.r, self.c) == (other.r, other.c)

    def __hash__(self):
        return hash((self.r, self.c))

# Movement directions
movemap = {
    '^': Vec(-1, 0),  # Up
    'v': Vec(1, 0),   # Down
    '<': Vec(0, -1),  # Left
    '>': Vec(0, 1)    # Right
}

def get_direction_vector(instruction):
    return movemap.get(instruction)

def grid_to_dict(grid):
    """Convert a 2D grid to a dictionary for faster lookups."""
    grid_dict = {}
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            grid_dict[(r, c)] = cell
    return grid_dict

def load_game_data(filename):
    """Load the map and instructions from a file."""
    with open(filename, 'r') as f:
        lines = f.read().splitlines()

    blank_line_index = lines.index("")
    grid_data = lines[:blank_line_index]
    moves_data = "".join(lines[blank_line_index + 1:])

    return grid_data, moves_data

def is_valid_position(grid_dict, x, y):
    """Check if a position is within bounds and not a wall."""
    return grid_dict.get((x, y)) != wall

def can_push_boxes_chain(grid_dict, x, y, dx, dy):
    """Check if a chain of boxes can be pushed."""
    while (x, y) in grid_dict and grid_dict[(x, y)] != wall:
        if grid_dict.get((x, y)) == open_space:
            return True
        if grid_dict.get((x, y)) != box:
            return False
        x += dx
        y += dy
    return False

def push_boxes_chain(grid_dict, x, y, dx, dy):
    """Push a chain of boxes in the given direction."""
    boxes = []
    while grid_dict.get((x, y)) == box:
        boxes.append((x, y))
        x += dx
        y += dy

    for bx, by in reversed(boxes):
        grid_dict[(bx + dx, by + dy)] = box
        grid_dict[(bx, by)] = open_space

def move_robot(grid_dict, robot_x, robot_y, instruction):
    """Attempt to move the robot based on the given instruction."""
    offset = movemap.get(instruction)
    if offset is not None:
        dx, dy = offset.r, offset.c
        new_x, new_y = robot_x + dx, robot_y + dy

        if is_valid_position(grid_dict, new_x, new_y):
            if grid_dict.get((new_x, new_y)) == box:
                if can_push_boxes_chain(grid_dict, new_x, new_y, dx, dy):
                    push_boxes_chain(grid_dict, new_x, new_y, dx, dy)
                    grid_dict[(new_x, new_y)] = robot
                    grid_dict[(robot_x, robot_y)] = open_space
                    robot_x, robot_y = new_x, new_y
            elif grid_dict.get((new_x, new_y)) == open_space:
                grid_dict[(new_x, new_y)] = robot
                grid_dict[(robot_x, robot_y)] = open_space
                robot_x, robot_y = new_x, new_y

    return robot_x, robot_y

def execute_instructions(grid_dict, robot_x, robot_y, moves_data):
    """Execute instructions and update the grid."""
    for instr in moves_data:
        robot_x, robot_y = move_robot(grid_dict, robot_x, robot_y, instr)
    return grid_dict, robot_x, robot_y

def calculate_gps_sum(grid_dict):
    """Calculate the sum of all boxes' GPS coordinates."""
    gps_sum = 0
    for (x, y), cell in grid_dict.items():
        if cell == box:
            gps_sum += GPS_MULTIPLIER * x + y
    return gps_sum

def process_final_movements(walls, box_pieces, start, moves_data):
    """Process final movements to calculate a separate output."""
    p = start
    for m in moves_data.strip():
        if m not in movemap:
            continue

        delta = movemap[m]
        newp = p + delta
        if newp in walls:
            continue

        if newp not in box_pieces:
            p = newp
            continue

        box = box_pieces[newp]
        tomove = find_boxes_to_move(box, delta, walls, box_pieces)
        if tomove is None:
            continue

        for box in tomove:
            a, b = box
            del box_pieces[a]
            del box_pieces[b]

        for box in tomove:
            a, b = box
            aa, bb = a + delta, b + delta
            box_pieces[aa] = (aa, bb)
            box_pieces[bb] = (aa, bb)

        p = newp

    ans2 = sum(100 * box[0].r + box[0].c for box in box_pieces.values()) // 2
    return ans2

def initialize_game_elements(grid_data):
    """Initialize walls, box pieces, and the robot's start position."""
    walls = set()
    box_pieces = {}
    start = None

    for r, row in enumerate(grid_data):
        for c, cell in enumerate(row):
            if cell == '@':
                start = Vec(r, BPT * c)
            elif cell == '#':
                walls.add(Vec(r, BPT * c))
                walls.add(Vec(r, BPT * c + 1))
            elif cell == 'O':
                a, b = Vec(r, BPT * c), Vec(r, BPT * c + 1)
                box_pieces[a] = (a, b)
                box_pieces[b] = (a, b)

    return walls, box_pieces, start

def find_boxes_to_move(box, delta, walls, box_pieces):
    """Find all boxes affected by movement."""
    q = deque([box])
    seen = set()

    while q:
        box = q.popleft()
        if box in seen:
            continue

        seen.add(box)
        if (box[0] + delta) in walls or (box[1] + delta) in walls:
            return None

        # Find adjacent boxes in the given direction
        a, b = box
        adj_box_a = box_pieces.get(a + delta)
        adj_box_b = box_pieces.get(b + delta)
        if adj_box_a:
            q.append(adj_box_a)
        if adj_box_b:
            q.append(adj_box_b)

    return seen

# Example integration
if __name__ == "__main__":
    filename = "day_15_input.txt"
    grid_data, moves_data = load_game_data(filename)

    map_ = grid_to_dict([list(line) for line in grid_data])
    robot_position = next((pos for pos, value in map_.items() if value == robot), None)
    if robot_position is None:
        raise ValueError("Robot not found in the map!")
    robot_x, robot_y = robot_position

    walls, box_pieces, start = initialize_game_elements(grid_data)

    # Execute instructions
    map_, robot_x, robot_y = execute_instructions(map_, robot_x, robot_y, moves_data)

    # Display final map
    print("Final Map:")
    for r in range(max(pos[0] for pos in map_.keys()) + 1):
        row = ''.join(map_.get((r, c), open_space) for c in range(max(pos[1] for pos in map_.keys()) + 1))
        print(row)

    # Calculate GPS sum
    gps_sum = calculate_gps_sum(map_)
    print(f"Sum of all boxes' GPS coordinates P1: {gps_sum}")

    # Process final movements
    final_answer = process_final_movements(walls, box_pieces, start, moves_data)
    print(f"Sum of all boxes' GPS coordinates P2: {final_answer}")

   

