import random
from strategy import evaluate_hand, is_dealer_blackjack, dealer_strategy, dumb_stategy

# Global Variables
DECK_COUNT = 1
PLAYER_COUNT = 2
BANKROLL = 100
TABLE_MIN = 10
BET_SIZE = 10
player_strategy = dumb_stategy



def initialize_deck(deck_count=DECK_COUNT, shuffle=True):
    cards = list('23456789JQKA')
    deck = cards * 4 * DECK_COUNT
    if shuffle:
        random.shuffle(deck)
    return deck



def deal_cards(deck, player_count=PLAYER_COUNT):
    player_cards = {x:[deck.pop(), deck.pop()] for x in range(player_count)}
    player_cards['dealer'] = [deck.pop(), deck.pop()]
    return player_cards # new deck state is maintained



def hit(hand: list, deck):
    hand += [deck.pop()]
    return hand



def play_round(deck, player_count):
    player_cards = deal_cards(deck, player_count)
    print('Hands:')
    print(player_cards)
    dealer_up = evaluate_hand([player_cards['dealer'][0]])[0]

    # Dealer Blackjack check
    if is_dealer_blackjack(player_cards):
        outcome = {p:'lose' for p in range(player_count)}
        outcome['dealer'] = 'blackjack'
        return outcome, player_cards
    
    # player moves
    outcome = {}
    for p in range(player_count):
        print("\nPlayer {}".format(p))
        hand = player_cards[p]
        print(hand)

        # Blackjack!
        if evaluate_hand(hand)[0] == 21:
            outcome[p] = 'blackjack'
            print('Blackjack!')
            continue
        # Not Blackjack
        move = player_strategy(hand, dealer_up)
        print(move)
        while move == 'hit':
            hand = hit(hand, deck)
            print(hand)
            move = player_strategy(hand, dealer_up)
            print(move)
        if move == 'bust':
            outcome[p] = 'lose'
        player_cards[p] = hand

    # dealer moves
    print('\nDealer:')
    dealer_hand = player_cards['dealer']
    print(dealer_hand)
    dealer_move = dealer_strategy(dealer_hand)
    print(dealer_move)
    while dealer_move == 'hit':
        dealer_hand = hit(dealer_hand, deck)
        print(dealer_hand)
        dealer_move = dealer_strategy(dealer_hand)
        print(dealer_move)
    player_cards['dealer'] = dealer_hand

    # dealer bust
    if dealer_move == 'bust':
        outcome['dealer'] = 'bust'
        for p in range(player_count):
            outcome[p] = 'win'
        return outcome, player_cards

    # who won?
    dealer_score = evaluate_hand(player_cards['dealer'])[0]
    for p in range(player_count):
        if p in outcome.keys():
            continue
        player_score = evaluate_hand(player_cards[p])[0]
        if player_score == dealer_score:
            outcome[p] = 'push'
        if player_score > dealer_score:
            outcome[p] = 'win'
        if player_score < dealer_score:
            outcome[p] = 'lose'
    
    return outcome, player_cards

def main():
    d = initialize_deck(1, True)
    outcome, hands = play_round(d, 2)
    print('Final Hands:')
    print(hands)
    print('Outcome:')
    print(outcome)


if __name__ == "__main__":
    main()