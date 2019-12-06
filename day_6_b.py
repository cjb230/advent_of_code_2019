SOURCE_FILE = 'day_6_input.txt'
SATELLITE_PARENTS = dict()


def path_to_root(satellite):
    global SATELLITE_PARENTS
    path = list()
    current_loc = satellite
    while True:
        if current_loc == 'COM':
            break
        current_loc = SATELLITE_PARENTS[current_loc]
        path.append(current_loc)
    return path


def main():
    global SATELLITE_PARENTS

    with open(SOURCE_FILE) as f:
        orbits = [orbit.rstrip() for orbit in f.readlines()]

    for orbit in orbits:
        SATELLITE_PARENTS[orbit[4:]] = orbit[0:3]
    print('SATELLITE PARENTS: ' + str(SATELLITE_PARENTS))

    santa_path = path_to_root('SAN')
    my_path = path_to_root('YOU')

    common_path_length = 0
    santa_path.reverse()
    my_path.reverse()
    while True:
        if my_path[common_path_length] == santa_path[common_path_length]:
            common_path_length += 1
        else:
            break
    #print('Common path length was: ' + str(common_path_length))
    traverse_path_length = len(santa_path) + len(my_path) - 2 * common_path_length
    print(traverse_path_length)


if __name__ == "__main__":
    main()
