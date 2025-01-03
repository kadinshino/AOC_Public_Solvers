import re

class ThreeBitComputer:
    def __init__(self, registers, program):
        self.A, self.B, self.C = registers
        self.program = program
        self.instruction_pointer = 0
        self.output = []

    def combo_operand_value(self, operand):
        if operand is None or operand == 7:
            return None  # Invalid or reserved combo operand
        if 0 <= operand <= 3:
            return operand  # Literal values 0–3
        if operand == 4:
            return self.A  # Value of register A
        if operand == 5:
            return self.B  # Value of register B
        if operand == 6:
            return self.C  # Value of register C

    def run(self):
        while self.instruction_pointer < len(self.program):
            opcode = self.program[self.instruction_pointer]
            operand = self.program[self.instruction_pointer + 1] if self.instruction_pointer + 1 < len(self.program) else None
            operand_value = self.combo_operand_value(operand)

            if opcode == 0:  # adv
                if operand_value is not None:
                    self.A //= 2 ** operand_value

            elif opcode == 1:  # bxl
                self.B ^= operand

            elif opcode == 2:  # bst
                if operand_value is not None:
                    self.B = operand_value % 8

            elif opcode == 3:  # jnz
                if self.A != 0:
                    self.instruction_pointer = operand
                    continue

            elif opcode == 4:  # bxc
                self.B ^= self.C

            elif opcode == 5:  # out
                if operand_value is not None:
                    self.output.append(operand_value % 8)

            elif opcode == 6:  # bdv
                if operand_value is not None:
                    self.B = self.A // (2 ** operand_value)

            elif opcode == 7:  # cdv
                if operand_value is not None:
                    self.C = self.A // (2 ** operand_value)

            # Move to the next instruction
            self.instruction_pointer += 2

        return self.output

    @staticmethod
    def parse_file(filename):
        with open(filename, 'r') as file:
            content = file.read()

        # Extract register values
        register_pattern = r"Register A:\s*(\d+)\s*Register B:\s*(\d+)\s*Register C:\s*(\d+)"
        registers_match = re.search(register_pattern, content)
        if not registers_match:
            raise ValueError("Invalid register format in input.")
        registers = tuple(map(int, registers_match.groups()))

        # Extract program
        program_pattern = r"Program:\s*([\d,]+)"
        program_match = re.search(program_pattern, content)
        if not program_match:
            raise ValueError("Invalid program format in input.")
        program = list(map(int, program_match.group(1).split(',')))

        return registers, program

    @staticmethod
    def find_closest_a_for_self_output(program):
        def recursive_match(values, program, current_a, results, level):
            target_value = values[-level]
            for i in range(8):  # Test all possible values (0 to 7)
                test_a = current_a + i
                # Simulate the program execution with this `test_a`
                computer = ThreeBitComputer((test_a, 0, 0), program)
                result = computer.run()

                # Check if the output matches the current target value
                if len(result) >= level and result[-level] == target_value:
                    if level == len(values):  # Base case: all levels matched
                        results.append(test_a)
                    else:  # Recursive case: go deeper
                        recursive_match(values, program, test_a * 8, results, level + 1)

        # Prepare to start recursion
        values = program  # Program doubles as the target self-output
        results = []
        recursive_match(values, program, 0, results, 1)

        # Return the smallest valid `A`, or None if no solutions found
        return min(results) if results else None

if __name__ == "__main__":
    # Assume the input is in a file named 'input.txt'
    input_file = 'day_17_input.txt'

    # Parse the input from the file
    registers, program = ThreeBitComputer.parse_file(input_file)

    # Initialize the computer
    computer = ThreeBitComputer(registers, program)

    # Part 1: Run the program
    output = computer.run()
    print("Part 1 Output:", ",".join(map(str, output)))

    # Part 2: Find the closest initial A that causes the program to output itself
    closest_a = ThreeBitComputer.find_closest_a_for_self_output(program)
    print(f"Part 2 Closest Initial A: {closest_a}")

