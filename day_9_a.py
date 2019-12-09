import itertools

SOURCE_FILE = 'day_9_input.txt'

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
        mode_details = (instruction - unpacked_instruction['opcode']) / 100

        if mode_details > 0:
            mode_string = str(mode_details)

            if mode_string[-1] == MODE_IMMEDIATE:  # this must exist if we are here
                unpacked_instruction['p1_mode'] = MODE_IMMEDIATE
            elif mode_string[-1] == MODE_RELATIVE:
                unpacked_instruction['p1_mode'] = MODE_RELATIVE

            if len(mode_string) > 1:
                if mode_string[-2] == MODE_IMMEDIATE:  # this must exist if we are here
                    unpacked_instruction['p2_mode'] = MODE_IMMEDIATE
                elif mode_string[-2] == MODE_RELATIVE:
                    unpacked_instruction['p2_mode'] = MODE_RELATIVE

    return unpacked_instruction


def docker_intcode(memory_state_input, inputs, memory_pointer_start = 0, relative_base_start = 0,
                   suspend_on_output = False, return_state = False):
    halted = False
    suspended = False
    next_input = 0
    memory_state = memory_state_input.copy()
    memory_pointer = memory_pointer_start
    relative_base = relative_base_start
    outputs = list()

    while not suspended and not halted:
        this_instruction = memory_state[memory_pointer:memory_pointer+4]
        params_and_opcode = instruction_modes(this_instruction[0])
        opcode = params_and_opcode['opcode']
        number_of_parameters = opcode_parameter_number(opcode)

        if number_of_parameters > 0:
            if params_and_opcode['p1_mode'] == MODE_POSITION:
                try:
                    param_1 = memory_state[this_instruction[1]]
                except IndexError:
                    print('Tried to access mem location ' + str(this_instruction[1]))
                    exit()
            elif params_and_opcode['p1_mode'] == MODE_IMMEDIATE:
                param_1 = this_instruction[1]
            elif params_and_opcode['p1_mode'] == MODE_RELATIVE:
                param_1 = memory_state[this_instruction[1] + relative_base]
            else:
                param_1 = 'UNKNOWN'

            if number_of_parameters > 1:
                if params_and_opcode['p2_mode'] == 'position':
                    param_2 = memory_state[this_instruction[2]]
                elif params_and_opcode['p2_mode'] == 'immediate':
                    param_2 = this_instruction[2]
                elif params_and_opcode['p2_mode'] == MODE_RELATIVE:
                    param_2 = memory_state[this_instruction[2] + relative_base]
                else:
                    param_2 = 'UNKNOWN'

        memory_pointer += 1 + opcode_parameter_number(opcode)  # may be overwritten by jumps, or ignored by termination
        if opcode == OC_ADD:
            memory_state[this_instruction[3]] = param_1 + param_2
        elif opcode == OC_MULTIPLY:
            memory_state[this_instruction[3]] = param_1 * param_2
        elif opcode == OC_INPUT:
            memory_state[this_instruction[1]] = inputs[next_input]
            next_input += 1
        elif opcode == OC_OUTPUT:
            outputs.append(param_1)
            if suspend_on_output:
                suspended = True
        elif opcode == OC_JUMP_IF_TRUE:
            if param_1 != 0:
                memory_pointer = param_2
        elif opcode == OC_JUMP_IF_FALSE:
            if param_1 == 0:
                memory_pointer = param_2
        elif opcode == OC_LESS_THAN:
            if param_1 < param_2:
                memory_state[this_instruction[3]] = 1
            else:
                memory_state[this_instruction[3]] = 0
        elif opcode == OC_EQUALS:
            if param_1 == param_2:
                memory_state[this_instruction[3]] = 1
            else:
                memory_state[this_instruction[3]] = 0
        elif opcode == OC_ADJUST_REL_BASE:
            relative_base += param_1
        elif opcode == OC_TERMINATE:
            continue_processing = False
            halted = True
        else:
            print('ERROR')

    # build return dict
    end_state = dict()
    if halted:
        end_state['halted'] = True
    else:
        end_state['halted'] = False
    if suspend_on_output:
        end_state['output'] = outputs[0]
    else:
        end_state['outputs'] = outputs
    if return_state:
        end_state['memory'] = memory_state.copy()
        end_state['memory_pointer'] = memory_pointer
        end_state['relative_base'] = relative_base
    return end_state


def main():
    code = dict()
    with open(SOURCE_FILE) as f:
        code = {key: (int(this_string)) for key, this_string in enumerate(f.readline().split(','))}
    print(str(code))

    inputs = dict()
    inputs[0] = 1
    returned_state = docker_intcode(code, inputs)
    print(str(returned_state))


if __name__ == "__main__":
    main()
