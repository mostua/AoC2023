import sys
import functools
from dataclasses import dataclass
from enum import Enum



    # seed = 1
    # soil = 2
    # fertilizer = 3
    # water = 4
    # light = 5
    # temperature = 6
    # humidity = 7
    # location = 8

@dataclass
class Mapping:
    destStart: int
    sourceStart: int
    range: int

@dataclass
class Converter:
    fr: str
    to: str
    mappings: list[Mapping]

@dataclass
class Input:
    seeds: list[str]
    maps: dict[str, Converter]

    def convertSeed(self, seed: int, type: str) -> (int, str):
        converter = self.maps[type]
        newType = converter.to
        for mapping in converter.mappings:
            if mapping.sourceStart <= seed and seed < mapping.sourceStart + mapping.range:
                return (mapping.destStart + seed - mapping.sourceStart), newType
        # not found -> map to the same value
        return seed, newType


def parseSeeds(seedLine: str):
    return [int(str) for str in seedLine.split(" ")[1:]]

def parseConvDef(mapDefStr: str) -> (str, str):
    parts = mapDefStr.split('-')
    return (parts[0], parts[2])

def parseMapping(line: str) -> Mapping:
    nums = [int(num) for num in line.split()]
    return Mapping(nums[0], nums[1], nums[2])

def parseConv(conLines: list[str]) -> Converter:
    (fr, to) = parseConvDef(conLines[0].replace(" map:", ""))
    mappings = [parseMapping(conLine) for conLine in conLines[1:]]
    return Converter(fr, to, mappings)


def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = [line.strip() for line in f.readlines()]
        parts = []
        current = []
        for l in lines: 
            if l == "":
                if len(current) > 0:
                    parts.append(current)
                current = []
            else:
                current.append(l)
        
        # last part
        if len(current) > 0:
            parts.append(current)
                
        seeds = parseSeeds(parts[0][0])
        convs = [parseConv(conv) for conv in parts[1:]]
        convsDict = {}
        for c in convs:
            convsDict[c.fr] = c
        return Input(seeds, convsDict)
    
TYPES = [
    'seed',
    'soil',
    'fertilizer',
    'water',
    'light',
    'temperature',
    'humidity',
    'location'
    ]

def mapSeed(seed: int, input: Input) -> int:
    currentVal = seed
    type = 'seed'
    while True:
        currentVal, type = input.convertSeed(currentVal, type)
        if type == 'location':
            return currentVal


def firstTask(input):
    mapped = [mapSeed(seed, input) for seed in input.seeds]
    return min(mapped)

def secondTask(input):
    for i in range(input.seeds[0], input.seeds[0] + 100):
        print(mapSeed(i, input))
    return input


if __name__=="__main__":
    input = read()
    print(input)
    print(firstTask(input))
    print(secondTask(input))
