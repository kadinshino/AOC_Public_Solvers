from sympy import symbols, Eq, solve
import pandas as pd

def solve_claw_machine(a_x, a_y, b_x, b_y, p_x, p_y):
    # Symbols for number of presses
    x, y = symbols('x y', integer=True, nonnegative=True)
    
    # Equations for x and y
    eq_x = Eq(x * a_x + y * b_x, p_x)
    eq_y = Eq(x * a_y + y * b_y, p_y)
    
    # Solve the system of equations
    solutions = solve((eq_x, eq_y), (x, y), dict=True)
    
    # Find the minimum cost solution
    min_cost = float('inf')
    best_solution = None
    for sol in solutions:
        if sol[x].is_integer and sol[y].is_integer and sol[x] >= 0 and sol[y] >= 0:  # Ensure non-negative integer solutions
            cost = 3 * sol[x] + sol[y]
            if cost < min_cost:
                min_cost = cost
                best_solution = sol
    
    return min_cost, best_solution

def process_machines(file_path, offset=0):
    machines = []
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]  # Skip blank lines
        for i in range(0, len(lines), 3):
            if i + 2 >= len(lines):
                break
            a_line = lines[i]
            b_line = lines[i + 1]
            prize_line = lines[i + 2]

            # Extract numbers from the lines
            try:
                a_x = int(a_line.split('+')[1].split(',')[0])
                a_y = int(a_line.split('+')[2])
                b_x = int(b_line.split('+')[1].split(',')[0])
                b_y = int(b_line.split('+')[2])
                p_x = int(prize_line.split('=')[1].split(',')[0]) + offset
                p_y = int(prize_line.split('=')[2]) + offset
                machines.append((a_x, a_y, b_x, b_y, p_x, p_y))
            except (IndexError, ValueError):
                print(f"Skipping invalid block: {a_line}, {b_line}, {prize_line}")
    
    # Solve for each machine and collect results
    results = []
    for machine in machines:
        a_x, a_y, b_x, b_y, p_x, p_y = machine
        cost, solution = solve_claw_machine(a_x, a_y, b_x, b_y, p_x, p_y)
        results.append((cost, solution))
    
    return results

# Input file path (adjust as needed)
input_file = 'day_13.input.txt'

def main():
    # Process machines without offset for P1
    results_p1 = process_machines(input_file)

    # Convert results to a DataFrame
    df_p1 = pd.DataFrame(results_p1, columns=["Minimum Cost", "Solution (x: A presses, y: B presses)"])

    # Output total results count and total cost of all solutions P1
    print(f"Total machines processed: {len(results_p1)}")
    total_cost_p1 = sum(cost for cost, _ in results_p1 if cost != float('inf'))
    print(f"Total cost of all solutions P1: {total_cost_p1}")

    # Process machines with offset for P2
    offset = 10000000000000
    results_p2 = process_machines(input_file, offset=offset)

    # Convert results to a DataFrame
    df_p2 = pd.DataFrame(results_p2, columns=["Minimum Cost", "Solution (x: A presses, y: B presses)"])

    # Calculate and output the total cost of all solutions P2
    total_cost_p2 = sum(cost for cost, _ in results_p2 if cost != float('inf'))
    print(f"Total cost of all solutions P2: {total_cost_p2}")

if __name__ == "__main__":
    main()
