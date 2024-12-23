from dataclasses import dataclass

data = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()

with open("input_8", "r") as file:
    data = file.read().strip()

# In particular, an antinode occurs at any point that is perfectly in line with
# two antennas of the same frequency - but only when one of the antennas is
# twice as far away as the other. This means that for any pair of antennas with
# the same frequency, there are two antinodes, one on either side of them.

# I can use taxicab distance to determine the antinodes for any pair of antennas.

area = [[char for char in line] for line in data.splitlines()]

@dataclass(frozen=True)
class Position:
    y: int
    x: int

antennas = dict()

for i, row in enumerate(area):
    for j, char in enumerate(row):
        if char != ".":
            if char not in antennas:
                antennas[char] = list()
            antennas[char].append(Position(i, j))


antinodes = set()

# Finds antinode closer to the first position.
def find_antinode(first_position, second_position):
    vertical_difference = second_position.y - first_position.y
    horizontal_difference = second_position.x - first_position.x

    possible_antinode_y = first_position.y - vertical_difference
    possible_antinode_x = first_position.x - horizontal_difference

    return Position(possible_antinode_y, possible_antinode_x)

def is_in_area(position, area):
    return 0 <= position.y < len(area) and 0 <= position.x < len(area[position.y])

for antenna_type in antennas:
    same_frequency_antennas = antennas[antenna_type] 
    for first_index in range(len(same_frequency_antennas)):
        for second_index in range(first_index+1, len(same_frequency_antennas)):
            first_position = same_frequency_antennas[first_index]
            second_position = same_frequency_antennas[second_index]

            possible_position = find_antinode(first_position, second_position)
            if is_in_area(possible_position, area):
                antinodes.add(possible_position)

            possible_position = find_antinode(second_position, first_position)
            if is_in_area(possible_position, area):
                antinodes.add(possible_position)

print(len(antinodes))

# Part 2
antinodes = set()
for antenna_type in antennas:
    same_frequency_antennas = antennas[antenna_type] 
    for first_index in range(len(same_frequency_antennas)):
        for second_index in range(first_index+1, len(same_frequency_antennas)):
            first_position = same_frequency_antennas[first_index]
            second_position = same_frequency_antennas[second_index]


            # Keep finding the position of the next antinode.
            # For first antenna:
            possible_position = find_antinode(first_position, second_position)
            while is_in_area(possible_position, area):
                antinodes.add(possible_position)
                second_position = first_position
                first_position = possible_position 
                possible_position = find_antinode(first_position, second_position)

            # For second antenna:
            possible_position = find_antinode(second_position, first_position)
            while is_in_area(possible_position, area):
                antinodes.add(possible_position)
                first_position = second_position
                second_position = possible_position
                possible_position = find_antinode(second_position, first_position)

# Add the antennas themselves.
for antenna_type in antennas:
    same_frequency_antennas = antennas[antenna_type]
    if len(same_frequency_antennas) > 1:
        for antenna in same_frequency_antennas:
            antinodes.add(antenna)

print(len(antinodes))
