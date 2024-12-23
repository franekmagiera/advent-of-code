from enum import Enum, StrEnum

data = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""".strip()


data = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()

with open("input_15", "r") as file:
    data = file.read()

area, moves = data.split("\n\n")

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def next(self, position: tuple[int, int]) -> tuple[int, int]:
        x, y = position
        match self:
            case Direction.UP:
                return x-1, y
            case Direction.RIGHT:
                return x, y+1
            case Direction.DOWN:
                return x+1, y
            case Direction.LEFT:
                return x, y-1

def map_direction(char: str) -> Direction:
    match char:
        case "<":
            return Direction.LEFT
        case "v":
            return Direction.DOWN
        case ">":
            return Direction.RIGHT
        case "^":
            return Direction.UP

class Element(StrEnum):
    WALL = "#"
    BOX = "O"
    SPACE = "."
    ROBOT = "@"

area = [[Element(char) for char in row] for row in area.splitlines()]
moves = [map_direction(char) for char in moves if not char.isspace()]

def area_as_str(area) -> str:
    return "\n".join("".join(row) for row in area)

def find_robot(area) -> tuple[int, int] | None:
    for i, row in enumerate(area):
        for j, el in enumerate(row):
            if el is Element.ROBOT:
                return i, j
    return None

robot = find_robot(area)

def find_next_free_space(initial_x, initial_y, area, direction) -> tuple[int, int] | None:
    assert area[initial_x][initial_y] is Element.BOX

    x, y = initial_x, initial_y
    # Don't bother checking the limits of the map, we should run into a wall earlier.
    while area[x][y] is Element.BOX:
        x, y = direction.next((x, y))
    if area[x][y] is Element.WALL:
        return None
    return x, y

for direction in moves:
    x, y = robot
    next_x, next_y = direction.next(robot)
    match area[next_x][next_y]:
        case Element.WALL:
            continue
        case Element.SPACE:
            # Clear space after the robot.
            area[x][y] = Element.SPACE
            # Move the robot.
            area[next_x][next_y] = Element.ROBOT
            robot = (next_x, next_y)
        case Element.BOX:
            next_free_space = find_next_free_space(next_x, next_y, area, direction)
            if next_free_space is not None:
                # Clear space after the robot.
                area[x][y] = Element.SPACE
                # Move the robot.
                area[next_x][next_y] = Element.ROBOT
                robot = (next_x, next_y)
                # Move the box.
                free_space_x, free_space_y = next_free_space
                area[free_space_x][free_space_y] = Element.BOX
        case Element.ROBOT:
            raise RuntimeError("Unexpected another robot")

def compute_gps_coordinates(position: tuple[int, int]):
    x, y = position
    return 100 * x + y

print(area_as_str(area))

result = sum(
    compute_gps_coordinates((i, j))
    for i, row in enumerate(area)
    for j, el in enumerate(row)
    if el is Element.BOX)

print(result)

# Part 2

data = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()

with open("input_15", "r") as file:
    data = file.read()

area, moves = data.split("\n\n")

def resize_area(area: str) -> str:
    resized_area = ""

    for char in area:
        match char:
            case "#":
                resized_area += "##"
            case "O":
                resized_area += "[]"
            case ".":
                resized_area += ".."
            case "@":
                resized_area += "@."
            case any_str:
                resized_area += any_str
    
    return resized_area

area = resize_area(area)

area = [[char for char in row] for row in area.splitlines()]
moves = [map_direction(char) for char in moves if not char.isspace()]

def find_robot(area) -> tuple[int, int] | None:
    for i, row in enumerate(area):
        for j, el in enumerate(row):
            if el == "@":
                return i, j
    return None

robot = find_robot(area)

def find_next_free_space_vertically(initial_x, initial_y, area, direction):
    assert direction is Direction.LEFT or direction is Direction.RIGHT
    assert area[initial_x][initial_y] in ["[", "]"]

    x, y = initial_x, initial_y
    # Don't bother checking the limits of the map, we should run into a wall earlier.
    while area[x][y] in ["[", "]"]:
        x, y = direction.next((x, y))
    if area[x][y] == "#":
        return None
    return x, y

# Shamlessly copy pasted for up and down conditions.
def can_push_up(initial_x, initial_y, area):
    if area[initial_x][initial_y] == ".":
        return True
    if area[initial_x][initial_y] == "[":
        return (can_push_up(initial_x - 1, initial_y, area) and can_push_up(initial_x - 1, initial_y + 1, area))
    if area[initial_x][initial_y] == "]":
        return (can_push_up(initial_x - 1, initial_y, area) and can_push_up(initial_x - 1, initial_y - 1, area))
    return False

def can_push_down(initial_x, initial_y, area):
    if area[initial_x][initial_y] == ".":
        return True
    if area[initial_x][initial_y] == "[":
        return (can_push_down(initial_x + 1, initial_y, area) and can_push_down(initial_x + 1, initial_y + 1, area))
    if area[initial_x][initial_y] == "]":
        return (can_push_down(initial_x + 1, initial_y, area) and can_push_down(initial_x + 1, initial_y - 1, area))
    return False
        
def push_up(x, y, mover_y, area):
    if area[x][y] == ".":
        area[x][y] = area[x+1][y]
    elif area[x][y] == "[":
        push_up(x - 1, y, y, area)
        push_up(x - 1, y + 1, y, area)
        area[x][y] = area[x+1][y]
        if y+1 != mover_y:
            area[x][y+1] = "."
        else:
            area[x][y+1] = area[x+1][y+1]
    elif area[x][y] == "]":
        push_up(x - 1, y, y, area)
        push_up(x - 1, y - 1, y, area)
        area[x][y] = area[x+1][y]
        if y-1 != mover_y:
            area[x][y-1] = "."
        else:
            area[x][y-1] = area[x+1][y-1]

def push_down(x, y, mover_y, area):
    if area[x][y] == ".":
        area[x][y] = area[x-1][y]
    elif area[x][y] == "[":
        push_down(x + 1, y, y, area)
        push_down(x + 1, y + 1, y, area)
        area[x][y] = area[x-1][y]
        if y+1 != mover_y:
            area[x][y+1] = "."
        else:
            area[x][y+1] = area[x-1][y+1]
    elif area[x][y] == "]":
        push_down(x + 1, y, y, area)
        push_down(x + 1, y - 1, y, area)
        area[x][y] = area[x-1][y]
        if y-1 != mover_y:
            area[x][y-1] = "."
        else:
            area[x][y-1] = area[x-1][y-1]

for direction in moves:
    x, y = robot
    next_x, next_y = direction.next(robot)
    match area[next_x][next_y]:
        case "#":
            continue
        case ".":
            # Clear space after the robot.
            area[x][y] = "."
            # Move the robot.
            area[next_x][next_y] = "@"
            robot = (next_x, next_y)
        case "[" | "]":
            assert (
                area[next_x][next_y] == "[" and direction is Direction.RIGHT or
                area[next_x][next_y] == "]" and direction is Direction.LEFT or
                direction is Direction.UP or direction is Direction.DOWN
            )

            if direction is Direction.LEFT or direction is Direction.RIGHT:
                next_free_space = find_next_free_space_vertically(next_x, next_y, area, direction)
                if next_free_space is not None:
                    # Move the boxes.
                    free_space_x, free_space_y = next_free_space
                    if direction is Direction.LEFT:
                        area[free_space_x][free_space_y:next_y] = area[free_space_x][free_space_y+1:next_y+1]
                    else:
                        assert direction is Direction.RIGHT
                        area[free_space_x][next_y+1:free_space_y+1] = area[free_space_x][next_y:free_space_y]
                    # Clear space after the robot.
                    area[x][y] = "."
                    # Move the robot.
                    area[next_x][next_y] = "@"
                    robot = (next_x, next_y)
            else:
                assert direction is Direction.UP or direction is Direction.DOWN
                if direction is Direction.UP and can_push_up(next_x, next_y, area):
                    push_up(next_x, next_y, y, area)
                    robot = (next_x, next_y)
                    # Clear space after the robot.
                    area[x][y] = "."
                if direction is Direction.DOWN and can_push_down(next_x, next_y, area):
                    push_down(next_x, next_y, y, area)
                    robot = (next_x, next_y)
                    # Clear space after the robot.
                    area[x][y] = "."
        case Element.ROBOT:
            raise RuntimeError("Unexpected another robot")

def area_as_str(area) -> str:
    return "\n".join("".join(row) for row in area)

print(area_as_str(area))
result = sum(
    compute_gps_coordinates((i, j))
    for i, row in enumerate(area)
    for j, el in enumerate(row)
    if el == "["
)
print(result)
