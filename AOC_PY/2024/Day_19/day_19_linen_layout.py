def count_ways_to_construct(design, towel_patterns):
    # Sort towel patterns by length in descending order to prioritize longer matches
    sorted_patterns = sorted(towel_patterns, key=len, reverse=True)
    
    # Create a DP array where dp[i] is the number of ways to construct the first i characters of the design
    dp = [0] * (len(design) + 1)
    dp[0] = 1  # Base case: One way to construct an empty design (do nothing)

    # Iterate through each position in the design
    for i in range(1, len(design) + 1):
        # Check each towel pattern
        for pattern in sorted_patterns:
            # If the pattern matches the end of the current substring, add the ways from the previous state
            if i >= len(pattern) and design[i - len(pattern):i] == pattern:
                dp[i] += dp[i - len(pattern)]

    # The last element of dp gives the total number of ways to construct the full design
    return dp[len(design)]


def process_designs_with_all_options(file_path):
    # Read the input from the specified file
    with open(file_path, 'r') as file:
        input_text = file.read()
    
    # Split the input into two parts: towel patterns and designs
    parts = input_text.strip().split("\n\n")
    if len(parts) != 2:
        raise ValueError("Input file should contain two sections separated by a blank line.")
    
    # Parse towel patterns and designs
    towel_patterns = [pattern.strip() for pattern in parts[0].replace(',', ' ').split()]
    designs = parts[1].strip().splitlines()

    possible_designs = 0  # Counter for designs that can be constructed
    total_ways = 0       # Counter for the total number of arrangements across all designs

    # Process each design
    for i, design in enumerate(designs):
        print(f"\nProcessing design {i+1}/{len(designs)}: {design}")
        # Count the number of ways to construct the current design
        ways = count_ways_to_construct(design, towel_patterns)
        if ways > 0:
            # If at least one way exists, increment the possible designs count
            print(f"Design '{design}' can be made in {ways} ways.")
            possible_designs += 1
        else:
            # If no ways exist, indicate that the design is not possible
            print(f"Design '{design}' is NOT possible.")
        # Add the number of ways for this design to the total
        total_ways += ways

    # Return the results: number of possible designs and total arrangements
    return possible_designs, total_ways

# Example usage
file_path = 'day_19_input.txt'  # Replace with the path to your input file
possible_designs, total_ways = process_designs_with_all_options(file_path)

# Print the final results
print(f"\nNumber of possible designs: {possible_designs}")
print(f"Total number of ways to arrange designs: {total_ways}")
