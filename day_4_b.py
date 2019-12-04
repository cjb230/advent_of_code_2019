PWD_MIN = 156218
PWD_MAX = 652527


def has_two_adjacent_same(test_password):
    result = False
    test_string = str(test_password)
    if test_string[0] == test_string[1] or test_string[1] == test_string[2] or test_string[2] == test_string[3] or test_string[3] == test_string[4] or test_string[4] == test_string[5]:
        result = True
    return result


def never_decreases(test_password):
    result = True
    test_string = str(test_password)
    if test_string[0] > test_string[1] or test_string[1] > test_string[2] or test_string[2] > test_string[3] or test_string[3] > test_string[4] or test_string[4] > test_string[5]:
        result = False
    return result


def has_a_pair(test_password):
    test_string = str(test_password)
    if ((test_string[0] == test_string[1] and test_string[1] != test_string[2]) or
        (test_string[1] == test_string[2] and test_string[1] != test_string[0] and test_string[1] != test_string[3]) or
        (test_string[2] == test_string[3] and test_string[1] != test_string[2] and test_string[3] != test_string[4]) or
        (test_string[3] == test_string[4] and test_string[2] != test_string[3] and test_string[4] != test_string[5]) or
        (test_string[4] == test_string[5] and test_string[4] != test_string[3])):
        return True
    return False


def main():
    global PWD_MIN
    global PWD_MAX
    criteria_valid = 0
    for i in range (PWD_MIN, PWD_MAX + 1):
        if has_two_adjacent_same(i) and never_decreases(i) and has_a_pair(i):
            criteria_valid += 1
    print(criteria_valid)


if __name__ == "__main__":
    main()
