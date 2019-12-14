SOURCE_FILE = 'day_10_input.txt'


def gcd(a, b):
    if a % b == 0:
        return b
    return gcd(b, a % b)


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return x


def get_asteroid_map():
    with open(SOURCE_FILE) as f:
        asteroid_map = [[this_char for this_char in this_line.rstrip()] for this_line in f.readlines()]
    y_size = len(asteroid_map)
    x_size = len(asteroid_map[0])

    rectified_asteroid_map = list()
    for x in range(x_size):
        new_list = list()
        rectified_asteroid_map.append(new_list)
        for y in range(y_size):
            rectified_asteroid_map[x].append(asteroid_map[y][x])

    return rectified_asteroid_map


def reduce_vector(x_in, y_in):
    x_result = x_in
    y_result = y_in

    if x_in != 0 and y_in != 0:
        cd = gcd(abs(x_in), abs(y_in))
        if cd > 1:
            x_result = int(x_in / cd)
            y_result = int(y_in / cd)
    else:
        x_result = sign(x_in)
        y_result = sign(y_in)

    return x_result, y_result


def vector_to_rotation_order(this_vector):
    rotation_order = None

    if this_vector[0] == 0 and this_vector[1] == -1:  # up
        rotation_order = 0
    elif this_vector[0] == 1 and this_vector[1] == 0:  # right
        rotation_order = 1
    elif this_vector[0] == 0 and this_vector[1] == 1:  # down
        rotation_order = 2
    elif this_vector[0] == -1 and this_vector[1] == 0:  # left
        rotation_order = 3
    elif this_vector[0] > 0 and this_vector[1] < 0:  # top right
        rotation_order = -1 * (this_vector[0] / this_vector[1])
    elif this_vector[0] > 0 and this_vector[1] > 0:  # bottom right
        rotation_order = 1 + (this_vector[1] / this_vector[0])
    elif this_vector[0] < 0 and this_vector[1] > 0:  # bottom left
        rotation_order = 2 + (-1 * (this_vector[0] / this_vector[1]))
    elif this_vector[0] < 0 and this_vector[1] < 0:  # top left
        rotation_order = 3 + (this_vector[1] / this_vector[0])

    return rotation_order


def main():
    space_map = get_asteroid_map()
    x_size = len(space_map)
    y_size = len(space_map[0])

    asteroids_found = 0
    location_x = 11
    location_y = 19
    if space_map[location_x][location_y] == '#':
        asteroids_found += 1
        asteroid_vector_dict = dict()
        for considering_x in range(x_size):
            for considering_y in range(y_size):
                if space_map[considering_x][considering_y] == '#':
                    vector_x = considering_x - location_x
                    vector_y = considering_y - location_y
                    if max(abs(vector_x), abs(vector_y)) > 0:  # ignoring the asteroid we're on
                        this_reduced_vector = tuple(reduce_vector(vector_x, vector_y))
                        try:
                            multiplier = vector_x / this_reduced_vector[0]
                        except ZeroDivisionError:
                            multiplier = vector_y / this_reduced_vector[1]
                        try:
                            asteroid_vector_dict[this_reduced_vector].add(multiplier)
                        except KeyError:
                            asteroid_vector_dict[this_reduced_vector] = set()
                            asteroid_vector_dict[this_reduced_vector].add(multiplier)
        #print(str(asteroid_vector_dict))

    print('Max visible = ' + str(len(asteroid_vector_dict)) + ', from ' + str(location_x) + ', ' + str(location_y))
    #print(str(asteroid_vector_dict))


    rotation_order_dict = dict()
    i = 0
    for this_vector, multiples in asteroid_vector_dict.items():
        i += 1
        #print()
        #print(i)
        #print(len(rotation_order_dict))
        this_rotation_order = vector_to_rotation_order(this_vector)
        multiples_list = list(multiples)
        multiples_list.sort()
        final_multiples = [int(this_multiple) for this_multiple in multiples_list]
        #print(str(final_multiples))
        rotation_order_dict[this_rotation_order] = final_multiples

    #print(len(rotation_order_dict))
    #print(str(rotation_order_dict))
    #for direction in sorted(rotation_order_dict.items()):
    #    print(str(direction))

    asteroids_destroyed = 0
    current_direction = 0
    while True:
        # fire
        print()
        print('Asteroids destroyed = ' + str(asteroids_destroyed))
        asteroids_remaining = 0
        for direction, asteroids_in_direction in rotation_order_dict.items():
            asteroids_remaining += len(asteroids_in_direction)
        print('Asteroids remaining = ' + str(asteroids_remaining))
        print('Current direction = ' + str(current_direction))
        print(str(rotation_order_dict[current_direction]))

        asteroids_in_this_direction = rotation_order_dict[current_direction]
        if len(asteroids_in_this_direction) == 1:
            del rotation_order_dict[current_direction]
        else:
            asteroids_in_this_direction.pop(0)
        print('Directions remaining = ' + str(len(rotation_order_dict)))

        asteroids_destroyed += 1
        if asteroids_destroyed == 200:
            break

        # rotate
        bigger_directions = [direction for direction in rotation_order_dict.keys() if direction > current_direction]
        if len(bigger_directions) == 0:
            bigger_directions = rotation_order_dict.keys()
        current_direction = min(bigger_directions)


    #print(str(rotation_order_dict))
    for direction in sorted(rotation_order_dict.items()):
        print(str(direction))


if __name__ == "__main__":
    main()
