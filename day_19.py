data = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".strip().splitlines()

with open("input_19", "r") as file:
    data = file.read().strip().splitlines()

available_patterns = set(data[0].split(", "))
designs = data[2:]

possible_patterns = set()

def is_possible(design: str, available_patterns, possible_patterns):
    if design in available_patterns:
        return True
    if design in possible_patterns:
        return True
    
    result = any(
        is_possible(design.removeprefix(available_pattern), available_patterns, possible_patterns)
        for available_pattern in available_patterns
        if design.startswith(available_pattern)
    )

    if result:
        possible_patterns.add(design)
    return result

result = sum(is_possible(design, available_patterns, possible_patterns) for design in designs)
print(result)


# Part 2
possible_patterns = dict()

def count_possible(design: str, available_patterns, possible_patterns):
    if design in possible_patterns:
        return possible_patterns[design]
    
    result = sum(
        count_possible(design.removeprefix(available_pattern), available_patterns, possible_patterns)
        for available_pattern in available_patterns
        if design.startswith(available_pattern)
    )

    if design in available_patterns:
        result += 1

    if result != 0:
        if design not in possible_patterns:
            possible_patterns[design] = 0
        possible_patterns[design] += result

    return result

result = sum(count_possible(design, available_patterns, possible_patterns) for design in designs)
print(result)
