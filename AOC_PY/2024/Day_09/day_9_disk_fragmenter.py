def load_disk_string_from_file(filename):
    try:
        with open(filename, 'r') as file:
            disk_string = file.readline().strip()
        return disk_string
    except Exception as e:
        print(f"[ERROR] Failed to read file {filename}: {e}")
        return ""

################################ Part 1 ################################

def convert_to_dense_with_ids(disk_string):
   """
   Convert the disk string into a dense format with file IDs.
   """
   dense_format = ""
   file_id = 0
   for i in range(0, len(disk_string), 2):
       file_block = int(disk_string[i])
       if i + 1 < len(disk_string):
           free_space = int(disk_string[i + 1])
       else:
           free_space = 0
       dense_format += str(file_id) * file_block + '.' * free_space
       file_id += 1
   # print(f"[DEBUG] Initial Dense Format: {dense_format}")
   return dense_format

def defragment_with_moves(dense_string):
   """
   Defragment the disk one block at a time, moving the last block of any file to the leftmost free space.
   """
   disk = list(dense_string)
   steps = [dense_string]

   while True:
       try:
           last_block_index = len(disk) - 1 - disk[::-1].index(next(c for c in reversed(disk) if c.isdigit()))
           first_free_space = disk.index('.')
       except ValueError:
           break

       if last_block_index < first_free_space:
           break

       disk[first_free_space], disk[last_block_index] = disk[last_block_index], '.'
       steps.append("".join(disk))

   # print(f"[DEBUG] Defragmentation Steps:")
   for step in steps:
       print(f"    {step}")
   return steps[-1]

def calculate_checksum(data):
    """
    Calculate checksum for a defragmented memory or string.
    Input can be a string (dense format) or a list (memory format).
    """
    checksum = 0
    for i, char in enumerate(data):
        if isinstance(char, int) or (isinstance(char, str) and char.isdigit()):
            checksum += i * int(char)
    return checksum

################################ Part 2 ################################

class Block:
    def __init__(self, id, size):
        self.id = id
        self.size = size

    @staticmethod
    def new_file(id, size):
        return Block(id, size)

    @staticmethod
    def new_free(size):
        return Block(None, size)

    def split(self, size_diff):
        return Block.new_free(size_diff), Block.new_free(self.size - size_diff)

def parse_disk_string(disk_string):
    """
    Parse the disk string into a list of blocks (files and free spaces).
    :param disk_string: A string representing the disk.
    :return: A list of Block instances.
    """
    blocks = []
    for index, size in enumerate(disk_string):
        size = int(size)
        if index % 2 == 0:
            blocks.append(Block.new_file(index // 2, size))
        else:
            blocks.append(Block.new_free(size))
    return blocks

def defragment_with_whole_files(disk_string):
    """
    Defragment the disk by rearranging whole file blocks to fit into free spaces.
    :param disk_string: A string representing the disk.
    :return: A list representing the defragmented memory.
    """
    blocks = parse_disk_string(disk_string)
    seen_ids = set()
    file_index = len(blocks) - 1

    while file_index > 0:
        file = blocks[file_index]

        # Skip if this block is free space or already processed.
        if file.id is None or file.id in seen_ids:
            file_index -= 1
            continue

        seen_ids.add(file.id)

        # Find the first free space block large enough to hold the current file block.
        free_index = next(
            (i for i, block in enumerate(blocks) if block.id is None and block.size >= file.size),
            None
        )

        if free_index is None or free_index > file_index:
            file_index -= 1
            continue

        # Rearrange blocks: move the file block into the free space.
        free = blocks[free_index]
        size_diff = free.size - file.size

        if size_diff > 0:
            # Split free space into two blocks.
            remaining_free, displaced_free = free.split(size_diff)
            blocks[free_index] = file
            blocks[file_index] = displaced_free
            blocks.insert(free_index + 1, remaining_free)
        else:
            # Swap file and free space blocks directly.
            blocks[free_index], blocks[file_index] = blocks[file_index], blocks[free_index]
            file_index -= 1

    # Flatten blocks into a memory representation.
    memory = []
    for block in blocks:
        if block.id is not None:
            memory.extend([block.id] * block.size)
        else:
            memory.extend([None] * block.size)

    return memory

# Example usage with a real disk string
disk_string = "2333133121414131402"  # File sizes
print("[INFO] Starting Disk Defragmentation Process")
dense_format = convert_to_dense_with_ids(disk_string)
defragged_string = defragment_with_moves(dense_format)
checksum = calculate_checksum(defragged_string)
print(f"[RESULT] Filesystem Checksum: {checksum}")

# Internal validation with a test string
test_disk_string = disk_string
print("[INFO] Running internal validation...")
# dense_format = convert_to_dense_with_ids(test_disk_string)
defragged_memory = defragment_with_whole_files(test_disk_string)
checksum = calculate_checksum(defragged_memory)
print(f"[RESULT] Test Final Defragmented Memory: {defragged_memory}")
print(f"[RESULT] Test Filesystem Checksum: {checksum}")
expected_checksum = 2858
if checksum == expected_checksum:
    print("[VALIDATION] Internal validation successful!")
else:
    print("[VALIDATION] Internal validation failed! Checksum does not match expected value.")

########################### load from file ################################

# # Load disk string from file after validation
# disk_string = load_disk_string_from_file('day_9_input.txt') 
# defragged_memory = defragment_with_whole_files(disk_string)
# checksum = calculate_checksum(defragged_memory)
# # print(f"[RESULT] Final Defragmented Memory from File: {defragged_memory}")
# print(f"[RESULT] Filesystem Checksum from File: {checksum}")
