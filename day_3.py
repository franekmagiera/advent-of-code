import re

input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

with open("input_3", "r") as file:
    input = file.read()

def puzzle1(input):
    pattern = re.compile(r"mul\((\d+),(\d+)\)")
    matches = pattern.findall(input)
    return sum(int(match[0]) * int(match[1]) for match in matches)

print(puzzle1(input))

def puzzle2(input):
    pattern = re.compile(r"mul\((\d+),(\d+)\)|(don't)\(\)|(do)\(\)")
    matches = pattern.findall(input)

    sum = 0
    include = True
    for match in matches:
        if match[-1] == "do":
            include = True
            continue
        if match[-2] == "don't":
            include = False
            continue
        if include:
            sum += int(match[0]) * int (match[1])
    return sum 

print(puzzle2(input))
