import tracemalloc

def split_stone(number):
    """Split a stone into two stones based on its digits."""
    digits = str(number)
    mid = len(digits) // 2
    left = int(digits[:mid]) if digits[:mid] else 0
    right = int(digits[mid:]) if digits[mid:] else 0
    return [left, right]

def transform_stone(number):
    """Transform a single stone based on the rules."""
    if number == 0:
        return [1]
    elif len(str(number)) % 2 == 0:
        return split_stone(number)
    else:
        return [number * 2024]

def process_stones(stones, blinks, memo):
    """Process a list of stones recursively with memoization."""
    if not stones or blinks <= 0:
        return len(stones)  # Base case: no more splits

    key = (tuple(stones), blinks)
    if key in memo:
        return memo[key]

    total_stones = 0
    for stone in stones:
        new_stones = transform_stone(stone)
        total_stones += process_stones(new_stones, blinks - 1, memo)

    memo[key] = total_stones
    return total_stones

def main():
    # Example input
    initial_stones = [125, 17]
    
    # Initialize tracemalloc to track memory usage
    tracemalloc.start()
    
    total_stone_count_1 = 0
    total_stone_count_2 = 0

    memo = {}
    
    for stone in initial_stones:

        total_stone_count_1 += process_stones([stone], 25, memo)  # Each stone is processed with 6 blinks
        total_stone_count_2 += process_stones([stone], 75, memo)  # Each stone is processed with 6 blinks
        

        # Get the current and peak memory usage
        current, peak = tracemalloc.get_traced_memory()
        print(f"Finished processing stone {stone}. Current Memory: {current / 1024 ** 2:.2f} MB, Peak Memory: {peak / 1024 ** 2:.2f} MB")
    
    # Output the results
    print(f"After processing all stones with 25 blinks, there are {total_stone_count_1} stones.")
    print(f"After processing all stones with 75 blinks, there are {total_stone_count_2} stones.")

if __name__ == "__main__":
    main()