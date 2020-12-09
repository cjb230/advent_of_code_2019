import intcode as ic
import os


def day_2_unit():
    with open('tests/day_2a_test_1') as f:
        day_2a_test_1_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
        day_2a_test_1_expected_result = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    day_2a_test_1_computer = ic.IntcodeComputer(day_2a_test_1_prog)
    result = day_2a_test_1_computer.run_to_halt(return_memory=True)
    if result == day_2a_test_1_expected_result:
        print('2a1 successful')
    else:
        print('2a1 failed')

    with open('tests/day_2a_test_2') as f:
        day_2a_test_2_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
        day_2a_test_2_expected_result = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    day_2a_test_2_computer = ic.IntcodeComputer(day_2a_test_2_prog)
    result = day_2a_test_2_computer.run_to_halt(return_memory=True)
    if result == day_2a_test_2_expected_result:
        print('2a2 successful')
    else:
        print('2a2 failed')

    with open('tests/day_2a_test_3') as f:
        day_2a_test_3_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
        day_2a_test_3_expected_result = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    day_2a_test_3_computer = ic.IntcodeComputer(day_2a_test_3_prog)
    result = day_2a_test_3_computer.run_to_halt(return_memory=True)
    if result == day_2a_test_3_expected_result:
        print('2a3 successful')
    else:
        print('2a3 failed')

    with open('tests/day_2a_test_4') as f:
        day_2a_test_4_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
        day_2a_test_4_expected_result = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    day_2a_test_4_computer = ic.IntcodeComputer(day_2a_test_4_prog)
    result = day_2a_test_4_computer.run_to_halt(return_memory=True)
    if result == day_2a_test_4_expected_result:
        print('2a4 successful')
    else:
        print('2a4 failed')

    with open('tests/day_2a_test_5') as f:
        day_2a_test_5_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
        day_2a_test_5_expected_result = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    day_2a_test_5_computer = ic.IntcodeComputer(day_2a_test_5_prog)
    result = day_2a_test_5_computer.run_to_halt(return_memory=True)
    if result == day_2a_test_5_expected_result:
        print('2a5 successful')
    else:
        print('2a5 failed')


def day_5_unit():
    with open('tests/day_5b_test_1') as f:
        day_5b_test_1_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    input_list = [8]
    day_5b_test_1a_computer = ic.IntcodeComputer(day_5b_test_1_prog.copy(), input_list)
    result = day_5b_test_1a_computer.run_to_halt(return_output=True)
    if result[0] == 1:
        print('5b1a successful')
    else:
        print('5b1a failed')
    input_list = [7]
    day_5b_test_1b_computer = ic.IntcodeComputer(day_5b_test_1_prog.copy(), input_list)
    result = day_5b_test_1b_computer.run_to_halt(return_output=True)
    if result[0] == 0:
        print('5b1b successful')
    else:
        print('5b1b failed')

    with open('tests/day_5b_test_2') as f:
        day_5b_test_2_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    input_list = [7]
    day_5b_test_2a_computer = ic.IntcodeComputer(day_5b_test_2_prog.copy(), input_list)
    result = day_5b_test_2a_computer.run_to_halt(return_output=True)
    if result[0] == 1:
        print('5b2a successful')
    else:
        print('5b2a failed')
    input_list = [8]
    day_5b_test_2b_computer = ic.IntcodeComputer(day_5b_test_2_prog.copy(), input_list)
    result = day_5b_test_2b_computer.run_to_halt(return_output=True)
    if result[0] == 0:
        print('5b2b successful')
    else:
        print('5b2b failed')

    with open('tests/day_5b_test_3') as f:
        day_5b_test_3_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    input_list = [8]
    day_5b_test_3a_computer = ic.IntcodeComputer(day_5b_test_3_prog.copy(), input_list)
    result = day_5b_test_3a_computer.run_to_halt(return_output=True)
    if result[0] == 1:
        print('5b3a successful')
    else:
        print('5b3a failed')
    input_list = [9]
    day_5b_test_3b_computer = ic.IntcodeComputer(day_5b_test_3_prog.copy(), input_list)
    result = day_5b_test_3b_computer.run_to_halt(return_output=True)
    if result[0] == 0:
        print('5b3b successful')
    else:
        print('5b3b failed')

    with open('tests/day_5b_test_4') as f:
        day_5b_test_4_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    input_list = [7]
    day_5b_test_4a_computer = ic.IntcodeComputer(day_5b_test_4_prog.copy(), input_list)
    result = day_5b_test_4a_computer.run_to_halt(return_output=True)
    if result[0] == 1:
        print('5b4a successful')
    else:
        print('5b4a failed')
    input_list = [9]
    day_5b_test_4b_computer = ic.IntcodeComputer(day_5b_test_4_prog.copy(), input_list)
    result = day_5b_test_4b_computer.run_to_halt(return_output=True)
    if result[0] == 0:
        print('5b4b successful')
    else:
        print('5b4b failed')

    with open('tests/day_5b_test_5') as f:
        day_5b_test_5_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    input_list = [0]
    day_5b_test_5a_computer = ic.IntcodeComputer(day_5b_test_5_prog.copy(), input_list)
    result = day_5b_test_5a_computer.run_to_halt(return_output=True)
    if result[0] == 0:
        print('5b5a successful')
    else:
        print('5b5a failed')
    input_list = [9]
    day_5b_test_5b_computer = ic.IntcodeComputer(day_5b_test_5_prog.copy(), input_list)
    result = day_5b_test_5b_computer.run_to_halt(return_output=True)
    if result[0] == 1:
        print('5b5b successful')
    else:
        print('5b5b failed')

    with open('tests/day_5b_test_6') as f:
        day_5b_test_6_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    input_list = [0]
    day_5b_test_6a_computer = ic.IntcodeComputer(day_5b_test_6_prog.copy(), input_list)
    result = day_5b_test_6a_computer.run_to_halt(return_output=True)
    if result[0] == 0:
        print('5b6a successful')
    else:
        print('5b6a failed')
    input_list = [9]
    day_5b_test_6b_computer = ic.IntcodeComputer(day_5b_test_6_prog.copy(), input_list)
    result = day_5b_test_6b_computer.run_to_halt(return_output=True)
    if result[0] == 1:
        print('5b6b successful')
    else:
        print('5b6b failed')

    with open('tests/day_5b_test_7') as f:
        day_5b_test_7_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    input_list = [7]
    day_5b_test_7a_computer = ic.IntcodeComputer(day_5b_test_7_prog.copy(), input_list)
    result = day_5b_test_7a_computer.run_to_halt(return_output=True)
    if result[0] == 999:
        print('5b7a successful')
    else:
        print('5b7a failed')
    input_list = [8]
    day_5b_test_7b_computer = ic.IntcodeComputer(day_5b_test_7_prog.copy(), input_list)
    result = day_5b_test_7b_computer.run_to_halt(return_output=True)
    if result[0] == 1000:
        print('5b7b successful')
    else:
        print('5b7b failed')
    input_list = [9]
    day_5b_test_7c_computer = ic.IntcodeComputer(day_5b_test_7_prog.copy(), input_list)
    result = day_5b_test_7c_computer.run_to_halt(return_output=True)
    if result[0] == 1001:
        print('5b7c successful')
    else:
        print('5b7c failed')


def day_9_unit():
    with open('tests/day_9a_test_1') as f:
        day_9a_test_1_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    day_9a_test_1_computer = ic.IntcodeComputer(day_9a_test_1_prog.copy())
    initial_values = list(day_9a_test_1_prog.values())
    result = day_9a_test_1_computer.run_to_halt(return_output=True)
    if result == initial_values:
        print('9a1 successful')
    else:
        print('9a1 failed')

    with open('tests/day_9a_test_2') as f:
        day_9a_test_2_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    day_9a_test_2_computer = ic.IntcodeComputer(day_9a_test_2_prog)
    result = day_9a_test_2_computer.run_to_halt(return_output=True)
    if result[0] == 1219070632396864:
        print('9a2 successful')
    else:
        print('9a2 failed')

    with open('tests/day_9a_test_3') as f:
        day_9a_test_3_prog = {x: int(this_string) for x, this_string in enumerate(f.readline().split(','))}
    day_9a_test_3_computer = ic.IntcodeComputer(day_9a_test_3_prog)
    result = day_9a_test_3_computer.run_to_halt(return_output=True)
    if result[0] == 1125899906842624:
        print('9a3 successful')
    else:
        print('9a3 failed')



def main():
    day_2_unit()
    day_5_unit()
    day_9_unit()
    exit()


if __name__ == "__main__":
    #print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))
    print(os.getcwd())
    main()
