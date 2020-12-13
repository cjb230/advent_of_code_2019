import intcode as ic

SOURCE_FILE = 'day_13_input.txt'
EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4


def program():
    with open(SOURCE_FILE) as f:
        intcode_program = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    return intcode_program


def main():
    bb_program = program()
    bb_brain = ic.IntcodeComputer(bb_program)
    while not bb_brain.is_halted:
        results = bb_brain.run_to_halt(print_output=False)
        set = {}
        x = 1
        block_count = 0
        for this_output in results['output']:
            set[x] = this_output
            x += 1
            if x == 4:
                x = 1
                if set[3] == BLOCK:
                    block_count += 1
    print(block_count)


if __name__ == "__main__":
    main()
