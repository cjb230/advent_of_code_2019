SOURCE_FILE = 'day_8_input.txt'
LAYER_SIZE = 25 * 6


def breakdown(image_data):
    output = dict()
    for i in range(1, int((len(image_data) / LAYER_SIZE) + 1)):
        lower_bound = (i - 1) * LAYER_SIZE
        upper_bound = i * LAYER_SIZE
        output[i] = image_data[lower_bound:upper_bound]
        #print('- ' + output[i])
    return output


def pretty_print(input_layer):
    line_length = 25
    i = 1
    for pixel in input_layer:
        if pixel == 0:
            print('#', end='')
        elif pixel == 1:
            print(' ', end='')
        if i % 25 == 0:
            print('\n', end='')
        i += 1


def main():
    with open(SOURCE_FILE) as f:
        image_data = f.readline()
    #print(len(image_data))
    #print(len(image_data) / LAYER_SIZE)
    #print(breakdown(image_data))
    layers = breakdown(image_data)

    viewable_layer = list()
    for this_pixel in range(1, LAYER_SIZE + 1):
        for depth in range(1, 101):
            possible_pixel = layers[depth][this_pixel -1]
            if possible_pixel in ('0', '1'):
                viewable_layer.append(int(possible_pixel))
                break
    pretty_print(viewable_layer)


if __name__ == "__main__":
    main()
