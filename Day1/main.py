import sys
import functools

def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = f.readlines()
        return lines


def extract(line): 
    return [char for char in line if char.isdigit()]

def extractDigits(lines):
    return [extract(line) for line in lines]

def extractNumber(digits): 
    return [int(dig[0] + dig[len(dig) - 1]) for dig in digits]

def sumAll(numbers):
    return functools.reduce(lambda a,b: a+b, numbers)

def firstTask(lines):
    digits = extractDigits(lines)
    numbers = extractNumber(digits)
    return sumAll(numbers)


NUM_MAPS = {
    'one': '1', 
    'two': '2', 
    'three': '3', 
    'four': '4', 
    'five': '5', 
    'six': '6', 
    'seven': '7', 
    'eight': '8', 
    'nine': '9'
}

def replaceLiterals(line):
    result = line
    for replace in NUM_MAPS:
        # trick to not parse everything, make one one1one to keep shared letters intact
        result = result.replace(replace, replace + NUM_MAPS[replace] + replace)
    return result

def secondTask(lines):
    replaced = [replaceLiterals(line) for line in lines]
    digits = extractDigits(replaced)
    numbers = extractNumber(digits)
    return sumAll(numbers)

if __name__=="__main__":
    lines = read()
    print(firstTask(lines))
    print(secondTask(lines))