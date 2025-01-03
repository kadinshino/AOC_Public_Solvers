from collections import Counter

# Function to determine the quadrant of a robot
def determine_quadrant(robot, center_col, center_row):
    x, y = robot["position"]
    
    # Ensure robots in the blue area are not assigned to any quadrant
    if x == center_col or y == center_row:
        return None
    
    if x < center_col and y < center_row:
        return 1  # Top Left
    elif x >= center_col and y < center_row:
        return 2  # Top Right
    elif x < center_col and y >= center_row:
        return 3  # Bottom Left
    else:
        return 4  # Bottom Right

# Function to assign robots to quadrants
def assign_robots_to_quadrants(robots, center_col, center_row):
    quadrants = {1: [], 2: [], 3: [], 4: []}
    for robot in robots:
        quadrant = determine_quadrant(robot, center_col, center_row)
        if quadrant:  # Ignore robots in the blue area
            quadrants[quadrant].append(robot)
    return quadrants

# Function to calculate the new position of a robot after one cycle
def update_robot(robot, grid_size):
    x, y = robot["position"]
    vx, vy = robot["velocity"]
    
    # Update the position based on velocity
    x = (x + vx) % grid_size[0]
    y = (y + vy) % grid_size[1]
    
    return {"position": [x, y], "velocity": [vx, vy]}

# Function to load robot data from a file
def load_robot_data(file_path):
    robots = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                # Parse position and velocity
                parts = line.split(" ")
                x, y = map(int, parts[0].split("=")[1].split(","))
                vx, vy = map(int, parts[1].split("=")[1].split(","))
                robots.append({"position": [x, y], "velocity": [vx, vy]})
    return robots

# Load robot data from file
robots = load_robot_data("day_14_input.txt")

# Simulation parameters
grid_size = (101, 103)  # Change this to your desired grid size
total_cycles = 10403  # Total number of cycles
final_cycle_checkpoint = 100  # Cycle after which the final distribution is calculated

# Define restricted area (+ cross in the middle of the grid)
center_col = grid_size[0] // 2  # Middle column
center_row = grid_size[1] // 2  # Middle row

# Track minimum safety factor and the corresponding cycle
min_safety_factor = float('inf')
min_cycle = 0  # Initialize to the first cycle
min_quadrant_distribution = None
final_quadrants = None  # To store distribution after 100 cycles
final_safety_factor = None

# Run the simulation
for cycle in range(total_cycles):
    # Update robots for the current cycle
    robots = [update_robot(robot, grid_size) for robot in robots]
    
    # Calculate the final quadrant distribution after 100 cycles
    if cycle == final_cycle_checkpoint - 1:  # Adjust for zero-based index
        final_quadrants = assign_robots_to_quadrants(robots, center_col, center_row)
        final_safety_factor = 1
        for robots_in_quadrant in final_quadrants.values():
            final_safety_factor *= len(robots_in_quadrant)

    # Assign robots to quadrants
    quadrants = assign_robots_to_quadrants(robots, center_col, center_row)
    
    # Calculate the safety factor for this cycle
    safety_factor = 1
    for quadrant, robots_in_quadrant in quadrants.items():
        safety_factor *= len(robots_in_quadrant)
    
    # Check if this is the minimum safety factor observed
    if safety_factor < min_safety_factor:
        min_safety_factor = safety_factor
        min_cycle = cycle + 1  # Correcting off-by-one: first cycle is cycle 1
        min_quadrant_distribution = {
            q: len(robots_in_quadrant) for q, robots_in_quadrant in quadrants.items()
        }

# Output results for final quadrant distribution and safety factor after 100 cycles
print("Final Quadrant Distribution (after 100 cycles):")
for quadrant, robots_in_quadrant in final_quadrants.items():
    print(f"  Quadrant {quadrant}: {len(robots_in_quadrant)} robots")
print(f"Final Safety Factor (after 100 cycles): {final_safety_factor}\n")

# Output results for the densest formation
print(f"Cycle with densest formation: {min_cycle}")
print(f"Lowest Safety Factor: {min_safety_factor}")
print("Quadrant Distribution at Minimum Safety Factor:")
for quadrant, count in min_quadrant_distribution.items():
    print(f"  Quadrant {quadrant}: {count} robots")
