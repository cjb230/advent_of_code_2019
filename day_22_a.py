SOURCE_FILE = 'day_22_input.txt'


DECK_SIZE = 10007
DECK = dict()


def deal_w_increment(increment):
    global DECK
    new_deck = dict()
    for position, value in DECK.items():
        new_position = (position * increment) % DECK_SIZE
        new_deck[new_position] = value
    DECK = new_deck


def deal_new_stack():
    global DECK
    new_deck = dict()
    for position, value in DECK.items():
        new_deck[DECK_SIZE - position - 1] = value
    DECK = new_deck


def deal_cut(cut_position):
    global DECK
    global DECK_SIZE
    new_deck = dict()
    for position, value in DECK.items():
        new_position = position - cut_position
        if new_position < 0:
            new_position += DECK_SIZE
        elif new_position > (DECK_SIZE - 1):
            new_position -= DECK_SIZE
        new_deck[new_position] = value
    DECK = new_deck


def main():
    with open(SOURCE_FILE) as f:
        deals = f.readlines()

    for i in range(DECK_SIZE):
        DECK[i] = i

    for deal in deals:
        deal = deal.strip()
        if deal[0:3] == 'cut':
            deal_cut(int(deal[4:]))
        elif deal[0:19] == 'deal with increment':
            deal_w_increment(int(deal[20:]))
        elif deal == 'deal into new stack':
            deal_new_stack()
        else:
            print('  --' + deal[0:4] + '--')
            exit()

    for position, value in DECK.items():
        if value == 2019:
            print(position)


if __name__ == "__main__":
    main()
