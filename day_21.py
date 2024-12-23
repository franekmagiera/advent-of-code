from enum import Enum
import re

data = """
029A
980A
179A
456A
379A
""".strip()

# data = """
# 319A
# 985A
# 340A
# 489A
# 964A
# """.strip()

codes = data.splitlines()

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
numeric_keypad = [
    [ "7", "8",  "9"],
    [ "4", "5",  "6"],
    [ "1", "2",  "3"],
    [  -1, "0",  "A"]
]

class Action(Enum):
    UP    = 1,
    DOWN  = 2,
    LEFT  = 3,
    RIGHT = 4,
    PRESS = 5,

    def as_str(self):
        match self:
            case Action.UP:
                return "^"
            case Action.DOWN:
                return "v"
            case Action.LEFT:
                return "<"
            case Action.RIGHT:
                return ">"
            case Action.PRESS:
                return "A"


#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
directional_keypad = [
    [         -1,   Action.UP, Action.PRESS],
    [Action.LEFT, Action.DOWN, Action.RIGHT]
]

def find_actions(sequence, initial_position, keypad):
    x, y = initial_position
    assert within_limits(x, y, keypad)

    keypad_coordinates = {sign: (i, j) for i, row in enumerate(keypad) for j, sign in enumerate(row)}
    avoid_x, avoid_y = keypad_coordinates[-1]
    actions = []

    for sign in sequence:
        desired_x, desired_y = keypad_coordinates[sign]

        horizontal_difference = desired_y - y
        direction = Action.LEFT if horizontal_difference < 0 else Action.RIGHT
        horizontal_actions = [direction] * abs(horizontal_difference) if horizontal_difference != 0 else []

        vertical_difference = desired_x - x
        direction = Action.UP if vertical_difference < 0 else Action.DOWN
        vertical_actions = [direction] * abs(vertical_difference) if vertical_difference != 0 else []

        if x == avoid_x:
            actions += vertical_actions
            actions += horizontal_actions
        else:
            actions += horizontal_actions
            actions += vertical_actions
        
        
        actions.append(Action.PRESS)
        x, y = desired_x, desired_y

    return actions

def within_limits(x, y, array):
    return 0 <= x < len(array) and 0 <= y < len(array[0])

# numeric_keypad_initial_position = (3, 2)
# actions = find_actions("179A", numeric_keypad_initial_position, numeric_keypad)
# for action in actions:
#     print(action, end = " ")
#     if action is Action.PRESS:
#         print("\n", end="")

# print("---")
# directional_keypad_initiial_position = (0, 2)
# actions = find_actions(actions, directional_keypad_initiial_position, directional_keypad)
# for action in actions:
#     print(action, end = " ")
#     if action is Action.PRESS:
#         print("\n", end="")

def find_final_actions(sequence, directional_keypads):
    numeric_keypad_initial_position = (3, 2)
    actions = find_actions(sequence, numeric_keypad_initial_position, numeric_keypad)

    directional_keypad_initial_position = (0, 2)
    for _ in range(directional_keypads - 1):
        actions = find_actions(actions, directional_keypad_initial_position, directional_keypad)
    return actions

def get_numeric_part(code):
    pattern = re.compile(r"(\d+)[a-zA-Z]")
    match = pattern.match(code)
    return int(match.group(1))

directional_keypads = 3
total_complexity = sum(
    len(find_final_actions(code, directional_keypads)) * get_numeric_part(code)
    for code in codes
)
print(total_complexity)

complexities = [
    (len(find_final_actions(code, directional_keypads)), get_numeric_part(code))
    for code in codes
]
print(complexities)

# 219314 too high

# --- 2nd approach
def find_actions(sequence, initial_position, keypad):
    x, y = initial_position
    assert within_limits(x, y, keypad)

    keypad_coordinates = {sign: (i, j) for i, row in enumerate(keypad) for j, sign in enumerate(row)}
    actions = []

    for sign in sequence:
        desired_x, desired_y = keypad_coordinates[sign]

        action = {}
        horizontal_difference = desired_y - y
        direction = Action.LEFT if horizontal_difference < 0 else Action.RIGHT
        if horizontal_difference != 0:
            action[direction] = abs(horizontal_difference)  # How many times to perform a given step.

        vertical_difference = desired_x - x
        direction = Action.UP if vertical_difference < 0 else Action.DOWN
        if vertical_difference != 0:
            action[direction] = abs(vertical_difference)
        
        actions.append(action)
        x, y = desired_x, desired_y

    return actions

def taxicab_distance(a, b):
    x_a, y_a = a
    x_b, y_b = b
    return abs(x_a - x_b) + abs(y_a - y_b)

# Tries to find the best combination to perform given actions on a directional keypad.
def find_best_combination(actions, initial_position, keypad, next_initial_position, next_keypad):
    x, y = initial_position
    assert within_limits(x, y, keypad)
    next_x, next_y = next_initial_position
    assert within_limits(next_x, next_y, next_keypad)

    keypad_coordinates = {sign: (i, j) for i, row in enumerate(keypad) for j, sign in enumerate(row)}
    next_keypad_coordinates = {sign: (i, j) for i, row in enumerate(next_keypad) for j, sign in enumerate(row)}
    next_avoid_x, next_avoid_y = next_keypad_coordinates[-1]

    presses = []
    for moves in actions:
        # I might have a couple of moves to do.
        # They should always end with an Action.PRESS.
        # Let's try a heurestic where I just move to the closest move
        # from where I'm currently at, while avoiding the gap.
        while moves:
            _, _, closest_move = min(
                (
                    taxicab_distance(keypad_coordinates[move], (x, y)),
                    i,
                    move
                )
                for i, move in enumerate(moves)
            )
            assert closest_move in (Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN)
            times = moves.pop(closest_move)
            if closest_move is Action.LEFT or closest_move is Action.RIGHT:
                next_final_x = next_x
                next_final_y = next_y + (-1 if closest_move is Action.LEFT else 1) * times
            if closest_move is Action.UP or closest_move is Action.DOWN:
                next_final_x = next_x + (-1 if closest_move is Action.UP else 1) * times
                next_final_y = next_y
            # Pick next closest button if pressing the closest one would go through
            # the gap.
            # if (
            #     # I can make use of the fact that I can't go "through" the gap
            #     (next_final_x, next_final_y) == (next_avoid_x, next_avoid_y)
            #     # next_final_x == next_x and next_avoid_y in range(min(next_y, next_final_y)+1, max(next_y, next_final_y))
            #     # or next_final_y == next_y and next_avoid_x in range(min(next_x, next_final_x)+1, max(next_x, next_final_x))
            # ):
            #     # This should always find some other minimum.
            #     assert moves
            #     _, next_closest_move = min(
            #         (taxicab_distance(keypad_coordinates[move], (x, y)), move)
            #         for move in moves
            #     )
            #     moves[closest_move] = times
            #     closest_move = next_closest_move
            #     times = moves.pop(closest_move)
            #     if closest_move is Action.LEFT or closest_move is Action.RIGHT:
            #         next_final_x = next_x
            #         next_final_y = next_y + (-1 if closest_move is Action.LEFT else 1) * times
            #     if closest_move is Action.UP or closest_move is Action.DOWN:
            #         next_final_x = next_x + (-1 if closest_move is Action.UP else 1) * times
            #         next_final_y = next_y
            
            # Now, just perform the closest_move specified amount of times.
            presses += [closest_move] * times
            x, y = keypad_coordinates[closest_move]
            next_x, next_y = next_final_x, next_final_y
        presses.append(Action.PRESS)
    return presses

# print(
#     find_best_combination(
#         find_actions("029A", (3, 2), numeric_keypad),
#         (0, 2),
#         directional_keypad,
#         (3, 2),
#         numeric_keypad
#     )
# )

def find_final_actions(sequence, directional_keypads):
    numeric_keypad_initial_position = (3, 2)
    directional_keypad_initial_position = (0, 2)
    actions = find_actions(sequence, numeric_keypad_initial_position, numeric_keypad)
    actions = find_best_combination(
        actions,
        directional_keypad_initial_position,
        directional_keypad,
        numeric_keypad_initial_position,
        numeric_keypad
    )

    for _ in range(directional_keypads - 1):
        actions = find_actions(actions, directional_keypad_initial_position, directional_keypad)
        actions = find_best_combination(
            actions,
            directional_keypad_initial_position,
            directional_keypad,
            directional_keypad_initial_position,
            directional_keypad
        )
    return actions

def get_numeric_part(code):
    pattern = re.compile(r"(\d+)[a-zA-Z]")
    match = pattern.match(code)
    return int(match.group(1))

directional_keypads = 3
total_complexity = sum(
    len(find_final_actions(code, directional_keypads)) * get_numeric_part(code)
    for code in codes
)
print(total_complexity)

complexities = [
    (len(find_final_actions(code, directional_keypads)), get_numeric_part(code))
    for code in codes
]
print(complexities)

# 216734 too high

# 215374 was just right, both of the approaches above do not work, I just chose the minimum from
# both methods for each codes and somehow it was the right result.

# But seeing the Part 2, I guess I need to rethink my approach anyways, even this wrong solution takes too long.

# -----

# Attempt 3

import itertools

def check_permutation(permutation, moves, keypad, initial_position):
    keypad_coordinates = {sign: (i, j) for i, row in enumerate(keypad) for j, sign in enumerate(row)}
    avoid_x, avoid_y = keypad_coordinates[-1]
    x, y = initial_position
    if (x, y) == (avoid_x, avoid_y):
        return False
    # if (x, y) != start_and_end:
    #     return False
    for move in permutation:
        if move is Action.LEFT or move is Action.RIGHT:
            y = y + (-1 if move is Action.LEFT else 1) * moves[move]
        if move is Action.UP or move is Action.DOWN:
            x = x + (-1 if move is Action.UP else 1) * moves[move]
        if (x, y) == (avoid_x, avoid_y):
            return False
    # if (x, y) != start_and_end:
    #     return False

    return True


def find_best_combination(actions, initial_position, keypad, next_initial_position, next_keypad):
    keypad_coordinates = {sign: (i, j) for i, row in enumerate(keypad) for j, sign in enumerate(row)}

    presses = []
    for moves in actions:
        # I might have a couple of moves to do.
        # They should always end with an Action.PRESS.
        
        # Figure out the best order of moves so that the distance travelled is smallest.
        if len(moves) == 1:
            best_moves = [move for move in moves]
        elif len(moves) == 0:
            best_moves = []
        else:
            _, _, best_moves = min(
                (taxicab_distance(keypad_coordinates[pair[0]], keypad_coordinates[pair[1]]), i, permutation)
                for i, permutation in enumerate(itertools.permutations([move for move in moves]))
                if check_permutation(permutation, moves, next_keypad, next_initial_position)
                for pair in zip(permutation, [Action.PRESS] + list(permutation[1:]))
            )
        for move in best_moves:
            presses += [move] * moves[move]
        presses.append(Action.PRESS)
    return presses


# print(
#     find_best_combination(
#         find_actions("029A", (3, 2), numeric_keypad),
#         (0, 2),
#         directional_keypad,
#         (3, 2),
#         numeric_keypad
#     )
# )

def find_final_actions(sequence, directional_keypads):
    numeric_keypad_initial_position = (3, 2)
    directional_keypad_initial_position = (0, 2)
    actions = find_actions(sequence, numeric_keypad_initial_position, numeric_keypad)
    actions = find_best_combination(
        actions,
        directional_keypad_initial_position,
        directional_keypad,
        numeric_keypad_initial_position,
        numeric_keypad
    )

    for _ in range(directional_keypads - 1):
        actions = find_actions(actions, directional_keypad_initial_position, directional_keypad)
        actions = find_best_combination(
            actions,
            directional_keypad_initial_position,
            directional_keypad,
            directional_keypad_initial_position,
            directional_keypad
        )
    return actions

directional_keypads = 3
total_complexity = sum(
    len(find_final_actions(code, directional_keypads)) * get_numeric_part(code)
    for code in codes
)
print(total_complexity)

complexities = [
    (len(find_final_actions(code, directional_keypads)), get_numeric_part(code))
    for code in codes
]
print(complexities)

# Still nothing works...

# Hints from Reddit:
# It's possible to solve without recursion. I'll repost my hints here =) The
# important observation to start with is that when you are moving a nested
# keypad from button X to go press button Y, the last thing you did was press X,
# and the last thing you will do is press Y. So all the keypads above start
# resting on button A and end resting on button A again!  So, this means the
# cost of moving keypad 5 from X to Y doesn't depend on where the robot arm is
# on the parent keypads 1, 2, 3, 4, you know they're all always in the same
# fixed spot So, you can forget about all the keypads two levels above entirely,
# the cost to move on the current keypad only depends on the the state of the
# current keypad + the costs to move from A to X, Y, Z, and back to A on the
# parent keypad. And the costs for the parent don't depend on the state of
# anything above, because we know that state above is always the same after each
# step, resting on button A.  With those hints, there's a strategy that works
# without any recursion and with the same small memory cost, no matter how many
# keypads are chained: you can pre-compute all the shortest
# https://www.reddit.com/r/adventofcode/comments/1hj8380/comment/m34g89j/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
