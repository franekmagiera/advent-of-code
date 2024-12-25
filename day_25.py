data = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
""".strip()

with open("input_25", "r") as file:
    data = file.read().strip()

HEIGHT = 7
WIDTH  = 5

keys = []
locks = []

for schematics in data.split("\n\n"):
    is_key = schematics.split("\n")[0] == WIDTH * "." 
    matrix = [[char for char in line] for line in schematics.splitlines()]
    heights = []
    for column in range(WIDTH):
        char = matrix[0][column]
        i = 1
        while i < HEIGHT and matrix[i][column] == char:
            i += 1
        heights.append(i)
    heights = [height - 1 for height in heights]
    if is_key:
        heights = [HEIGHT - 2 - height for height in heights]
        keys.append(heights)
    else:
        locks.append(heights)

def overlaps(key, lock, lock_height):
    return any(key_height + pin_height > lock_height - 2 for key_height, pin_height in zip(key, lock))

result = sum(not overlaps(key, lock, HEIGHT) for key in keys for lock in locks)
print(result)
