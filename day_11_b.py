import intcode as ic

SOURCE_FILE = 'day_11_input'
IS_BLACK = 0
IS_WHITE = 1
TURN_LEFT = 0
TURN_RIGHT = 1
FACING_UP = 0
FACING_RIGHT = 1
FACING_DOWN = 2
FACING_LEFT = 3

def program():
    with open(SOURCE_FILE) as f:
        intcode_program = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    return intcode_program


def move_robot(current_location, current_heading, turn_direction: int):
    results = dict()
    if turn_direction not in (TURN_LEFT, TURN_RIGHT):
        print('Unknown turn direction ' + str(turn_direction))
        exit()
    if current_heading not in (FACING_UP, FACING_RIGHT, FACING_DOWN, FACING_LEFT):
        print('Unknown current facing ' + str(current_heading))
        exit()
    if turn_direction == TURN_LEFT:
        new_direction = current_heading - 1
        if new_direction == -1:
            new_direction = 3
    else: # turning right
        new_direction = current_heading + 1
        if new_direction == 4:
            new_direction = 0
    results['direction'] = new_direction
    if new_direction == FACING_UP:
        new_location = (current_location[0], current_location[1] + 1)
    elif new_direction == FACING_DOWN:
        new_location = (current_location[0], current_location[1] - 1)
    elif new_direction == FACING_RIGHT:
        new_location = (current_location[0] + 1, current_location[1])
    else: # facing left
        new_location = (current_location[0] - 1, current_location[1])
    results['location'] = new_location
    return results


def main():
    robot_program = program()
    robot_brain = ic.IntcodeComputer(robot_program)
    current_panel = (0, 0)
    current_heading = FACING_UP
    panels_ever_painted = set()
    panels_white = set()
    panels_white.add((0, 0))
    loop = 0
    while not(robot_brain.is_halted):
        if current_panel in panels_white:
            next_input = [1]
        else:
            next_input = [0]
        results = robot_brain.run_to_halt(new_inputs=next_input, print_output=False)
        if results['output'][0] == 1:
            panels_white.add(current_panel)
        elif results['output'][0] == 0:
            panels_white.discard(current_panel)
        else:
            print('Unknown paint colour ' + str(results['output']))
        panels_ever_painted.add(current_panel)
        move_result = move_robot(current_panel, current_heading, results['output'][1])
        current_panel = move_result['location']
        current_heading = move_result['direction']
        loop += 1

    min_x = 100
    max_x = -100
    min_y = 100
    max_y = -100
    for this_panel in panels_white:
        this_x = this_panel[0]
        if this_x < min_x:
            min_x = this_x
        if this_x > max_x:
            max_x = this_x
        this_y = this_panel[1]
        if this_y < min_y:
            min_y = this_y
        if this_y > max_y:
            max_y = this_y
    x_range = max_x - min_x
    y_range = max_y - min_y

    picture = list()
    for this_row in range(y_range + 1):
        picture.append([' ' for x in range(x_range + 1)])
    for this_panel in panels_white:

        picture[-1 * this_panel[1]][this_panel[0] - 1] = '#'
    for this_row in range(y_range + 1):
        str1 = ''
        print(str1.join(picture[this_row]))


if __name__ == "__main__":
    main()
