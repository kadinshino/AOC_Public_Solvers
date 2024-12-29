from collections import defaultdict, deque

def parse_input_file(file_path):
    initial_values = {}
    operations = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                try:
                    name, value = line.split(':')
                    initial_values[name.strip()] = int(value.strip())
                except ValueError:
                    print(f"Skipping malformed initial value line: {line}")
            elif '->' in line:
                try:
                    operand1, operator, operand2, _, result = line.split(' ')
                    operations.append((operand1, operator, operand2, result))
                except ValueError:
                    print(f"Skipping malformed operation line: {line}")
            else:
                print(f"Unrecognized Line Format: {line}")

    return initial_values, operations

def apply_operations(initial_values, operations):
    mem = dict(**initial_values)
    dependencies = defaultdict(list)
    in_degree = defaultdict(int)

    # Build dependency graph and in-degree map
    for left, op, right, result in operations:
        dependencies[left].append((op, right, result))
        dependencies[right].append((op, left, result))
        in_degree[result] += 1

    # Initialize queue with nodes having no incoming edges
    queue = deque([wire for wire in initial_values if in_degree[wire] == 0])

    while queue:
        current = queue.popleft()
        for op, other_operand, result in dependencies[current]:
            if other_operand in mem:
                if op == 'AND':
                    mem[result] = mem[current] & mem[other_operand]
                elif op == 'OR':
                    mem[result] = mem[current] | mem[other_operand]
                elif op == 'XOR':
                    mem[result] = mem[current] ^ mem[other_operand]
                else:
                    raise ValueError(f"Unknown operation: {op}")

                in_degree[result] -= 1
                if in_degree[result] == 0:
                    queue.append(result)

    return mem

def sum_zvalues(results):
    z_keys = sorted([k for k in results if k.startswith('z')], reverse=True)
    result = 0
    for k in z_keys:
        result <<= 1
        result += results[k]
    return result

def identify_swapped_wires(operations, values):
    use_map = defaultdict(list)
    for op in operations:
        use_map[op[0]].append(op)
        use_map[op[2]].append(op)

    swapped = set()

    def add_if_swapped(result, condition):
        if condition:
            swapped.add(result)

    for left, op, right, result in operations:
        if result == 'z45' or left == 'x00':
            continue

        usage = use_map[result]
        using_ops = [o[1] for o in usage]

        is_input_left = left[0] in 'xy'
        is_input_right = right[0] in 'xy'
        result_startswith_z = result.startswith('z')
        
        if op == 'XOR':
            if is_input_left:
                add_if_swapped(result, not is_input_right or (result_startswith_z and result != 'z00'))
                add_if_swapped(result, result != 'z00' and sorted(using_ops) != ['AND', 'XOR'])
            else:
                add_if_swapped(result, not result_startswith_z)
        elif op == 'AND':
            add_if_swapped(result, is_input_left and not is_input_right)
            add_if_swapped(result, [o[1] for o in usage] != ['OR'])
        elif op == 'OR':
            add_if_swapped(result, is_input_left or is_input_right)
            add_if_swapped(result, sorted(using_ops) != ['AND', 'XOR'])

    return ','.join(sorted(swapped))

# Example Usage
if __name__ == '__main__':
    file_path = 'day_24_input.txt'
    initial_values, operations = parse_input_file(file_path)

    results = apply_operations(initial_values, operations)
    decimal_output = sum_zvalues(results)
    swapped_wires = identify_swapped_wires(operations, initial_values)

    print(f"Final Decimal Output P1: {decimal_output}")
    print(f"Final Swapped Wires P2: {swapped_wires}")
