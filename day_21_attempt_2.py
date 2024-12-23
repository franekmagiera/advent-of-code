import re
from collections import deque

data = """
029A
980A
179A
456A
379A
""".strip()

data = """
319A
985A
340A
489A
964A
""".strip()

codes = data.splitlines()

def get_numeric_part(code):
    pattern = re.compile(r"(\d+)[a-zA-Z]")
    match = pattern.match(code)
    return int(match.group(1))

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

numeric_pad = [
    [ "7", "8", "9"],
    [ "4", "5", "6"],
    [ "1", "2", "3"],
    [None, "0", "A"]
]

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
directional_keypad = [
    [None, "^", "A"],
    [ "<", "v", ">"]
]

def find_paths_for_keypad(keypad: list[list[int]]):
    # None key should be avoided.
    all_keys = [key for row in keypad for key in row if key is not None]

    paths = {key: dict() for key in all_keys}

    for i, row in enumerate(keypad):
        for j, element in enumerate(row):
            if element is not None:
                for goal in all_keys:
                    if element != goal:
                        paths[element][goal] = find_paths(i, j, goal, keypad)
                    else:
                        paths[element][goal] = [""]
    
    return paths 

def find_paths(from_x: int, from_y: int, goal: str, keypad: list[list[int]]):
    if keypad[from_x][from_y] == goal:
        raise RuntimeError("did not expect that")

    queue = deque()
    queue.append((from_x, from_y, ""))
    visited = set()

    paths = []
    while queue:
        x, y, moves = queue.popleft()
        if keypad[x][y] == goal:
            paths.append(moves)
        else:
            neighbors = get_neighbors(x, y, keypad)
            for neighbor in neighbors:
                row, col, move = neighbor
                if keypad[row][col] is not None and (row, col) not in visited:
                    queue.append((row, col, moves + move))
        visited.add((x, y))
    return paths

def within_limits(x, y, array):
    return 0 <= x < len(array) and 0 <= y < len(array[x])

def get_neighbors(x, y, array):
    return [
        (row, col, move)
        for row, col, move in [(x-1, y, "^"), (x+1, y, "v"), (x, y-1, "<"), (x, y+1, ">")]
        if within_limits(row, col, array)
    ]

numeric_keypad_paths = find_paths_for_keypad(numeric_pad)
directional_keypad_paths = find_paths_for_keypad(directional_keypad)

def generate_paths(keys, keypad_paths, previous_key="A"):
    if previous_key == "A":
        keys = "A" + keys
    if len(keys) == 2:
        return [path + "A" for path in keypad_paths[keys[0]][keys[1]]]
    return [
        path + "A" + next_part
        for path in keypad_paths[keys[0]][keys[1]]
        for next_part in generate_paths(keys[1:], keypad_paths, "")
    ]

# This did part 1:
# complexity = 0
# for code in codes:
#     paths = generate_paths(code, numeric_keypad_paths)
#     for i in range(2):
#         paths = [
#             next_level_path
#             for path in paths
#             for next_level_path in generate_paths(path, directional_keypad_paths)
#         ]
#     shortest_path = min(paths, key=len)
#     complexity += len(shortest_path) * get_numeric_part(code)

# print(complexity)
# For part 2 it is going to be too slow.

# Part 2
def generate_paths_for_directional_keypad(keys, previous_key="A"):
    if previous_key == "A":
        keys = "A" + keys
    if keys == "A":
        return [""]
    if len(keys) == 2:
        return [path + "A" for path in directional_keypad_paths[keys[0]][keys[1]]]
    return [
        path + "A" + next_part
        for path in directional_keypad_paths[keys[0]][keys[1]]
        for next_part in generate_paths(keys[1:], directional_keypad_paths, "")
    ]

def find_shortest_sequence(keys, depth, cache):
    if depth == 0:
        return len(keys)
    if (keys, depth) in cache:
        return cache[(keys, depth)]
    moves_to_make = keys.split("A")
    total_length = 0
    for i, move in enumerate(moves_to_make):
        if i != len(moves_to_make) - 1:
            move = move + "A"
        paths = generate_paths_for_directional_keypad(move)
        total_length += min(find_shortest_sequence(path, depth-1, cache) for path in paths)
    cache[(keys, depth)] = total_length
    return total_length

complexity = 0
for code in codes:
    paths = generate_paths(code, numeric_keypad_paths)
    cache = {}
    shortest_path = min(find_shortest_sequence(path, 25, cache) for path in paths)
    complexity += shortest_path * get_numeric_part(code)
print(complexity)

# It was hard, couldn't have done it without the tips from:
# https://www.reddit.com/r/adventofcode/comments/1hjx0x4/2024_day_21_quick_tutorial_to_solve_part_2_in/
