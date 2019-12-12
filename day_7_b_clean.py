import itertools

SOURCE_FILE = 'day_7_input.txt'
AMP_A_MEMORY = list()
AMP_B_MEMORY = list()
AMP_C_MEMORY = list()
AMP_D_MEMORY = list()
AMP_E_MEMORY = list()
MEM_POINTER_A = 0
MEM_POINTER_B = 0
MEM_POINTER_C = 0
MEM_POINTER_D = 0
MEM_POINTER_E = 0
HALTED = False

OC_ADD = 1
OC_MULTIPLY = 2
OC_INPUT = 3
OC_OUTPUT = 4
OC_JUMP_IF_TRUE = 5
OC_JUMP_IF_FALSE = 6
OC_LESS_THAN = 7
OC_EQUALS = 8
OC_TERMINATE = 99

MODE_POSITION = 0
MODE_IMMEDIATE = 1


def opcode_parameter_number(opcode):
    parameter_number = None
    if opcode in (OC_ADD, OC_MULTIPLY, OC_LESS_THAN, OC_EQUALS):
        parameter_number = 3
    elif opcode in (OC_JUMP_IF_TRUE, OC_JUMP_IF_FALSE):
        parameter_number = 2
    elif opcode in (OC_INPUT, OC_OUTPUT):
        parameter_number = 1
    elif opcode == OC_TERMINATE:
        parameter_number = 0
    return parameter_number


def instruction_modes(instruction):
    unpacked_instruction = dict()
    unpacked_instruction['opcode'] = instruction % 100
    params_to_set_modes = opcode_parameter_number(unpacked_instruction['opcode'])
    if params_to_set_modes > 0:
        unpacked_instruction['p1_mode'] = 'position'
    if params_to_set_modes > 1:
        unpacked_instruction['p2_mode'] = 'position'
    if params_to_set_modes > 2:
        unpacked_instruction['p3_mode'] = 'position'

    if params_to_set_modes > 0:
        mode_details = (instruction - unpacked_instruction['opcode']) / 100

        if mode_details > 0:
            mode_string = str(mode_details)

            if mode_string[-1] == MODE_IMMEDIATE:  # this must exist if we are here
                unpacked_instruction['p1_mode'] = 'immediate'

            if len(mode_string) > 1:
                if mode_string[-2] == MODE_IMMEDIATE:  # this must exist if we are here
                    unpacked_instruction['p2_mode'] = 'immediate'

    return unpacked_instruction


def d2ocker_intcode(memory_state_input, inputs, memory_pointer_start = 0, halt_on_output = False, return_state = False):
    memory_state = memory_state_input.copy()
    memory_pointer = memory_pointer_start
    outputs = list()

    # build return dict
    end_state = dict()
    if halt_on_output:
        end_state['output'] = outputs[0]
    else:
        end_state['outputs'] = outputs
    if return_state:
        end_state['memory'] = memory_state.copy()
        end_state['memory_pointer'] = memory_pointer

    return end_state




def docker_intcode(vm, inputs):
    global AMP_A_MEMORY
    global AMP_B_MEMORY
    global AMP_C_MEMORY
    global AMP_D_MEMORY
    global AMP_E_MEMORY
    global MEM_POINTER_A
    global MEM_POINTER_B
    global MEM_POINTER_C
    global MEM_POINTER_D
    global MEM_POINTER_E
    global HALTED

    next_input = 0
    continue_processing = True

    if vm == 'A':
        amp_memory = AMP_A_MEMORY.copy()
        memory_pointer = MEM_POINTER_A
    elif vm == 'B':
        amp_memory = AMP_B_MEMORY.copy()
        memory_pointer = MEM_POINTER_B
    elif vm == 'C':
        amp_memory = AMP_C_MEMORY.copy()
        memory_pointer = MEM_POINTER_C
    elif vm == 'D':
        amp_memory = AMP_D_MEMORY.copy()
        memory_pointer = MEM_POINTER_D
    elif vm == 'E':
        amp_memory = AMP_E_MEMORY.copy()
        memory_pointer = MEM_POINTER_E

    while continue_processing:
        this_instruction = amp_memory[memory_pointer:memory_pointer+4]
        params_and_opcode = instruction_modes(this_instruction[0])
        opcode = params_and_opcode['opcode']
        number_of_parameters = opcode_parameter_number(opcode)

        if number_of_parameters > 0:
            if params_and_opcode['p1_mode'] == 'position':
                param_1 = amp_memory[this_instruction[1]]
            elif params_and_opcode['p1_mode'] == 'immediate':
                param_1 = this_instruction[1]
            else:
                param_1 = 'UNKNOWN'

            if number_of_parameters > 1:
                if params_and_opcode['p2_mode'] == 'position':
                    param_2 = amp_memory[this_instruction[2]]
                elif params_and_opcode['p2_mode'] == 'immediate':
                    param_2 = this_instruction[2]
                else:
                    param_2 = 'UNKNOWN'

        memory_pointer += 1 + opcode_parameter_number(opcode)  # may be overwritten by jumps, or ignored by termination
        if opcode == OC_ADD:
            amp_memory[this_instruction[3]] = param_1 + param_2
        elif opcode == OC_MULTIPLY:
            amp_memory[this_instruction[3]] = param_1 * param_2
        elif opcode == OC_INPUT:
            amp_memory[this_instruction[1]] = inputs[next_input]
            next_input += 1
        elif opcode == OC_OUTPUT:
            if vm == 'A':
                AMP_A_MEMORY = amp_memory.copy()
                MEM_POINTER_A = memory_pointer
            elif vm == 'B':
                AMP_B_MEMORY = amp_memory.copy()
                MEM_POINTER_B = memory_pointer
            elif vm == 'C':
                AMP_C_MEMORY = amp_memory.copy()
                MEM_POINTER_C = memory_pointer
            elif vm == 'D':
                AMP_D_MEMORY = amp_memory.copy()
                MEM_POINTER_D = memory_pointer
            elif vm == 'E':
                AMP_E_MEMORY = amp_memory.copy()
                MEM_POINTER_E = memory_pointer
            return param_1
        elif opcode == OC_JUMP_IF_TRUE:
            if param_1 != 0:
                memory_pointer = param_2
        elif opcode == OC_JUMP_IF_FALSE:
            if param_1 == 0:
                memory_pointer = param_2
        elif opcode == OC_LESS_THAN:
            if param_1 < param_2:
                amp_memory[this_instruction[3]] = 1
            else:
                amp_memory[this_instruction[3]] = 0
        elif opcode == OC_EQUALS:
            if param_1 == param_2:
                amp_memory[this_instruction[3]] = 1
            else:
                amp_memory[this_instruction[3]] = 0
        elif opcode == OC_TERMINATE:
            continue_processing = False
            HALTED = True
        else:
            print('ERROR')

    return


def generate_lexicographic_combinations(range_min, range_max):
    range_list = list(range(range_min, range_max + 1))
    return itertools.permutations(range_list)


def next_vm(this_vm):
    if this_vm == 'A':
        return 'B'
    elif this_vm == 'B':
        return 'C'
    elif this_vm == 'C':
        return 'D'
    elif this_vm == 'D':
        return 'E'
    elif this_vm == 'E':
        return 'A'


def simulate_combinations(program):
    global AMP_A_MEMORY
    global AMP_B_MEMORY
    global AMP_C_MEMORY
    global AMP_D_MEMORY
    global AMP_E_MEMORY
    global MEM_POINTER_A
    global MEM_POINTER_B
    global MEM_POINTER_C
    global MEM_POINTER_D
    global MEM_POINTER_E
    global HALTED

    combinations = generate_lexicographic_combinations(5, 9)
    max_output = None

    for combination in combinations:
        AMP_A_MEMORY = GOLD_COPY.copy()
        AMP_B_MEMORY = GOLD_COPY.copy()
        AMP_C_MEMORY = GOLD_COPY.copy()
        AMP_D_MEMORY = GOLD_COPY.copy()
        AMP_E_MEMORY = GOLD_COPY.copy()
        MEM_POINTER_A = 0
        MEM_POINTER_B = 0
        MEM_POINTER_C = 0
        MEM_POINTER_D = 0
        MEM_POINTER_E = 0

        steps = 6
        HALTED = False
        this_amplifier_inputs = [combination[0], 0]
        this_vm = 'A'
        last_output = docker_intcode(this_vm, this_amplifier_inputs)
        this_vm = next_vm(this_vm)
        this_amplifier_inputs = [combination[1], last_output]
        last_output = docker_intcode(this_vm, this_amplifier_inputs)
        this_vm = next_vm(this_vm)
        this_amplifier_inputs = [combination[2], last_output]
        last_output = docker_intcode(this_vm, this_amplifier_inputs)
        this_vm = next_vm(this_vm)
        this_amplifier_inputs = [combination[3], last_output]
        last_output = docker_intcode(this_vm, this_amplifier_inputs)
        this_vm = next_vm(this_vm)
        this_amplifier_inputs = [combination[4], last_output]
        last_output = docker_intcode(this_vm, this_amplifier_inputs)

        while not HALTED:
            this_vm = next_vm(this_vm)
            this_amplifier_inputs = [last_output]
            x = docker_intcode(this_vm, this_amplifier_inputs)
            if x:
                last_output = x
            steps += 1

        if max_output is None or last_output > max_output:
            max_output = last_output

    return max_output


def main():
    global GOLD_COPY

    with open(SOURCE_FILE) as f:
        amplifier_prog = [int(this_string) for  this_string in f.readline().split(',')]
    GOLD_COPY = amplifier_prog.copy()

    max_output = simulate_combinations(amplifier_prog)
    print('MAX = ' + str(max_output))


if __name__ == "__main__":
    main()
