import sys
import functools
from dataclasses import dataclass
 
def isSymbol(char):
    return not char.isdigit() and '.' != char

@dataclass(init=False)
class Field:
    rows: list[str]
    width: int
    height: int

    def __init__(self, rows: list[str]):
        self.rows = rows
        self.height = len(rows)
    
        if self.height > 0:
            self.width = len(rows[0])
        else:
            self.width = 0

    def get(self, column, row):
        return self.rows[row][column]
    
    def nearSymbol(self, column, row):
        for y in range(max(0, row - 1), min(self.height - 1, row + 1) + 1):
            for x in range(max(0, column - 1), min(self.width - 1, column + 1) + 1):
                if x == column and y == row:
                    continue
                if isSymbol(self.rows[y][x]):
                    return True
        return False
    
    def locate(self, column, row):
        if column < 0 or column >= self.width:
            return []
        if row < 0 or row >= self.height:
            return []        

        if self.rows[row][column].isdigit():
            start = end = column
            while start -1 >= 0 and self.rows[row][start - 1].isdigit():
                start -= 1
            while end + 1 < self.width and self.rows[row][end + 1].isdigit():
                end += 1
            return [int(self.rows[row][start:(end + 1)])]
        return []
    
    def locateLine(self, column, row):
        result = []
        top = self.locate(column, row)
        if len(top) > 0:
            result.extend(top)
            return result
        result.extend(self.locate(column - 1, row))
        result.extend(self.locate(column + 1, row))
        return result
        



def read():
    fileName = sys.argv[1]
    with open(fileName) as f:
        lines = f.readlines()
        rows = [line.strip() for line in lines]
        return Field(rows)


def findSymbols(rows):
    symbols = []
    for row, points in enumerate(rows):
        for column, char in enumerate(points):
            if isSymbol(char):
                symbols.append({row: row, column: column})
    return symbols

class State:
    number: int
    valid: bool

    def __init__(self):
        self.reset()

    def getValue(self):
        if self.isValid():
            return self.number
        return 0
    
    def reset(self):
        self.number = 0
        self.valid = False

    def isValid(self):
        return self.valid
    
    def increase(self, digit: int, nearSymbol: bool):
        self.number = self.number * 10 + digit
        self.valid = self.valid or nearSymbol


def firstTask(field):
    result = 0
    for row, points in enumerate(field.rows):
        state = State()
        for column, char in enumerate(points):
            if not char.isdigit():
                result += state.getValue()
                state.reset()
            if char.isdigit():
                state.increase(int(char), field.nearSymbol(column, row))
        result += state.getValue()
    return result

def secondTask(field): 
    result = 0
    for row, points in enumerate(field.rows):
        for column, char in enumerate(points):
            if char == '*':
                nums = []
                nums.extend(field.locate(column - 1, row)) # left
                nums.extend(field.locate(column + 1, row)) # right
                nums.extend(field.locateLine(column, row - 1)) # top
                nums.extend(field.locateLine(column, row + 1)) # bottom
                values = list(filter(lambda x : x != None, nums))
                if len(values) == 2:
                    result += values[0] * values[1]
    return result
                

if __name__=="__main__":
    field = read()
    print(firstTask(field))
    print(secondTask(field))

# 76359193 to low
# 19785736
