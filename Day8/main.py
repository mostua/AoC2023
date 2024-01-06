import sys
import functools
from dataclasses import dataclass
from enum import IntEnum
from math import sqrt, ceil, floor, gcd
import re
from itertools import permutations

   
@dataclass
class Node:
    id: str
    left: str
    right: str

@dataclass
class Input:
    ins: str
    nodes: list[Node]
    net: dict[str, Node]

PARSE_REG = re.compile(r'([0-9A-Z]+)')

def parseNode(line):
    v = line.split()
    res = PARSE_REG.findall(line)
    return Node(res[0], res[1], res[2])

def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = f.readlines()
        ins = lines[0].strip()
        nodes = [parseNode(line.strip()) for line in lines[2:]]
        net = {}
        for node in nodes:
            net[node.id] = node
        return Input(ins, nodes, net)
    
@dataclass(frozen=True)
class VisitKey:
    id: str
    step: int

    
def findNoSteps(input: str, start: str, end: str):
    print(start, end)
    visited = {}
    current =  start
    if not start in input.net:
        return -1
    i = 0
    while current != end:
        visitKey = VisitKey(current, i % len(input.ins))
        if visitKey in visited:
            raise Exception('Loop detected')
        visited[visitKey] = True
        ins = input.ins[i % len(input.ins)]
        if ins == 'L':
            current = input.net[current].left
        else:
            current = input.net[current].right
        i += 1
            
    return i


def firstTask(input):
    return findNoSteps(input, 'AAA', 'ZZZ')


def allEnds(list: list[str], letter: str):
    return len(list) == len([v for v in list if v[2] == letter])

def findLcm(list: list[int]) -> int:
    if len(list) == 1:
        return list[0]
    if len(list) == 2:
        return int(list[0] * list[1] / gcd(list[0], list[1]))
    else:
        return findLcm([list[0], findLcm(list[1:])])

def secondTask(input):
    starts = [node.id for node in input.nodes if node.id[2] == 'A']
    ends = [node.id for node in input.nodes if node.id[2] == 'Z']
    distances = {}
    for start in starts:
        distances[start] = {}
        for end in ends:
            try:
                distances[start][end] = findNoSteps(input, start, end)
            except:
                distances[start][end] = -1
                print("{} -> {} not found".format(start, end))
            
        
    lowest = sys.maxsize
    print(distances)
    for endPerm in permutations(ends):
        values = []
        for i in range(0, len(starts)):
            values.append(distances[starts[i]][endPerm[i]])
        if len([value for value in values if value < 0]) > 0:
            continue
        lowest = min([lowest, findLcm(values)])
    return lowest
        


if __name__=="__main__":
    input = read()
    print(firstTask(input))
    print(secondTask(input))
