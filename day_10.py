data = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()

with open("input_10", "r") as file:
    data = file.read().strip()

area = [[int(char) for char in line] for line in data.splitlines()]

def is_in_area(i, j, area):
    return 0 <= i and i < len(area) and 0 <= j and j < len(area[i])

def find_possible_next_steps(i, j, area):
    current_height = area[i][j]
    possible_next_steps = []
    if is_in_area(i-1, j, area) and area[i-1][j] - current_height == 1:
        possible_next_steps.append((i-1, j))
    if is_in_area(i+1, j, area) and area[i+1][j] - current_height == 1:
        possible_next_steps.append((i+1, j))
    if is_in_area(i, j-1, area) and area[i][j-1] - current_height == 1:
        possible_next_steps.append((i, j-1))
    if is_in_area(i, j+1, area) and area[i][j+1] - current_height == 1:
        possible_next_steps.append((i, j+1))
    return possible_next_steps

PEAK = 9

def count_peaks(i, j, area):
    current_height = area[i][j]
    if current_height == PEAK:
        return {(i, j)}
    possible_next_steps = find_possible_next_steps(i, j, area)
    peaks = set() 
    for next_step in possible_next_steps:
        peaks = peaks.union(count_peaks(next_step[0], next_step[1], area))
    return peaks

scores = 0
for i, row in enumerate(area):
    for j, col in enumerate(row):
        if area[i][j] == 0:
            scores += len(count_peaks(i, j, area)) 

print(scores)

def count_trails(i, j, area):
    current_height = area[i][j]
    if current_height == PEAK:
        return 1
    possible_next_steps = find_possible_next_steps(i, j, area)
    return sum(count_trails(next_step[0], next_step[1], area) for next_step in possible_next_steps)

ratings = sum([
    count_trails(i, j, area)
    for i, row in enumerate(area) for j, _ in enumerate(row)
    if area[i][j] == 0
])

print(ratings)
