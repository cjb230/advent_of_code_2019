SOURCE_FILE = 'day_8_input.txt'
LAYER_SIZE = 25 * 6


def layer_counter(layer):
    if len(layer) != LAYER_SIZE:
        print('PANIC')
        exit()
    result_set = dict()
    result_set['zeroes'] = 0
    result_set['ones'] = 0
    result_set['twos'] = 0
    result_set['others'] = ''
    for this_pixel in layer:
        if this_pixel == '0':
            result_set['zeroes'] += 1
        elif this_pixel == '1':
            result_set['ones'] += 1
        elif this_pixel== '2':
            result_set['twos'] += 1
        else:
            result_set['others'] += this_pixel
    return result_set


def breakdown(image_data):
    output = dict()
    for i in range(1, int((len(image_data) / LAYER_SIZE) + 1)):
        lower_bound = (i - 1) * LAYER_SIZE
        upper_bound = i * LAYER_SIZE
        output[i] = image_data[lower_bound:upper_bound]
        #print('- ' + output[i])
    return output


def main():
    with open(SOURCE_FILE) as f:
        image_data = f.readline()
    #print(len(image_data))
    #print(len(image_data) / LAYER_SIZE)
    #print(breakdown(image_data))
    layers = breakdown(image_data)

    min_zeroes = 150
    product_at_min_zeroes = 0
    for layer_number, layer_value in layers.items():
        layer_results = layer_counter(layer_value)
        if layer_results['zeroes'] < min_zeroes:
            print(str(layer_number) + ' has ' + str(layer_results['zeroes']) + ' zeroes.')
            min_zeroes = layer_results['zeroes']
            product_at_min_zeroes = layer_results['ones'] * layer_results['twos']
    print(product_at_min_zeroes)


if __name__ == "__main__":
    main()
