import re
import operator

example_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

lines = [[int(digit) for digit in line.split(" ")] for line in re.split("\n+", example_input)]

with open("input_2", "r") as file:
    lines = file.readlines()

lines = [[int(digit) for digit in line.split(" ")] for line in lines]

def check(numbers):
    first_diff = numbers[1] - numbers[0]
    if first_diff == 0:
        return False
    relation = operator.lt if first_diff > 0 else operator.gt

    current = 0
    next = 1
    while next < len(numbers):
        if not relation(numbers[current], numbers[next]) or abs(numbers[current]- numbers[next]) > 3:
            return False
        current = next
        next += 1
    return True

def puzzle1(lines):
    return sum(check(line) for line in lines)

def check2(numbers):
    if check(numbers[1:]):
        return True
    first_diff = numbers[1] - numbers[0]
    if first_diff == 0:
        return False
    relation = operator.lt if first_diff > 0 else operator.gt

    current = 0
    next = 1
    while next < len(numbers):
        if not relation(numbers[current], numbers[next]) or abs(numbers[current] - numbers[next]) > 3:
            return check(numbers[:current] + numbers[current+1:]) or check(numbers[:next] + numbers[next+1:])
        current = next
        next += 1
    return True

def puzzle2(lines):
    return sum(check2(line) for line in lines)

print(puzzle1(lines))
print(puzzle2(lines))
