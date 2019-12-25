SOURCE_FILE = 'day_24_input.txt'


def read_input():
    grid_start_state = list()
    with open(SOURCE_FILE) as f:
        grid_start_state = list((char for char in (line.rstrip() for line in f.readlines())))
    return grid_start_state


def biodiversity(input_grid):
    i = 0
    score = 0
    for line in input_grid:
        for cell in line:
            if cell == '#':
                score += pow(2, i)
            i += 1
    return score


def next_grid(input_grid):
    neighbour_grid = []
    new_grid = []
    for i in range(5):
        neighbour_grid.append([0, 0, 0, 0, 0,])

    for j in range(5):
        for k in range(5):
            neighbours = 0
            if j > 0 and input_grid[j - 1][k] == '#':
                neighbours += 1
            if j < 4 and input_grid[j + 1][k] == '#':
                neighbours += 1
            if k > 0 and input_grid[j][k - 1] == '#':
                neighbours += 1
            if k < 4 and input_grid[j][k + 1] == '#':
                neighbours += 1
            neighbour_grid[j][k] = neighbours

    for m in range(5):
        new_grid_line = []
        for n in range(5):
            if input_grid[m][n] == '#' and neighbour_grid[m][n] != 1:
                new_grid_line.append('.')
            elif input_grid[m][n] == '.' and neighbour_grid[m][n] in (1, 2):
                new_grid_line.append('#')
            else:
                new_grid_line.append(input_grid[m][n])
        new_grid.append(new_grid_line)
    return new_grid


def main():
    biodiversity_set = set()
    start_grid = read_input()
    biodiversity_set.add(biodiversity(start_grid))
    next_step_grid = next_grid(start_grid)
    i = 1

    while True:
        this_biodiversity = biodiversity(next_step_grid)
        if this_biodiversity in biodiversity_set:
            print(this_biodiversity)
            break
        else:
            biodiversity_set.add(this_biodiversity)
        if i % 100 == 0:
            print('Step ' + str(i))
        i += 1
        next_step_grid = next_grid(next_step_grid)


if __name__ == "__main__":
    main()
