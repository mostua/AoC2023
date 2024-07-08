import sys
import functools
from dataclasses import dataclass
from enum import IntEnum
from math import sqrt, ceil, floor, gcd
import re
from itertools import permutations

@dataclass
class Row:
    streams: str
    group: list[int]

    def __hash__(self):
        return self.streams.__hash__()

@dataclass
class Input:
    rows: list[Row]

def read():
    fileName = sys.argv[1]
    rows = []
    with open(fileName) as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split(' ')
            streams = parts[0]
            group = [int(x) for x in parts[1].split(',')]
            rows.append(Row(streams, group))    
    return Input(rows)

def calcGroups(streams: str) -> list[int]: 
    group = 0
    prev = '.'
    res = []
    guarded = streams + '.'
    for s in guarded:
        if s == '#':
            group += 1
        elif prev == '#' and s == '.':
            res.append(group)
            group = 0
        prev = s
    return res

def uniq(opts: list[Row]) -> list[Row]:
    return  list(dict.fromkeys(opts))


def withOper(v: Row) -> Row:
    return Row('.' + v.streams, v.group)

def withDem(v: Row) -> Row:
    if len(v.streams) == 0 or v.streams[0] == '.':
        return Row("#" + v.streams, [1] + v.group)
    else:
        newGroup = [0] if len(v.group) == 0 else v.group[:]
        newGroup[0] += 1
        return Row("#" + v.streams, newGroup)

def canMatch(row: Row, destGr: list[int]) -> bool:
    if len(row.group) > len(destGr):
        return False
    for i, v in enumerate(row.group):
        # s : 0  0  0  0
        # 4 : 10 20 30 40
        # 2 : 29 40
        destI = len(destGr) - len(row.group) + i  
        if i == 0:
            if v > destGr[destI]:
                return False
        else:
            if v != destGr[destI]:
                return False
    return True
            

def generateOptions(row: Row, destGroup: list[int]) -> list[Row]:
    if len(row.streams) == 0:
        return [Row('', [])]
    s = row.streams
    nexts = []
    for next in uniq(generateOptions(Row(s[1:], row.group), destGroup)):
        if canMatch(next, destGroup):
            nexts.append(next) 
    result = []
    for v in nexts:
        if s[0] == '?':
            result.append(withOper(v))
            result.append(withDem(v))
        else:
            if s[0] == '.':
                result.append(withOper(v))
            else:
                result.append(withDem(v))
    return result

def calculateArrangments(row: Row) -> int:
    options = generateOptions(row, row.group)
    result = 0
    for opt in options:
        if opt.group == row.group:
            result += 1
    return result

def firstTask(input: Input):
    result = 0
    for row in input.rows:
        result += calculateArrangments(row)
    return result

def makeFive(row: Row) -> Row:
    streams = ''
    group = []
    for _ in range(0, 5):
        streams += row.streams
        group = group + row.group
    return Row(streams, group)

def secondTask(input: Input):
    result = 0
    for i, row in enumerate(input.rows):
        print(makeFive(row))
        result += calculateArrangments(makeFive(row))
        print(i, result)
    return result


if __name__=="__main__":
    input = read()
    print(firstTask(input))
    print(secondTask(input)) 
