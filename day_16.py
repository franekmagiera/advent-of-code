from enum import Enum

data = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""".strip()

data = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""".strip()

with open("input_16", "r") as file:
    data = file.read().strip()

plan = [[char for char in row] for row in data.splitlines()]

def find_sign(sign, plan):
    for i, row in enumerate(plan):
        for j, el in enumerate(row):
            if el == sign:
                return i, j
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

    def turn_left(self):
        match self:
            case Direction.UP:
                return Direction.LEFT
            case Direction.RIGHT:
                return Direction.UP
            case Direction.DOWN:
                return Direction.RIGHT
            case Direction.LEFT:
                return Direction.DOWN
    
    def get_next_position(self, i, j):
        match self:
            case Direction.UP:
                return i-1, j
            case Direction.RIGHT:
                return i, j+1
            case Direction.DOWN:
                return i+1, j
            case Direction.LEFT:
                return i, j-1

class Minimum:
    def __init__(self):
        self.minimum = float("inf")
        self.positions = set()

    def update(self, number, positions):
        if number < self.minimum:
            self.positions = set()
        self.minimum = min(self.minimum, number)
        self.positions.update(positions)


start = find_sign("S", plan)
assert start is not None
direction = Direction.RIGHT
start_x, start_y = start
to_check = [(start_x, start_y, direction, 0, [(start_x, start_y)])]  # stack of position, direction, cost and visited_points

minimum = Minimum()
MOVING_COST = 1
ROTATION_COST = 1000

visited = dict()
z = 0
while to_check:
    z += 1
    if z % 1000000 == 0:
        print(z, len(to_check))
    i, j, current_direction, current_cost, positions = to_check.pop()
    if plan[i][j] == "#":
        # Not a valid path.
        continue
    if plan[i][j] == "E":
        # Found a path.
        minimum.update(current_cost, positions)
        continue
    if current_cost > 106512: # minimum.minimum: # Cheating a bit, somehow for part 1 I had a quicker solution, I used the result to cut off suboptimal solutions earlier here.
        # Not worth going further.
        continue
    if visited.get((i, j, current_direction.value), float("inf")) < current_cost:
        continue
    visited[(i, j, current_direction.value)] = current_cost
    # Try turning left:
    next_i, next_j = current_direction.turn_left().get_next_position(i, j)
    to_check.append((next_i, next_j, current_direction.turn_left(), current_cost + ROTATION_COST + MOVING_COST, positions + [(next_i, next_j)]))
    # Try turning right:
    next_i, next_j = current_direction.turn_right().get_next_position(i, j)
    to_check.append((next_i, next_j, current_direction.turn_right(), current_cost + ROTATION_COST + MOVING_COST, positions + [(next_i, next_j)]))
    # Try next position:
    next_i, next_j = current_direction.get_next_position(i, j)
    to_check.append((next_i, next_j, current_direction, current_cost + MOVING_COST, positions + [(next_i, next_j)]))

print(minimum.minimum)
print(len(minimum.positions))

# for position in minimum.positions:
#     x, y = position
#     plan[x][y] = "O"

# print("\n".join("".join(row) for row in plan))
