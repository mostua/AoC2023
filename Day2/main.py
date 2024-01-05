import sys
import functools
from dataclasses import dataclass
 
@dataclass
class Set:
    red: int
    green: int
    blue: int


@dataclass
class Game:
    no: int
    sets: list[Set]


def parseGameNo(gamePart):
    return int(gamePart[5:])

def parseSet(setPart):
    result = Set(red=0,green=0,blue=0)
    for colorDef in setPart.split(','):
        x = colorDef.strip().split(' ')
        color = x[1]
        value = int(x[0])
        if color == "red":
            result.red = value
        elif color == "green":
            result.green = value
        elif color == "blue":
            result.blue = value
    return result


def parseSets(setsPart):
    return [parseSet(setPart) for setPart in setsPart.split(';')]

def parseGame(line):
    parts = line.split(':')
    gamePart = parts[0]
    setsPart = parts[1]
    no = parseGameNo(gamePart)
    sets = parseSets(setsPart)
    return Game(no, sets)



def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = f.readlines()
        games = [parseGame(line) for line in lines]
        return games

MAX_CUBES = Set(red=12, green=13, blue=14)

def findMaxSet(game):
    maxSet = Set(red=0,green=0,blue=0)
    for set in game.sets:
        maxSet.red = max(maxSet.red, set.red)
        maxSet.green = max(maxSet.green, set.green)
        maxSet.blue = max(maxSet.blue, set.blue)
    return maxSet

def firstTask(games):
    possible = 0
    for game in games:
        maxSet = findMaxSet(game)
        if maxSet.red <= MAX_CUBES.red and maxSet.green <= MAX_CUBES.green and maxSet.blue <= MAX_CUBES.blue:
            possible += game.no
    return possible

def secondTask(games):
    result = 0
    for game in games:
        maxSet = findMaxSet(game)
        result += maxSet.red * maxSet.green * maxSet.blue
    return result

if __name__=="__main__":
    games = read()
    print(firstTask(games))
    print(secondTask(games))