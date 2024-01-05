import sys
import functools
from dataclasses import dataclass
from enum import IntEnum
from math import sqrt, ceil, floor


CARDS = {
    'A': 14, 
    'K': 13, 
    'Q': 12, 
    'J': 11, 
    'T': 10, 
    '9': 9, 
    '8': 8, 
    '7': 7, 
    '6': 6, 
    '5': 5, 
    '4': 4, 
    '3': 3,
    '2': 2,
    '1': 1
}

class Value(IntEnum):
    FIVE = 10
    FOUR = 9
    FULL = 4
    THREE = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0

@dataclass
class Play:
    cards: str
    bid: int

    def _aggrCards(self):
        grr = {}
        for card in self.cards:
            if card in grr:
                grr[card] += 1
            else:
                grr[card] = 1
        return grr
    
    def _aggrToValue(self, values: list[str]):
        values = list(reversed(sorted(values)))
        if len(values) == 5:
            return Value.HIGH_CARD
        if len(values) == 1:
            return Value.FIVE
        if values[0] == 4:
            return Value.FOUR
        if values[0] == 3:
            if values[1] == 2:
                return Value.FULL
            else:
                return Value.THREE
        if values[0] == 2:
            if values[1] == 2:
                return Value.TWO_PAIR
            else:
                return Value.ONE_PAIR
        print(values)
        raise Exception('Unexpected outcome')

    def getValue(self):
        grr = self._aggrCards()
        values = []
        for k in grr:
            values.append(grr[k])
        return self._aggrToValue(values)
    
    def cardValue(self, card):
        return CARDS[card]

    def __lt__(self, obj): 
        if self.getValue() != obj.getValue():
            return self.getValue() < obj.getValue()
        for i in range(0, len(self.cards)):
            if self.cards[i] != obj.cards[i]:
                return self.cardValue(self.cards[i]) < self.cardValue(obj.cards[i])
        return False
    
    # Hint:
    # __eq__ defined by dataclass


class PlayJokers(Play):
    def __init__(self, play: Play):
        super().__init__(play.cards, play.bid)


    def getValue(self):
        grr = self._aggrCards()
        if 'J' in grr:
            topLen = 0
            topChar = '1'
            for k in grr:
                if k == 'J':
                    continue
                if grr[k] > topLen:
                    topChar = k
                    topLen = grr[k]
                elif grr[k] == topLen and self.cardValue(k) > self.cardValue(topChar):
                    topChar = k
            # if all jokers
            if topLen == 0:
                topChar = 'A'
                grr[topChar] = 0
            grr[topChar] += grr['J']
            del grr['J']
        values = []
        for k in grr:
            values.append(grr[k])
        return self._aggrToValue(values)
        
    def cardValue(self, card): 
        if card == 'J':
            return 0
        else:
            return super().cardValue(card)
    

@dataclass
class Input:
    plays: list[Play]

def parsePlay(play) -> Play:
    parts = play.split()
    bid = int(parts[1])
    cards = parts[0]
    return Play(cards, bid)

def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = f.readlines()
        plays = [parsePlay(line.strip()) for line in lines]
        return Input(plays)

def firstTask(input):
    plays = input.plays
    ordered = sorted(plays)
    result = 0
    #print(ordered)
    for v, play in enumerate(ordered):
        result += (v + 1) * play.bid
    return result


def secondTask(input):
    plays = [PlayJokers(play) for play in input.plays]
    ordered = sorted(plays)
    result = 0
    #print(ordered)
    for v, play in enumerate(ordered):
        result += (v + 1) * play.bid
    return result


if __name__=="__main__":
    input = read()
    print(firstTask(input))
    print(secondTask(input))
