import sys
import functools
from dataclasses import dataclass
from enum import Enum
from math import sqrt, ceil, floor


@dataclass
class Input:
    times: list[int]
    distances: list[int]


def calculate(time: int, distance: int):
    comb = 0
    for i in range(0, time + 1):
        speed = i
        ttime = time - i
        d = speed * ttime
        if d > distance:
            comb += 1
            print(i, speed, ttime)
            
    print(comb)
    return comb

def convertToInts(arr: list[str]):
    return [int(v) for v in arr]

def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = f.readlines()
        times = convertToInts(lines[0].split()[1:])
        distances = convertToInts(lines[1].split()[1:])
        return Input(times, distances)

def firstTask(input):
    result = 1
    for i in range(0, len(input.times)):
        result *= calculate(input.times[i], input.distances[i])
    return result

def convertArrToInt(arr: list[int]) -> int:
    nums = [str(v) for v in arr]
    concatStr = functools.reduce(lambda a, b: a + b, nums)
    return int(concatStr)

def findRange(time: int, distance: int):
    # x * (time - x) > distance
    # - x^2 + time * x - distance > 0
    # x^2 - time * x + distance < 0
    # delta = time^2 - 4*distance
    # x1 = (time - sqrt(4*distance)) / 2
    # x2 = time + sqrt(4*distance) / 2
    delta = time**2 - 4*distance
    print(delta)
    x1 = (time - sqrt(delta))/2
    x2 = (time + sqrt(delta))/2
    return (ceil(min(x1,x2)), floor(max(x1,x2)))

def secondTask(input):
    time = convertArrToInt(input.times)
    distance = convertArrToInt(input.distances)
    start,end = findRange(time, distance)
    print(time, distance)
    print(start, end)
    return end - start + 1


if __name__=="__main__":
    input = read()
    print(firstTask(input))
    print(secondTask(input))
