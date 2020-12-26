import intcode as ic

SOURCE_FILE = 'day_19_input.txt'


def program():
    with open(SOURCE_FILE) as f:
        intcode_program = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    return intcode_program


def main():
    drone_program = program()
    affected_points = 0
    for x in range(0, 50):
        for y in range(0, 50):
            drone_brain = ic.IntcodeComputer(drone_program.copy(), [x, y])
            this_result = drone_brain.run_to_halt(print_output=False)
            if this_result['output'][0] == 1:
                affected_points += 1
    print(affected_points)


if __name__ == "__main__":
    main()
