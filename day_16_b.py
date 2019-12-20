import math

SOURCE_FILE = 'day_16_input.txt'
BASE_PATTERN = [0, 1, 0, -1]


def phase_pattern(element_number, length_required):
    output = list()
    i = 0
    while len(output) < (length_required + 1):
        phase_location = i % (element_number * len(BASE_PATTERN))
        base_pattern_slice = math.floor(phase_location / element_number)
        output.append(BASE_PATTERN[base_pattern_slice])
        i += 1
    output.pop(0)
    return output


def phase(phase_number, phase_input):
    output_length = len(phase_input)
    phase_output = list()
    i = 0

    for j in range(len(phase_input)):
        this_sum = 0
        #print()
        #print()
        #print('Digit ' + str(j))
        #print('==========')
        this_phase_pattern = phase_pattern(j + 1, output_length)
        for k in range(len(phase_input)):
            #print()
            #print(k)
            #print(str(phase_input[k]) + ' * ' + str(this_phase_pattern[k]))
            this_sum += phase_input[k] * this_phase_pattern[k]
            #print(this_sum)
        phase_output.append(abs(this_sum) % 10)
        #print(phase_output)

    return phase_output


def main():
    with open(SOURCE_FILE) as f:
        number_string = f.readline().rstrip()
    number_list = [int(character) for character in number_string]
    #print(number_list)
    phase_input = number_list
    for i in range(1, 101):
        phase_output = phase(i, phase_input)
        phase_input = phase_output.copy()
    print(i)
    print(phase_output)


if __name__ == "__main__":
    main()
