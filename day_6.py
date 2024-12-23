from enum import Enum

data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

with open("input_6", "r") as file:
    data = file.read()

m = [[char for char in line] for line in data.splitlines()]

# Find the initial position of the guard.
def find_guard(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == "^":
                return (i, j)
    return None

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def turn_right(self):
        match self:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP
    
initial_i, initial_j = find_guard(m)
i, j = initial_i, initial_j
direction = Direction.UP

visited_positions = list()

# Clear the initial position.
m[i][j] = "."

def get_next_position(i, j, direction):
    match direction:
        case Direction.UP:
            return i-1, j
        case Direction.RIGHT:
            return i, j+1
        case Direction.DOWN:
            return i+1, j
        case Direction.LEFT:
            return i, j-1
    print("Error for ", i, j, direction)

while True:
    visited_positions.append((i, j, direction))
    next_i, next_j = get_next_position(i, j, direction)
    if not (0 <= next_i < len(m) and 0 <= next_j < len(m[i])):
        break
    if m[next_i][next_j] == ".":
        i, j = next_i, next_j
    elif m[next_i][next_j] == "#":
        direction = direction.turn_right()

distinct_visited_positions = dict()
for t, position in enumerate(visited_positions):
    if distinct_visited_positions.get((position[0], position[1])) is None:
        distinct_visited_positions[(position[0], position[1])] = list()
    # key is (i, j), value is (time, direction)
    distinct_visited_positions[(position[0], position[1])].append((t, position[2]))

print(len(distinct_visited_positions))

# Part 2
possible_obstructions = set() 

for k, visited_position in enumerate(visited_positions):
    # Exclude guard's starting position.
    if (visited_position[0], visited_position[1]) == (initial_i, initial_j):
        continue
    m[visited_position[0]][visited_position[1]] = k 

    # Go back to the first position.
    i, j = visited_positions[0][0], visited_positions[0][1]
    direction = visited_positions[0][2]
    positions_visited_after_obstruction = set()
    
    while True:
        positions_visited_after_obstruction.add((i, j, direction))
        next_i, next_j = get_next_position(i, j, direction)
        if not (0 <= next_i < len(m) and 0 <= next_j < len(m[i])):
            break
        if m[next_i][next_j] == "#" or m[next_i][next_j] == k:
            direction = direction.turn_right()
            continue
        if (next_i, next_j, direction) in positions_visited_after_obstruction:
            possible_obstructions.add((visited_position[0], visited_position[1])) 
            break
        if m[next_i][next_j] == ".":
            i, j = next_i, next_j
    
    m[visited_position[0]][visited_position[1]] = "."

print(len(possible_obstructions))

# Pretty slow: ~13 seconds.
