import math
SOURCE_FILE = 'day_12_input.txt'
AXES = ('x', 'y', 'z')


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def parsed_input():
    moons_positions_actual = {1: {'x': -7, 'y': 17, 'z': -11},
                              2: {'x': 9, 'y': 12, 'z': 5},
                              3: {'x': -9, 'y': 0, 'z': -4},
                              4: {'x': 4, 'y': 6, 'z': 0}}

    moons_positions_test_1 = {1: {'x': -1, 'y': 0, 'z': 2},
                              2: {'x': 2, 'y': -10, 'z': -7},
                              3: {'x': 4, 'y': -8, 'z': 8},
                              4: {'x': 3, 'y': 5, 'z': -1}}

    return moons_positions_actual


def zero_matrix():
    matrix = {1: {'x': 0, 'y': 0, 'z': 0},
              2: {'x': 0, 'y': 0, 'z': 0},
              3: {'x': 0, 'y': 0, 'z': 0},
              4: {'x': 0, 'y': 0, 'z': 0}}
    return matrix


def step(starting_positions, starting_velocities, print_state=False, print_label=None):
    accelerations = zero_matrix()
    new_velocities = zero_matrix()
    new_positions = zero_matrix()
    for moon_a, position_a in starting_positions.items():
        for moon_b, position_b in starting_positions.items():
            if moon_a > moon_b:
                if position_a['x'] > position_b['x']:
                    accelerations[moon_a]['x'] -= 1
                    accelerations[moon_b]['x'] += 1
                elif position_a['x'] < position_b['x']:
                    accelerations[moon_a]['x'] += 1
                    accelerations[moon_b]['x'] -= 1

                if position_a['y'] > position_b['y']:
                    accelerations[moon_a]['y'] -= 1
                    accelerations[moon_b]['y'] += 1
                elif position_a['y'] < position_b['y']:
                    accelerations[moon_a]['y'] += 1
                    accelerations[moon_b]['y'] -= 1

                if position_a['z'] > position_b['z']:
                    accelerations[moon_a]['z'] -= 1
                    accelerations[moon_b]['z'] += 1
                elif position_a['z'] < position_b['z']:
                    accelerations[moon_a]['z'] += 1
                    accelerations[moon_b]['z'] -= 1

    for moon in starting_velocities:
        for axis in AXES:
            new_velocities[moon][axis] = starting_velocities[moon][axis] + accelerations[moon][axis]

    for moon in starting_positions:
        for axis in AXES:
            new_positions[moon][axis] = starting_positions[moon][axis] + new_velocities[moon][axis]

    if print_state:
        print()
        print('After step ' + str(print_label) + ':')
        print(str(new_positions))
        print(str(new_velocities))

    return new_positions, new_velocities


def main():
    initial_positions = parsed_input()
    initial_velocities = zero_matrix()
    saved_positions = initial_positions

    x_cycle_length = None
    y_cycle_length = None
    z_cycle_length = None
    i = 0
    while x_cycle_length is None or y_cycle_length is None or z_cycle_length is None:
        i += 1
        if i % 50000 == 0:
            print('Step ' + str(i))
        x_potentially_equal = True
        y_potentially_equal = True
        z_potentially_equal = True

        next_positions, next_velocities = step(initial_positions, initial_velocities, False, i)
        initial_positions = next_positions
        initial_velocities = next_velocities

        for moon_key, moon_positions_dict in next_positions.items():
            if x_potentially_equal:
                if next_velocities[moon_key]['x'] != 0:
                    x_potentially_equal = False
                elif next_positions[moon_key]['x'] != saved_positions[moon_key]['x']:
                    x_potentially_equal = False

            if y_potentially_equal:
                if next_velocities[moon_key]['y'] != 0:
                    y_potentially_equal = False
                elif next_positions[moon_key]['y'] != saved_positions[moon_key]['y']:
                    y_potentially_equal = False

            if z_potentially_equal:
                if next_velocities[moon_key]['z'] != 0:
                    z_potentially_equal = False
                elif next_positions[moon_key]['z'] != saved_positions[moon_key]['z']:
                    z_potentially_equal = False

        if x_cycle_length is None and x_potentially_equal:
            x_cycle_length = i
            print('X - ' + str(next_velocities))
        if y_cycle_length is None and y_potentially_equal:
            y_cycle_length = i
            print('Y - ' + str(next_velocities))
        if z_cycle_length is None and z_potentially_equal:
            z_cycle_length = i
            print('Z - ' + str(next_velocities))

    print('x = ' + str(x_cycle_length))
    print('y = ' + str(y_cycle_length))
    print('z = ' + str(z_cycle_length))
    total_cycle_length = lcm(x_cycle_length, lcm(y_cycle_length, z_cycle_length))
    print('total = ' + str(total_cycle_length))


if __name__ == "__main__":
    main()
