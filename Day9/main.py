import sys
import functools
from dataclasses import dataclass
from enum import IntEnum
from math import sqrt, ceil, floor, gcd
import re
from itertools import permutations

   
@dataclass
class Input:
    numbers: list[list[int]]

PARSE_REG = re.compile(r'([0-9A-Z]+)')



def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = f.readlines()
        numbers = [[int(v) for v in line] for line in [line.split() for line in lines]]
        return Input(numbers)

def findDiff(list: list[int]) -> (list[int], bool):
    res = []
    allZeroes = True
    for i in range(0, len(list) - 1):
        diff = list[i + 1] - list[i]
        res.append(diff)
        if diff != 0:
            allZeroes = False
    return res, allZeroes

def buildDiff(list: list[int]) -> list[list[int]]:
    differences: list[list[int]] = []
    differences.append(list)
    for level in range(0, len(list)):
        diff, allZeroes = findDiff(differences[level])
        differences.append(diff)
        if allZeroes:
            break
    return differences

def findNext(list):
    differences = buildDiff(list)
    # apend
    differences[-1].append(0)
    for level in range(len(differences) - 1, 0, -1):
        next = differences[level][-1] + differences[level - 1][-1]
        differences[level - 1].append(next)
    return differences[0][-1]


def findPrev(list):
    differences = buildDiff(list)
    # apend
    differences[-1] = [0] + differences[-1]
    for level in range(len(differences) - 1, 0, -1):
        prev = differences[level - 1][0] - differences[level][0] 
        differences[level - 1] = [prev] + differences[level - 1]
    return differences[0][0]

def firstTask(input):
    result = 0
    for list in input.numbers:
        result += findNext(list)
    return result


def secondTask(input):
    result = 0
    for list in input.numbers:
        result += findPrev(list)
    return result


if __name__=="__main__":
    input = read()
    print(firstTask(input))
    print(secondTask(input))
