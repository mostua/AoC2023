import sys
import functools
from dataclasses import dataclass
from enum import IntEnum
from math import sqrt, ceil, floor, gcd
import re
from itertools import permutations

@dataclass
class Point:
    x: int
    y: int
   
@dataclass
class Input:
    points: list[list[int]]

def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = f.readlines()
        points = []
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '#':
                    points.append(Point(x, y))
        return Input(points)
    
SCALE = 1000000

@dataclass
class Range:
    start: int
    end: int

    def len(self):
        return self.end-self.start+1
    
    def val(self):
        return self.len() * (SCALE - 1)


def findSpaces(points: list[int]) -> list[Range]: # here is an error
    res = []
    for i, val in enumerate(points):                     
        ni = i + 1
        if ni == len(points):
            break
        assert points[ni] >= val
        if points[ni] - 1 >= val + 1:
            res.append(Range(val + 1, points[ni] - 1))
    return res

def move(val: int, spaces: list[Range]) -> int:
    # slow but ok
    add = 0
    for xs in spaces:
        if xs.end < val:
            add += xs.val()
    return val + add

def transform(p: Point, xSpaces: list[Range], ySpaces: list[Range]) -> Point:
    return Point(move(p.x, xSpaces), move(p.y, ySpaces))

def dist(a: int, b:int) -> int:
    return max(a, b) - min(a, b)

def calculateDistance(p1: Point, p2: Point) -> int:
    return dist(p1.x, p2.x) + dist(p1.y, p2.y) 

def firstTask(input: Input):
    xs = []
    ys = []
    for p in input.points:
        xs.append(p.x)
        ys.append(p.y)
    xs.sort()
    ys.sort()
    xSpaces = findSpaces(xs)
    ySpaces = findSpaces(ys)
    print(xSpaces, ySpaces)
    result = 0
    for i, p1 in enumerate(input.points):
        for j, p2 in enumerate(input.points):
            if i < j:
                m1 = transform(p1, xSpaces, ySpaces)
                m2 = transform(p2, xSpaces, ySpaces)
#                print("{} {} -> {} {} -> {}".format(p1, p2, m1, m2, calculateDistance(m1, m2)))
                result += calculateDistance(m1, m2)
        print("{}".format(i))
    return result

def secondTask(input):
    result = 0
    return result


if __name__=="__main__":
    input = read()
    print(firstTask(input))
    print(secondTask(input)) 
