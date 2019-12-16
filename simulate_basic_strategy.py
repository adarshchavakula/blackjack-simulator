import random
from strategy import evaluate_hand, is_dealer_blackjack, dealer_strategy, BasicStrategy

# Global Variables
DECK_COUNT = 1
PLAYER_COUNT = 2
BANKROLL = 100
TABLE_MIN = 10
BET_SIZE = 10
player_strategy = BasicStrategy()




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


def player_move(players, deck, player_cards, p, dealer_up, player_bets, player_bankrolls, split_flag=0):
    hand = player_cards[p]
    move = player_strategy(hand, dealer_up)
    # Double only before first hit
    if move == 'double' and len(hand) > 2 :
        move = 'hit'
    print(move)

    # Split
    if move == 'split':
        split_flag += 1
        players += [p%10 + split_flag*10] # add new player
        player_cards[p] = hit([hand[0]], deck)
        player_cards[p%10 + split_flag*10] = hit([hand[1]], deck)
        player_bets[p%10 + split_flag*10] = player_bets[p%10]
        player_bankrolls[p%10] -= player_bets[p%10]
        # restart play for new hand - recursion
        return player_move(players, deck, player_cards, p, dealer_up, player_bets, split_flag)


    # Double
    if move == 'double':
        player_bets[p] *= 2
        player_bankrolls[p] -= player_bets[p]
        hand = hit(hand, deck)
        print(hand)
        if evaluate_hand(hand)[0] > 21:
            outcome = 'lose'
            return outcome

    # Hit
    while move == 'hit':
        hand = hit(hand, deck)
        print(hand)
        move = player_strategy(hand, dealer_up)
        print(move)
    player_cards[p] = hand
    if move == 'bust':
        outcome = 'lose'
        return outcome


def play_round(deck, players, player_bets, player_bankrolls):
    player_cards = deal_cards(deck, len(players))
    print('Hands:')
    print(player_cards)
    dealer_up = evaluate_hand([player_cards['dealer'][0]])[0]

    # Dealer Blackjack check
    if is_dealer_blackjack(player_cards):
        outcome = {p:'lose' for p in players}
        outcome['dealer'] = 'blackjack'
        print('Dealer Blackjack!')
        return outcome, player_cards

    outcome = {}
    # Player Blackjack check
    for p in players:
        if evaluate_hand(player_cards[p])[0] == 21:
            outcome[p] = 'blackjack'
            print('Player {} Blackjack!'.format(p))
    
    # player moves
    
    for p in players:
        if p in outcome.keys():
            continue
        print("\nPlayer {}".format(p))
        outcome[p] = player_move(players, deck, player_cards, p, dealer_up, player_bets, player_bankrolls, split_flag=0)
    

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
        for p in players:
            outcome[p] = 'win'
        return outcome, player_cards

    # who won?
    dealer_score = evaluate_hand(player_cards['dealer'])[0]
    for p in players:
        if outcome[p] is not None:
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
    player_count = PLAYER_COUNT
    players = list(range(player_count))
    player_bets = {0:BET_SIZE, 1:BET_SIZE}
    player_bankrolls = {0:BANKROLL, 1:BANKROLL}
    outcome, player_cards = play_round(d, players, player_bets, player_bankrolls)
    print('Final Hands:')
    print(player_cards)
    print('Outcome:')
    print(outcome)
    


if __name__ == "__main__":
    main()