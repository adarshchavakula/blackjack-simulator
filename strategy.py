
# Define card values
cards = list('23456789JQKA')
values = {c : int(c) for c in cards[:8]}
for c in cards[8:]:
    values[c] = 10
values['A'] = 11 



def evaluate_hand(hand:list):
    hand_value = sum([values[x] for x in hand])
    if 'A' in hand and hand_value < 21:
        flavor = 'soft'
    if 'A' in hand and hand_value > 21:
        hand_value -= 10
        flavor = 'hard'
    else:
        flavor = 'hard'
    return hand_value, flavor


def is_dealer_blackjack(player_cards):
    dealer_value = evaluate_hand(player_cards['dealer'])
    return dealer_value[0] == 21


def dealer_strategy(dealer_hand):
    dealer_value = evaluate_hand(dealer_hand)
    if dealer_value[0] > 21:
        return 'bust'
    if dealer_value[0] > 16 and dealer_value[1] == 'hard':
        return 'stand'
    if dealer_value[0] > 17 and dealer_value[1] == 'soft':
        return 'stand'
    return 'hit'


def dumb_stategy(hand, dealer_up):
    hand_value = evaluate_hand(hand)
    if hand_value[0] <= 11:
        return 'hit'
    if (dealer_up >= 7 and hand_value[0] <= 14):
        return 'hit'
    if (dealer_up >= 9 and hand_value[0] <= 16):
        return 'hit'
    if hand_value[0] > 21:
        return 'bust'
    return 'stand'
    
