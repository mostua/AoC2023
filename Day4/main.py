import sys
import functools
from dataclasses import dataclass
 
def isSymbol(char):
    return not char.isdigit() and '.' != char

@dataclass
class Card:
    no: int
    winning: list[int]
    have: list[int]

    def countWin(self):
        matching = 0
        winning = set(self.winning)
        for h in self.have:
            if h in winning:
                matching += 1
        return matching

def parseNumbers(numStr):
    print(numStr)
    return [int(x.strip()) for x in numStr.split()]

def parseCard(line):
    cardParts = line.split(": ")
    numberParts = cardParts[1].split(" | ")
    no = int(cardParts[0][5:])
    have = parseNumbers(numberParts[0])
    winning = parseNumbers(numberParts[1])
    return Card(no, winning, have)

def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = f.readlines()
        cards = [parseCard(line) for line in lines]
        return cards

def firstTask(cards):
    result = 0
    for card in cards:
        matching = card.countWin()
        print(matching, 1 << matching)
        if matching > 0:
            result += 1 << (matching - 1)
    return result

def secondTask(cards): 
    inst = [1 for _ in cards]
    for i, card in enumerate(cards):
        matching = card.countWin()
        for j in range(1, matching + 1):
            if i + j < len(inst):
                inst[i + j] += inst[i]
    print(inst)
    result = functools.reduce(lambda a,b : a + b, inst)
    return result
                

if __name__=="__main__":
    cards = read()
    print(firstTask(cards))
    print(secondTask(cards))
