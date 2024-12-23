import re

example_input = """3   4
4   3
2   5
1   3
3   9
3   3"""

lines = re.split("\n+", example_input)

with open("input_1", "r") as file:
    lines = file.readlines()

left = []
right = []

for line in lines:
    if line:
        split = re.split(r"\s+", line)
        left.append(int(split[0]))
        right.append(int(split[1]))

def puzzle1(left, right):
    return sum((abs(l - r) for l, r in zip(sorted(left), sorted(right))))

def puzzle2(left, right):
    frequency = dict()
    for number in right:
        if frequency.get(number) is None:
            frequency[number] = 1
        else:
            frequency[number] += 1
    return sum((number * frequency.get(number, 0) for number in left))

print("Puzzle 1 result: ", puzzle1(left, right))
print("Puzzle 2 result: ", puzzle2(left, right))
