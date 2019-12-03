ORIGINAL_PROGRAM = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,10,1,19,1,19,9,23,1,23,6,27,2,27,13,31,1,10,31,35,1,10,35,39,2,39,6,43,1,43,
          5,47,2,10,47,51,1,5,51,55,1,55,13,59,1,59,9,63,2,9,63,67,1,6,67,71,1,71,13,75,1,75,10,79,1,5,79,83,1,10,83,87,
          1,5,87,91,1,91,9,95,2,13,95,99,1,5,99,103,2,103,9,107,1,5,107,111,2,111,9,115,1,115,6,119,2,13,119,123,1,123,
          5,127,1,127,9,131,1,131,10,135,1,13,135,139,2,9,139,143,1,5,143,147,1,13,147,151,1,151,2,155,1,10,155,0,99,2,
          14,0,0]


def main():
    global ORIGINAL_PROGRAM
    for noun in range(0, 100):
        for verb in range(0, 100):
            print('Testing noun = ' + str(noun) + ', verb = ' + str(verb) + ' ... ', end = '')
            test_program = ORIGINAL_PROGRAM.copy()
            test_program[1] = noun
            test_program[2] = verb

            memory_pointer = 0
            continue_processing = True
            while continue_processing:
                this_instruction = test_program[memory_pointer:memory_pointer+4]
                if this_instruction[0] == 1:
                    test_program[this_instruction[3]] = test_program[this_instruction[1]] + test_program[this_instruction[2]]
                elif this_instruction[0] == 2:
                    test_program[this_instruction[3]] = test_program[this_instruction[1]] * test_program[this_instruction[2]]
                elif this_instruction[0] == 99:
                    continue_processing = False
                else:
                    print('ERROR, noun = ' + str(noun) + ', verb = ' + str(verb), ' pointer = ' + str(memory_pointer) +
                          ' this_intruction = ' +str(this_instruction))
                memory_pointer += 4
            print('DONE')
            if test_program[0] == 19690720:
                print('Success with noun = ' + str(noun) + ', verb = ' + str(verb))
                exit()


if __name__ == "__main__":
    main()

