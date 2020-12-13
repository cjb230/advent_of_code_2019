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
    bb_program[0] = 2
    bb_brain = ic.IntcodeComputer(bb_program)
    paddle_x_pos = -1
    ball_x_pos = -1
    score = 0
    next_input = [0]
    loop = 0
    while not bb_brain.is_halted:
        loop += 1
        results = bb_brain.run_to_halt(new_inputs=next_input, print_output=False)
        draw_details = {}
        x = 1
        block_count = 0
        for this_output in results['output']:
            draw_details[x] = this_output
            x += 1
            if x == 4:
                x = 1
                if draw_details[3] == PADDLE:
                    paddle_x_pos = draw_details[1]
                elif draw_details[3] == BALL:
                    ball_x_pos = draw_details[1]
                if draw_details[1] == -1 and draw_details[2] == 0:
                    score = draw_details[3]
        if paddle_x_pos > ball_x_pos:
            next_input = [-1]
        elif paddle_x_pos < ball_x_pos:
            next_input = [1]
        else:
            next_input = [0]
    print(score)


if __name__ == "__main__":
    main()
