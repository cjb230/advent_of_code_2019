import itertools
import math
SOURCE_FILE = 'day_7_input.txt'


def unpack_instruction(instruction):
    unpacked_instruction = dict()
    unpacked_instruction['opcode'] = instruction % 100
    unpacked_instruction['p1_mode'] = 'position'
    unpacked_instruction['p2_mode'] = 'position'
    unpacked_instruction['p3_mode'] = 'position'

    mode_details = (instruction - unpacked_instruction['opcode']) / 100
    if mode_details > 0:
        if mode_details % 10 == 1:
            unpacked_instruction['p1_mode'] = 'immediate'

        mode_details = math.floor(mode_details / 10)
        if mode_details % 10 == 1:
            unpacked_instruction['p2_mode'] = 'immediate'

        mode_details = math.floor(mode_details / 10)
        if mode_details % 10 == 1:
            unpacked_instruction['p3_mode'] = 'immediate'

    if unpacked_instruction['opcode'] == 3:
        unpacked_instruction['p1_mode'] = 'position'
    if unpacked_instruction['opcode'] in (1, 2):
        unpacked_instruction['p3_mode'] = 'position'

    return unpacked_instruction


def docker_intcode(program, inputs):
    outputs = list()

    next_input = 0
    memory_pointer = 0
    step = 1
    continue_processing = True

    while continue_processing:
        this_instruction = program[memory_pointer:memory_pointer+4]
        #print('STEP ' + str(step))
        #print('Memory pointer =  ' + str(memory_pointer))
        #print('Instructions = ' + str(this_instruction))
        params_and_opcode = unpack_instruction(this_instruction[0])
        opcode = params_and_opcode['opcode']
        #print('Unpacked instruction = ' + str(params_and_opcode))

        if opcode != 99:
            if params_and_opcode['p1_mode'] == 'position':
                param_1 = program[this_instruction[1]]
            elif params_and_opcode['p1_mode'] == 'immediate':
                param_1 = this_instruction[1]
            else:
                param_1 = 'UNKNOWN'

            if opcode in (1, 2, 5, 6, 7, 8): # opcodes that take three or more parameters
                if params_and_opcode['p2_mode'] == 'position':
                    param_2 = program[this_instruction[2]]
                elif params_and_opcode['p2_mode'] == 'immediate':
                    param_2 = this_instruction[2]
                else:
                    param_2 = 'UNKNOWN'
                #print('PROCESSING: ' + str(this_instruction) + ' .. [' + str(opcode) + ', ' + str(param_1) +
                #      ', ' + str(param_2) + ', ' + str(this_instruction[3]) + ']')
            else:
                #print('PROCESSING: ' + str(this_instruction) + ' .. [' + str(opcode) + ', ' + str(param_1) + ']')
                pass

        if opcode == 1:
            try:
                program[this_instruction[3]] = param_1 + param_2
            except (TypeError):
                print('INPUTS = ' + str(inputs))
                print(param_1)
                print(param_2)
                print(memory_pointer)
                exit()
            memory_pointer += 4
        elif opcode == 2:
            program[this_instruction[3]] = param_1 * param_2
            memory_pointer += 4
        elif opcode == 3:
            program[this_instruction[1]] = inputs[next_input]
            next_input += 1
            memory_pointer += 2
        elif opcode == 4:
            # print('OUTPUT: ' + str(param_1))
            outputs.append(param_1)
            memory_pointer += 2
        elif opcode == 5:
            if param_1 != 0:
                memory_pointer = param_2
            else:
                memory_pointer += 3
        elif opcode == 6:
            if param_1 == 0:
                memory_pointer = param_2
            else:
                memory_pointer += 3
        elif opcode == 7:
            if param_1 < param_2:
                program[this_instruction[3]] = 1
            else:
                program[this_instruction[3]] = 0
            memory_pointer += 4
        elif opcode == 8:
            if param_1 == param_2:
                program[this_instruction[3]] = 1
            else:
                program[this_instruction[3]] = 0
            memory_pointer += 4
        elif opcode == 99:
            continue_processing = False
        else:
            print('ERROR')
        step += 1

    return outputs


def generate_lexicographic_combinations(input_range):
    range_list = list(range(input_range))
    return itertools.permutations(range_list)


def simulate_combinations(program):
    combinations = generate_lexicographic_combinations(5)
    max_output = None

    for combination in combinations:
        last_output = 0
        for this_amplifier in range(5):
            this_amplifier_inputs = [combination[this_amplifier], last_output]
            last_output = docker_intcode(program.copy(), this_amplifier_inputs)[0]
        if max_output is None or last_output > max_output:
            max_output = last_output

    return max_output


def main():
    with open(SOURCE_FILE) as f:
        amplifier_prog = [int(this_string) for  this_string in f.readline().split(',')]
    max_output = simulate_combinations(amplifier_prog)
    print('MAX = ' + str(max_output))


if __name__ == "__main__":
    main()

