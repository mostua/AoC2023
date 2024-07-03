import sys
import functools
from dataclasses import dataclass
from enum import IntEnum
from math import sqrt, ceil, floor, gcd
import re
from itertools import permutations


sys.setrecursionlimit(140**2)

@dataclass(frozen=True)
class Pos:
    x: int
    y: int

@dataclass
class Input:
    rows: list[str]
    maxX: int
    maxY: int

    def within(self, p: Pos) -> bool: 
        return p.x >= 0 and p.x <= input.maxX and p.y >= 0 and p.y <= input.maxY

@dataclass(frozen=True)
class Vect:
    x: int
    y: int

@dataclass
class Net:
    start: Pos
    nodes: dict[Pos, list[Pos]]

#######
# 0 1 2
# 1
# 2

TAIL = {
    '|': [Vect(0, 1), Vect(0, -1)],
    '-': [Vect(1, 0), Vect(-1, 0)],
    'L': [Vect(1, 0), Vect(0, -1)],
    'J': [Vect(-1, 0), Vect(0, -1)],
    '7': [Vect(0, 1), Vect(-1, 0)],
    'F': [Vect(1, 0), Vect(0, 1)],
    '.': [],
    'S': [Vect(1, 0), Vect(0, 1), Vect(-1, 0), Vect(0, -1)]
}

ANGLE = {
    'L': True,
    'J': True,
    '7': True,
    'F': True
}

LINEAR = {
    '|': True,
    '-': True
}



def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = f.readlines()
        rows = [line.strip() for line in lines]    
        maxX = len(rows[0]) - 1
        maxY = len(rows) - 1
        return Input(rows, maxX, maxY)

def convertToNet(input: Input) -> Net:
    start = None
    nodesDirect = {}
    nodesIndirect = {}
    onList = lambda p, list: len([x for x in list if x == p]) > 0
    for y, row in enumerate(input.rows):
        for x, val in enumerate(row):
            node = Pos(x, y)
            if val == 'S':
                start = node
            edges = TAIL[val]
            nextPosList = []
            for edge in edges:
                nx = x + edge.x
                ny = y + edge.y
                nextPos = Pos(nx, ny)
                if input.within(nextPos):
                    nextPosList.append(nextPos)
            nodesDirect[node] = nextPosList
    for node in nodesDirect:
        indirect = []
        for next in nodesDirect[node]:
            if onList(node, nodesDirect[next]):
                indirect.append(next)
        nodesIndirect[node] = indirect
    return Net(start, nodesIndirect)

class Dfs:
    visited: dict[Pos, Pos]
    last: Pos
    net: Net

    def __init__(self, net: Net):
        self.visited = {}
        self.net = net
    
    def execute(self):
        self.next(self.net.start, None)
    
    def next(self, node: Pos, prev: Pos):
        self.visited[node] = prev
        sibs = self.net.nodes[node]
        for sib in sibs:
            # visited
            if sib in self.visited:
                # if start - we have a loop
                if sib == self.net.start and sib != prev:
                    self.last = node
            # go futher
            else: 
                self.next(sib, node)

    def findLoop(self):
        result = []
        current = self.last
        while current != None:
            result.append(current)
            current = self.visited[current]
        return result


def findLoop(net):
    dfs = Dfs(net)
    dfs.execute()
    return dfs.findLoop()

def firstTask(input):
    net = convertToNet(input)
    loop = findLoop(net)
    return (len(loop) + 1) // 2

def findAround():
    result = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if x == y == 0:
                continue
            result.append(Pos(x, y))
    print(result)
    return result

AROUND = findAround()

def vect(a: Pos, b: Pos) -> Vect:
    return Vect(a.x - b.x, a.y - b.y)

# scal mult
def vectMul(a: Vect, b: Vect): 
    print(a,b)
    assert a.x**2 + a.y**2 == 1
    assert b.x**2 + b.y**2 == 1
    return (a.x * b.x + a.y * b.y)

# |       
# L - (0, 1) (1, 0)

#   |
#  -J (0, 1) (-1, 0)

def secondTask(input: Input):
    net = convertToNet(input)
    loop = findLoop(net)
    print(loop)
    visited = {}
    partOfLoop = {}
    for l in loop:
        visited[l] = True
        partOfLoop[l] = True
    
    for i, p in enumerate(loop):
        mul = vectMul(vect(loop[i], loop[i-1]), vect(loop[(i+1)%len(loop)], loop[i]))
        print(input.rows[p.y][p.x], p, mul)
    starts = {}
    for Y in [0, input.maxY]:        
        for x in range(0, input.maxX + 1):
            cand = Pos(x, Y)
            if not cand in starts:
                starts[cand] = True
    for X in [0, input.maxX]:
        for y in range(0, input.maxY + 1):
            cand = Pos(X, y)
            if not cand in starts:
                starts[cand] = True
    for start in starts:
        visited[start] = True
        findPosible = lambda pos: [next for next in [Pos(pos.x + a.x, pos.y + a.y)
                                                    for a in AROUND] 
                                                    if input.within(next) and not next in visited]
        toVisit = findPosible(start)
        while len(toVisit) > 0:
            first = toVisit[0]
            del toVisit[0]
            if first in visited:
                continue
            visited[first] = True
            toVisit = toVisit + findPosible(first)
    for y in range(0, input.maxY + 1):
        for x in range(0, input.maxX + 1):
            p = Pos(x, y)
            if p in partOfLoop:
                print(input.rows[y][x], end="")
            elif p in visited:
                print("*", end="")
            else:
                print(".", end="")
        print("\n")

    return (input.maxX + 1) * (input.maxY + 1) - len(visited)


if __name__=="__main__":
    input = read()
    print(firstTask(input))
    print(secondTask(input))

# 834 - to high
# 813 - to high