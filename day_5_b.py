import math
SOURCE_FILE = 'day_5_input.txt'


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


def main():
    with open(SOURCE_FILE) as f:
        test_prog = [int(this_string) for  this_string in f.readline().split(',')]
    memory_pointer = 0
    step = 0
    continue_processing = True

    while continue_processing:
        print()
        step += 1
        print('STEP ' + str(step))
        print('Memory pointer =  ' + str(memory_pointer))

        this_instruction = test_prog[memory_pointer:memory_pointer+4]
        print('Instructions = ' + str(this_instruction))
        params_and_opcode = unpack_instruction(this_instruction[0])
        opcode = params_and_opcode['opcode']
        print('Unpacked instruction = ' + str(params_and_opcode))

        if opcode != 99:
            if params_and_opcode['p1_mode'] == 'position':
                param_1 = test_prog[this_instruction[1]]
            elif params_and_opcode['p1_mode'] == 'immediate':
                param_1 = this_instruction[1]
            else:
                param_1 = 'UNKNOWN'

            if opcode in (1, 2, 5, 6, 7, 8): # opcodes that take three or more parameters
                if params_and_opcode['p2_mode'] == 'position':
                    param_2 = test_prog[this_instruction[2]]
                elif params_and_opcode['p2_mode'] == 'immediate':
                    param_2 = this_instruction[2]
                else:
                    param_2 = 'UNKNOWN'
                print('PROCESSING: ' + str(this_instruction) + ' .. [' + str(opcode) + ', ' + str(param_1) +
                      ', ' + str(param_2) + ', ' + str(this_instruction[3]) + ']')
            else:
                print('PROCESSING: ' + str(this_instruction) + ' .. [' + str(opcode) + ', ' + str(param_1) + ']')
                pass

        if opcode == 1:
            test_prog[this_instruction[3]] = param_1 + param_2
            memory_pointer += 4
        elif opcode == 2:
            test_prog[this_instruction[3]] = param_1 * param_2
            memory_pointer += 4
        elif opcode == 3:
            user_input = input("Value needed: ")
            test_prog[this_instruction[1]] = int(user_input)
            memory_pointer += 2
        elif opcode == 4:
            print('OUTPUT: ' + str(param_1))
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
                test_prog[this_instruction[3]] = 1
            else:
                test_prog[this_instruction[3]] = 0
            memory_pointer += 4
        elif opcode == 8:
            if param_1 == param_2:
                test_prog[this_instruction[3]] = 1
            else:
                test_prog[this_instruction[3]] = 0
            memory_pointer += 4
        elif opcode == 99:
            continue_processing = False
        else:
            print('ERROR')


if __name__ == "__main__":
    main()

