from collections import defaultdict

SOURCE_FILE = 'day_13_input.txt'

OC_ADD = 1
OC_MULTIPLY = 2
OC_INPUT = 3
OC_OUTPUT = 4
OC_JUMP_IF_TRUE = 5
OC_JUMP_IF_FALSE = 6
OC_LESS_THAN = 7
OC_EQUALS = 8
OC_ADJUST_REL_BASE = 9
OC_TERMINATE = 99
MODE_POSITION = 0
MODE_IMMEDIATE = 1
MODE_RELATIVE = 2


def opcode_parameter_number(opcode):
    parameter_number = None
    if opcode in (OC_ADD, OC_MULTIPLY, OC_LESS_THAN, OC_EQUALS):
        parameter_number = 3
    elif opcode in (OC_JUMP_IF_TRUE, OC_JUMP_IF_FALSE):
        parameter_number = 2
    elif opcode in (OC_INPUT, OC_OUTPUT, OC_ADJUST_REL_BASE):
        parameter_number = 1
    elif opcode == OC_TERMINATE:
        parameter_number = 0
    return parameter_number


def instruction_modes(instruction):
    unpacked_instruction = dict()
    unpacked_instruction['opcode'] = instruction % 100
    params_to_set_modes = opcode_parameter_number(unpacked_instruction['opcode'])
    if params_to_set_modes > 0:
        unpacked_instruction['p1_mode'] = MODE_POSITION
        if params_to_set_modes > 1:
            unpacked_instruction['p2_mode'] = MODE_POSITION
            if params_to_set_modes > 2:
                unpacked_instruction['p3_mode'] = MODE_POSITION

    if params_to_set_modes > 0:
        mode_details = int((instruction - unpacked_instruction['opcode']) / 100)

        if mode_details > 0:
            p1_mode = mode_details % 10
            if p1_mode == MODE_IMMEDIATE:  # this must exist if we are here
                unpacked_instruction['p1_mode'] = MODE_IMMEDIATE
            elif p1_mode == MODE_RELATIVE:
                unpacked_instruction['p1_mode'] = MODE_RELATIVE

            if mode_details > 9:   # so a two-digit number
                p2_mode = int(((mode_details % 100) - p1_mode) / 10)
                if p2_mode == MODE_IMMEDIATE:  # this must exist if we are here
                    unpacked_instruction['p2_mode'] = MODE_IMMEDIATE
                elif p2_mode == MODE_RELATIVE:
                    unpacked_instruction['p2_mode'] = MODE_RELATIVE

                if mode_details > 99:  # so a three-digit number
                    p3_mode = int((mode_details - (mode_details % 100)) / 100)
                    if p3_mode == MODE_IMMEDIATE:  # this must exist if we are here
                        unpacked_instruction['p3_mode'] = MODE_IMMEDIATE
                    elif p3_mode == MODE_RELATIVE:
                        unpacked_instruction['p3_mode'] = MODE_RELATIVE

    return unpacked_instruction


def opcode_parameter_io(opcode):
    parameter_io = dict()
    if opcode in (OC_ADD, OC_MULTIPLY, OC_LESS_THAN, OC_EQUALS):
        parameter_io['p1'] = 'read'
        parameter_io['p2'] = 'read'
        parameter_io['p3'] = 'write'
    elif opcode in (OC_JUMP_IF_TRUE, OC_JUMP_IF_FALSE):
        parameter_io['p1'] = 'read'
        parameter_io['p2'] = 'read'
    elif opcode in (OC_OUTPUT, OC_ADJUST_REL_BASE):
        parameter_io['p1'] = 'read'
    elif opcode == OC_INPUT:
        parameter_io['p1'] = 'write'
    return parameter_io


def docker_intcode(memory_state_input, inputs=dict(), memory_pointer_start=0, relative_base_start=0,
                   suspend_on_output=False, return_state=False):
    def memory_read(address):
        try:
            return memory_state[address]
        except KeyError:
            memory_state[address] = 0
            return 0

    halted = False
    suspended = False
    next_input = 0
    memory_state = defaultdict(int)
    for k, v in memory_state_input.items():
        memory_state[k] = v
    memory_pointer = memory_pointer_start
    relative_base = relative_base_start
    outputs = list()
    current_instruction = 0

    while not suspended and not halted:
        current_instruction += 1
        instruction = memory_read(memory_pointer)
        params_and_opcode = instruction_modes(instruction)
        opcode = params_and_opcode['opcode']
        number_of_parameters = opcode_parameter_number(opcode)
        param_directions = opcode_parameter_io(opcode)
        write_address = None
        read_1_value = None
        read_2_value = None

        if number_of_parameters > 0:
            if param_directions['p1'] == 'read':
                if params_and_opcode['p1_mode'] == MODE_POSITION:
                    read_1_value = memory_read(memory_read(memory_pointer + 1))
                elif params_and_opcode['p1_mode'] == MODE_IMMEDIATE:
                    read_1_value = memory_read(memory_pointer + 1)
                elif params_and_opcode['p1_mode'] == MODE_RELATIVE:
                    read_1_value = memory_read(memory_read(memory_pointer + 1) + relative_base)
                else:
                    print('UNKNOWN read mode')
                    exit()
            elif param_directions['p1'] == 'write':
                if params_and_opcode['p1_mode'] == MODE_POSITION:
                    write_address = memory_read(memory_pointer + 1)
                elif params_and_opcode['p1_mode'] == MODE_IMMEDIATE:
                    print('Can''t write in immediate mode')
                    exit()
                elif params_and_opcode['p1_mode'] == MODE_RELATIVE:
                    write_address =  memory_read(memory_pointer + 1) + relative_base
                else:
                    print('UNKNOWN write mode')
                    exit()
            else:
                print('UNKNOWN param_directions[p1]')
                exit()

            if number_of_parameters > 1:
                if param_directions['p2'] == 'read':
                    if params_and_opcode['p2_mode'] == MODE_POSITION:
                        read_2_value = memory_read(memory_read(memory_pointer + 2))
                    elif params_and_opcode['p2_mode'] == MODE_IMMEDIATE:
                        read_2_value = memory_read(memory_pointer + 2)
                    elif params_and_opcode['p2_mode'] == MODE_RELATIVE:
                        read_2_value = memory_read(memory_read(memory_pointer + 2) + relative_base)
                    else:
                        print('UNKNOWN read mode')
                        exit()
                elif param_directions['p2'] == 'write':
                    if params_and_opcode['p2_mode'] == MODE_POSITION:
                        write_address = memory_read(memory_pointer + 2)
                    elif params_and_opcode['p2_mode'] == MODE_IMMEDIATE:
                        print('Can''t write in immediate mode')
                        exit()
                    elif params_and_opcode['p2_mode'] == MODE_RELATIVE:
                        write_address = memory_read(memory_pointer + 2) + relative_base
                    else:
                        print('UNKNOWN write mode')
                        exit()
                else:
                    print('UNKNOWN param_directions[p2]')
                    exit()

                if number_of_parameters > 2:
                    if param_directions['p3'] == 'read':
                        print('UNKNOWN read at param 3')
                        exit()
                    elif param_directions['p3'] == 'write':

                        if params_and_opcode['p3_mode'] == MODE_POSITION:
                            write_address = memory_read(memory_pointer + 3)
                        elif params_and_opcode['p3_mode'] == MODE_IMMEDIATE:
                            print('Can''t write in immediate mode')
                            exit()
                        elif params_and_opcode['p3_mode'] == MODE_RELATIVE:
                            write_address = memory_read(memory_pointer + 3) + relative_base
                        else:
                            print('UNKNOWN write mode')
                            exit()

                    else:
                        print('UNKNOWN param_directions[p3]')
                        exit()

        next_memory_pointer = memory_pointer + 1 + number_of_parameters  # may be overwritten by jumps, or ignored by termination
        if opcode == OC_ADD:
            memory_state[write_address] = read_1_value + read_2_value
        elif opcode == OC_MULTIPLY:
            memory_state[write_address] = read_1_value * read_2_value
        elif opcode == OC_INPUT:
            memory_state[write_address] = inputs[next_input]
            next_input += 1
        elif opcode == OC_OUTPUT:
            outputs.append(read_1_value)
            if suspend_on_output:
                suspended = True
        elif opcode == OC_JUMP_IF_TRUE:
            if read_1_value != 0:
                next_memory_pointer = read_2_value
        elif opcode == OC_JUMP_IF_FALSE:
            if read_1_value == 0:
                next_memory_pointer = read_2_value
        elif opcode == OC_LESS_THAN:
            if read_1_value < read_2_value:
                memory_state[write_address] = 1
            else:
                memory_state[write_address] = 0
        elif opcode == OC_EQUALS:
            if read_1_value == read_2_value:
                memory_state[write_address] = 1
            else:
                memory_state[write_address] = 0
        elif opcode == OC_ADJUST_REL_BASE:
            relative_base += read_1_value
        elif opcode == OC_TERMINATE:
            continue_processing = False
            halted = True
        else:
            print('ERROR')
        memory_pointer = next_memory_pointer

    # build return dict
    end_state = dict()
    if halted:
        end_state['halted'] = True
    else:
        end_state['halted'] = False
    if suspend_on_output:
        end_state['current_instruction'] = current_instruction
        end_state['output'] = outputs[0]
    else:
        end_state['outputs'] = outputs
    if return_state:
        end_state['memory'] = memory_state.copy()
        end_state['memory_pointer'] = memory_pointer
        end_state['relative_base'] = relative_base
    return end_state


def main():
    with open(SOURCE_FILE) as f:
        code = {key: (int(this_string)) for key, this_string in enumerate(f.readline().split(','))}
    code[0] = 2  # steal this game

    (memory_state_input, inputs=dict(), memory_pointer_start = 0, relative_base_start = 0,
     suspend_on_output = False, return_state = False):


    i = 0
    while True:
        i += 1
        returned_state = docker_intcode(code, {0: 0},  )  # , suspend_on_output=True, return_state=True)
        paddle_x_position = None
        ball_x_position = None
        for this_output in returned_state['outputs']:
            # find the score, move the paddle
            if i % 1 == 0 and this_output == 2:

            else:
                continue

    print(str(block_tile) + ' block tiles.')


if __name__ == "__main__":
    main()
