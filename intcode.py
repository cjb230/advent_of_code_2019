import functools

class IntcodeComputer:
    OP_ADD = 1
    OP_MULTIPLY = 2
    OP_INPUT = 3
    OP_OUTPUT = 4
    OP_JUMP_IF_TRUE = 5
    OP_JUMP_IF_FALSE = 6
    OP_LESS_THAN = 7
    OP_EQUALS = 8
    OP_ADJ_REL_BASE = 9
    OP_HALT = 99
    MODE_POSITION = 0
    MODE_IMMEDIATE = 1
    MODE_RELATIVE = 2

    def __init__(self, program, inputs_list=None):
        #_validate_memory_input(program)
        self.memory = program
        self.next_instruction = 0
        self.is_halted = False
        self.relative_base = 0
        self.print_output = False
        self.store_output = False
        self.execution_counter = 0
        self.inputs_list = inputs_list
        self.outputs_list = list()
        self.input_starved = False

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _opcode_parameter_slots(opcode: int) -> int:
        if opcode in (IntcodeComputer.OP_ADD, IntcodeComputer.OP_MULTIPLY, IntcodeComputer.OP_LESS_THAN, IntcodeComputer.OP_EQUALS):
            return 3
        elif opcode in (IntcodeComputer.OP_JUMP_IF_TRUE, IntcodeComputer.OP_JUMP_IF_FALSE):
            return 2
        elif opcode in (IntcodeComputer.OP_OUTPUT, IntcodeComputer.OP_INPUT, IntcodeComputer.OP_ADJ_REL_BASE):
            return 1
        elif opcode == IntcodeComputer.OP_HALT:
            return 0
        else:
            print('Unknown opcode ' + str(opcode))
            exit()

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _opcode_input_parameter_slots(opcode: int) -> int:
        if opcode in (IntcodeComputer.OP_ADD, IntcodeComputer.OP_MULTIPLY, IntcodeComputer.OP_LESS_THAN, IntcodeComputer.OP_EQUALS, IntcodeComputer.OP_JUMP_IF_TRUE, IntcodeComputer.OP_JUMP_IF_FALSE):
            return 2
        elif opcode in (IntcodeComputer.OP_OUTPUT, IntcodeComputer.OP_ADJ_REL_BASE):
            return 1
        elif opcode in (IntcodeComputer.OP_INPUT, IntcodeComputer.OP_HALT):
            return 0
        else:
            print('Unknown input parameter slots for opcode ' + str(opcode))
            exit()

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _opcode_output_parameter_slots(opcode: int) -> int:
        """
        The number of parameters which are outputs for this instruction.

        "Parameters that an instruction writes to will never be in immediate mode."
        (https://adventofcode.com/2019/day/5)

        :param opcode: The instruction to give number of output parameters for.
        :return: 
        """
        if opcode in (IntcodeComputer.OP_ADD, IntcodeComputer.OP_MULTIPLY, IntcodeComputer.OP_LESS_THAN, IntcodeComputer.OP_EQUALS, IntcodeComputer.OP_INPUT):
            return 1
        elif opcode in (IntcodeComputer.OP_OUTPUT, IntcodeComputer.OP_JUMP_IF_TRUE, IntcodeComputer.OP_JUMP_IF_FALSE, IntcodeComputer.OP_ADJ_REL_BASE, IntcodeComputer.OP_HALT):
            return 0
        else:
            print('Unknown output parameter slots for opcode ' + str(opcode))
            exit()

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _decode_instruction_modes(instruction_code: int):
        """
        Separate a full instruction code into an operation ("opcode") and modes for the parameters.

        :param instruction_code:
        :return: A dict containing the opcode and as many parameter modes as the opcode dictates
        """
        opcode = instruction_code % 100
        decoded_instruction = {"opcode": opcode}
        param_slots = IntcodeComputer._opcode_parameter_slots(opcode)
        parameter_mode_map = int((instruction_code - opcode) / 100)
        if param_slots > 0:
            decoded_instruction["param_1_mode"] = parameter_mode_map % 10
            parameter_mode_map = int((parameter_mode_map - decoded_instruction["param_1_mode"]) / 10)
        if param_slots > 1:
            decoded_instruction["param_2_mode"] = parameter_mode_map % 10
            parameter_mode_map = int((parameter_mode_map - decoded_instruction["param_2_mode"]) / 10)
        if param_slots > 2:
            decoded_instruction["param_3_mode"] = parameter_mode_map % 10
        return decoded_instruction

    def _read_memory(self, location):
        if location < 0 or not isinstance(location, int):
            print('Location must be a positive integer')
            exit()
        try:
            ans = self.memory[location]
        except KeyError:
            self.memory[location] = 0
            ans = 0
        return ans

    def _decode_input(self, input_mode, input_value):
        """
        Converts an input value and a mode into an absolute value.

        :param input_mode:
        :param input_value:
        :return: The decoded input value to use in the instruction
        """
        if input_mode == IntcodeComputer.MODE_IMMEDIATE:
            operation_input_value = self.memory[input_value]
        elif input_mode == IntcodeComputer.MODE_POSITION:
            operation_input_value = self._read_memory(self._read_memory(input_value))
        elif input_mode == IntcodeComputer.MODE_RELATIVE:
            operation_input_value = self._read_memory(self._read_memory(input_value) +self.relative_base)
        else:
            print("Couldn't decode input with mode = " + str(input_mode))
            exit()
        return operation_input_value

    def _decode_output(self, output_mode, output_value):
        """
        Converts an output value and a mode into an absolute memory address.

        :param output_mode:
        :param output_value:
        :return: The decoded memory address into which to write the output
        """
        if output_mode == IntcodeComputer.MODE_IMMEDIATE:
            print("Outputs can never be in immediate mode, and yet here we are.")
            exit()
        elif output_mode == IntcodeComputer.MODE_POSITION:
            operation_output_address = self._read_memory(output_value)
        elif output_mode == IntcodeComputer.MODE_RELATIVE:
            operation_output_address = self._read_memory(output_value) + self.relative_base
        else:
            print("Couldn't decode output with mode = " + str(output_mode))
            exit()
        return operation_output_address

    def _decode_params(self, decoded_instruction, parameter_starting_address):
        """
        Converts a map of input and output modes into real values.
        :param decoded_instructions:
        :param parameter_starting_address:
        :return: Dict with directly usable input values and the address for the output
        """
        decoded_params = dict()
        opcode = decoded_instruction["opcode"]
        param_slots = IntcodeComputer._opcode_parameter_slots(opcode)
        num_inputs = IntcodeComputer._opcode_input_parameter_slots(opcode)
        num_outputs = IntcodeComputer._opcode_output_parameter_slots(opcode)
        if num_outputs + num_inputs != param_slots:
            print('Input / output slot mismatch for opcode = ' + str(opcode))
            exit()
        if num_inputs > 0:
            decoded_params["input_1"] = self._decode_input(decoded_instruction["param_1_mode"], parameter_starting_address)
        if num_inputs > 1:
            decoded_params["input_2"] = self._decode_input(decoded_instruction["param_2_mode"], parameter_starting_address + 1)
        if num_outputs > 0:
            output_param_mode_desc = "param_" + str(param_slots) + "_mode"
            decoded_params["output_address"] = self._decode_output(decoded_instruction[output_param_mode_desc], parameter_starting_address + num_inputs)
        return decoded_params

    def _add(self, input1, input2, output_address):
        self.memory[output_address] = input1 + input2
        self.next_instruction += 4

    def _multiply(self,input1, input2, output_address):
        self.memory[output_address] = input1 * input2
        self.next_instruction += 4

    def _input(self, input_value, output_address):
        self.memory[output_address] = input_value
        self.next_instruction += 2

    def _output(self, input1):
        if self.print_output:
            print(input1)
        self.outputs_list.append(input1)
        self.next_instruction += 2

    def _jump_if_true(self, input1, input2):
        if input1:
            self.next_instruction = input2
        else:
            self.next_instruction += 3

    def _jump_if_false(self, input1, input2):
        if input1 == 0:
            self.next_instruction = input2
        else:
            self.next_instruction += 3

    def _less_than(self, input1, input2, output_address):
        if input1 < input2:
            self.memory[output_address] = 1
        else:
            self.memory[output_address] = 0
        self.next_instruction += 4

    def _equals(self, input1, input2, output_address):
        if input1 == input2:
            self.memory[output_address] = 1
        else:
            self.memory[output_address] = 0
        self.next_instruction += 4

    def _adjust_relative_base(self, input1):
        self.relative_base += input1
        self.next_instruction += 2

    def _halt(self):
        self.is_halted = True

    def _process_instruction(self, instruction_address):
        self.execution_counter += 1
        instruction = self.memory[instruction_address]
        #print(self.execution_counter, instruction_address, instruction)
        #if self.execution_counter > 100:
        #    exit()
        decoded_instruction_modes = self._decode_instruction_modes(instruction)
        decoded_params = self._decode_params(decoded_instruction_modes, instruction_address + 1)
        if decoded_instruction_modes["opcode"] == self.OP_ADD:
            self._add(decoded_params["input_1"], decoded_params["input_2"], decoded_params["output_address"])
        elif decoded_instruction_modes["opcode"] == self.OP_MULTIPLY:
            self._multiply(decoded_params["input_1"], decoded_params["input_2"], decoded_params["output_address"])
        elif decoded_instruction_modes["opcode"] == self.OP_INPUT:
            if len(self.inputs_list) > 0:
                self._input(self.inputs_list.pop(), decoded_params["output_address"])
            else:
                self.input_starved = True
                self.execution_counter -= 1
        elif decoded_instruction_modes["opcode"] == self.OP_OUTPUT:
            self._output(decoded_params["input_1"])
        elif decoded_instruction_modes["opcode"] == self.OP_JUMP_IF_TRUE:
            self._jump_if_true(decoded_params["input_1"], decoded_params["input_2"])
        elif decoded_instruction_modes["opcode"] == self.OP_JUMP_IF_FALSE:
            self._jump_if_false(decoded_params["input_1"], decoded_params["input_2"])
        elif decoded_instruction_modes["opcode"] == self.OP_LESS_THAN:
            self._less_than(decoded_params["input_1"], decoded_params["input_2"], decoded_params["output_address"])
        elif decoded_instruction_modes["opcode"] == self.OP_EQUALS:
            self._equals(decoded_params["input_1"], decoded_params["input_2"], decoded_params["output_address"])
        elif decoded_instruction_modes["opcode"] == self.OP_ADJ_REL_BASE:
            self._adjust_relative_base(decoded_params["input_1"])
        elif decoded_instruction_modes["opcode"] == self.OP_HALT:
            self._halt()
        else:
            print('Unknown instruction ' + decoded_instruction_modes["opcode"] + ' in __process_instruction')

    def run_to_halt(self, new_inputs=None, return_output=True, return_memory=False, print_output=False):
        self.outputs_list = list()
        if new_inputs:
            self.inputs_list = new_inputs
            self.input_starved = False
        if print_output:
            self.print_output = True
        while not (self.is_halted or self.input_starved):
            self._process_instruction(self.next_instruction)
        results = dict()
        if return_output:
            results['output'] = self.outputs_list
        if return_memory:
            results['memory'] = self.memory
        if len(results) > 0:
            return results
        else:
            return
