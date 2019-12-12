SOURCE_FILE = 'day_12_input.txt'
AXES = ('x', 'y', 'z')

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
    for i in range(1000):
        next_positions, next_velocities = step(initial_positions, initial_velocities, True, i+1)
        initial_positions = next_positions
        initial_velocities = next_velocities

    print(str(next_positions))
    print()
    print(str(next_velocities))

    total_energy = 0
    for moon_key, moon_positions_dict in next_positions.items():
        moon_pe = 0
        moon_ke = 0
        for axis in AXES:
            moon_pe += abs(moon_positions_dict[axis])
            moon_ke += abs(next_velocities[moon_key][axis])
        moon_energy = moon_pe * moon_ke
        print('Moon ' + str(moon_key) + ' energy = ' + str(moon_energy))
        total_energy += moon_energy
    print('Total = ' + str(total_energy))


if __name__ == "__main__":
    main()
