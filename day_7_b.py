import itertools
import math
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
        #print('STEP ' + str(step))
        #print('Memory pointer =  ' + str(memory_pointer))
        #print('Instructions = ' + str(this_instruction))
        params_and_opcode = unpack_instruction(this_instruction[0])
        opcode = params_and_opcode['opcode']
        #print('Unpacked instruction = ' + str(params_and_opcode))

        if opcode != 99:
            if params_and_opcode['p1_mode'] == 'position':
                param_1 = amp_memory[this_instruction[1]]
            elif params_and_opcode['p1_mode'] == 'immediate':
                param_1 = this_instruction[1]
            else:
                param_1 = 'UNKNOWN'

            if opcode in (1, 2, 5, 6, 7, 8): # opcodes that take three or more parameters
                if params_and_opcode['p2_mode'] == 'position':
                    param_2 = amp_memory[this_instruction[2]]
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
            amp_memory[this_instruction[3]] = param_1 + param_2
            memory_pointer += 4
        elif opcode == 2:
            amp_memory[this_instruction[3]] = param_1 * param_2
            memory_pointer += 4
        elif opcode == 3:
            amp_memory[this_instruction[1]] = inputs[next_input]
            next_input += 1
            memory_pointer += 2
        elif opcode == 4:
            memory_pointer += 2
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
                amp_memory[this_instruction[3]] = 1
            else:
                amp_memory[this_instruction[3]] = 0
            memory_pointer += 4
        elif opcode == 8:
            if param_1 == param_2:
                amp_memory[this_instruction[3]] = 1
            else:
                amp_memory[this_instruction[3]] = 0
            memory_pointer += 4
        elif opcode == 99:
            continue_processing = False
            HALTED = True
        else:
            print('ERROR')

    #print('WHY AM I HERE?  (vm = ' + vm + ', inputs = ' + str(inputs) + ')')
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
            #print('COMBINATION = ' + str(combination) + ', step = ' + str(steps), ', last VM = ' + str(this_vm) +
            #      ', last VM output = ' + str(last_output))
            this_vm = next_vm(this_vm)
            this_amplifier_inputs = [last_output]
            x = docker_intcode(this_vm, this_amplifier_inputs)
            if x:
                last_output = x
            steps += 1

        #print('Last VM output = ' + str(last_output))
        #if max_output:
        #    print('Max output = ' + str(max_output))
        if max_output is None or last_output > max_output:
            max_output = last_output

        #if max_output:
        #    print('Max output now = ' + str(max_output))

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

