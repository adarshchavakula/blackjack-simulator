import numpy as np
import pandas as pd

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


class BasicStrategy:
    def __init__(self):
        # 0: stand
        # 1: hit
        # 2: double
        self.action = {0: 'stand', 1: 'hit', 2: 'double'}

        # Hard Totals
        basic_hard = pd.DataFrame(
            np.zeros((18, 10), int), 
            index=range(4,22), columns=range(2,12))
        basic_hard.loc[4:10,:] = 1
        basic_hard.loc[9, 3:6] = 2
        basic_hard.loc[10, 2:9] = 2
        basic_hard.loc[11, :] = 2
        basic_hard.loc[12, 2:3] = 1
        basic_hard.loc[12:16, 7:11] = 1
        self.hard = {(x,y): basic_hard.at[x,y] for x in basic_hard.index for y in list(basic_hard)}
        
        # Soft Totals
        basic_soft = pd.DataFrame(
            np.zeros((9, 10), int), 
            index=range(13,22), columns=range(2,12))
        basic_soft.loc[13:18, :] = 1
        basic_soft.loc[13:18, 5:6] = 2
        basic_soft.loc[15:18, 4] = 2
        basic_soft.loc[17:18, 3] = 2
        basic_soft.loc[18, 2] = 2
        basic_soft.loc[18, 7:8] = 0
        basic_soft.loc[19, 6] = 2
        self.soft = {(x,y): basic_soft.at[x,y] for x in basic_soft.index for y in list(basic_soft)}

        # Pair Splits
        basic_split = pd.DataFrame(
            np.zeros((10, 10), int), 
            index=range(2,12), columns=range(2,12))
        basic_split.loc[[8, 11], :] = 1
        basic_split.loc[2:3, 2:7] = 1
        basic_split.loc[4, 5:6] = 1
        basic_split.loc[6, 2:6] = 1
        basic_split.loc[7, 2:7] = 1
        basic_split.loc[9, 2:9] = 1
        basic_split.loc[9, 7] = 0
        self.split = {(x,y): basic_split.at[x,y] for x in basic_split.index for y in list(basic_split)}
        return

    def __call__(self, hand, dealer_up):
        if len(hand) == 2 and hand[0] == hand[1]:
            if self.split[(values[hand[0]], dealer_up)]:
                return 'split'
        hand_value = evaluate_hand(hand)
        if hand_value[0] > 21:
            return 'bust'
        if hand_value[1] == 'soft':
            return self.action[self.soft[(hand_value[0], dealer_up)]]
        if hand_value[1] == 'hard':
            return self.action[self.hard[(hand_value[0], dealer_up)]]
            

