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

    # rectify x,y for sanity
    rectified_asteroid_map = list()
    for x in range(x_size):
        new_list = list()
        rectified_asteroid_map.append(new_list)
        for y in range(y_size):
            #print(str(x) + ', ' + str(y))
            #print(asteroid_map[y][x])
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


def main():
    space_map = get_asteroid_map()
    #print(str(asteroid_map))
    #print(str(asteroid_map[0][1]))
    x_size = len(space_map)
    y_size = len(space_map[0])

    max_visible_asteroids = 0
    for location_x in range(x_size):
        for location_y in range(y_size):
            if space_map[location_x][location_y] == '#':
                print('Processing asteroid at ' + str(location_x) + ', ' + str(location_y) + ' ...', end=' ')
                asteroid_vector_set = set()
                for considering_x in range(x_size):
                    for considering_y in range(y_size):
                        if space_map[considering_x][considering_y] == '#':
                            #print('  Considering asteroid at ' + str(considering_x) + ', ' + str(considering_y))
                            vector_x = considering_x - location_x
                            vector_y = considering_y - location_y
                            if max(abs(vector_x), abs(vector_y)) > 0:  # ignoring the asteroid we're on
                                asteroid_vector_set.add(tuple(reduce_vector(vector_x, vector_y)))
                currently_visible = len(asteroid_vector_set)
                print(str(currently_visible) + ' visible')
                if currently_visible > max_visible_asteroids:
                    max_visible_asteroids = currently_visible
    print('Max visible = ' + str(max_visible_asteroids))


if __name__ == "__main__":
    main()
