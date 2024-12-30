import numpy as np
from collections import Counter
from collections import defaultdict
from tqdm import tqdm

# Read initial secrets from a text file
def read_initial_secrets(file_path):
    with open(file_path, 'r') as file:
        return [int(line.strip()) for line in file if line.strip().isdigit()]

# Generate the next secret (aligned with `step` function)
def generate_next_secret(n):
    key = 16777216
    n = ((n * 64) ^ n) % key
    n = ((n // 32) ^ n) % key
    n = ((n * 2048) ^ n) % key
    return n

def process_line(n, sequence_length=4):
    window = 0
    ans1 = 0
    seen_now = set()
    sequence_dict = Counter()

    # Initialize the first window
    for _ in range(sequence_length):
        n_next = generate_next_secret(n)
        window = window * 20 + (n_next % 10) - (n % 10)
        n = n_next

    # Process the sliding window
    for i in range(1997):  # Iterate over the sequence
        if i == 1996:  # Special condition for part 1
            ans1 += n

        if window not in seen_now:
            sequence_dict[window] += n % 10
            seen_now.add(window)

        n_next = generate_next_secret(n)
        window = (window * 20 + (n_next % 10) - (n % 10)) % (20 ** sequence_length)
        n = n_next

    return ans1, sequence_dict

def find_best_sequence(file_path):
    initial_secrets = read_initial_secrets(file_path)
    total_ans1 = 0
    global_sequence_dict = defaultdict(int)

    for line in tqdm(initial_secrets, desc="Processing Secrets"):
        ans1, sequence_dict = process_line(line)
        total_ans1 += ans1

        # Merge sequence dictionaries
        for key, value in sequence_dict.items():
            global_sequence_dict[key] += value

    # Find the maximum value in the dictionary (part 2 result)
    max_bananas = max(global_sequence_dict.values())
    return total_ans1, max_bananas

# Entry point
if __name__ == "__main__":
    # Path to the text file containing initial secrets
    file_path = 'day_22_input.txt'

    # Find the results
    part1_result, part2_result = find_best_sequence(file_path)
    print(f"part 1: {part1_result}")
    print(f"part 2: {part2_result}")
