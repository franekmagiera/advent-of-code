import heapq
import itertools

data = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".strip()

with open("input_20", "r") as file:
    data = file.read().strip()

# data = """
# ###############
# #...#........E#
# #.#.#########.#
# #.#.#########.#
# #.#.#########.#
# #.#.#########.#
# #.#.#########.#
# #.#.#########.#
# #S#...........#
# ###############
# """.strip()

def get_initial_plan(data):
    return [[char for char in row] for row in data.splitlines()]

plan = get_initial_plan(data)

HEIGHT = len(plan)
WIDTH = len(plan[0])

def find_sign(sign, plan):
    for i, row in enumerate(plan):
        for j, el in enumerate(row):
            if el == sign:
                return i, j
    return None

start = find_sign("S", plan)
assert start is not None
start_x, start_y = start

end = find_sign("E", plan)
assert end is not None
end_x, end_y = end

def plan_as_str(plan):
    return "\n".join("".join(element for element in row) for row in plan)

# print(plan_as_str(plan))

class PriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.removed = "<removed-task>"
        self.counter = itertools.count()
    
    def add(self, element, priority=0):
        if element in self.entry_finder:
            self.remove(element)
        count = next(self.counter)
        entry = [priority, count, element]
        self.entry_finder[element] = entry
        heapq.heappush(self.pq, entry)
    
    def remove(self, element):
        entry = self.entry_finder.pop(element)
        entry[-1] = self.removed
    
    def pop(self):
        while self.pq:
            priority, count, element = heapq.heappop(self.pq)
            if element is not self.removed:
                del self.entry_finder[element]
                return priority, element
        return None
    
    def contains(self, element):
        return element in self.entry_finder
    
    def get_priority(self, element):
        if element in self.entry_finder:
            priority, _, _ = self.entry_finder[element]
            return priority
        return None

unvisited = PriorityQueue()
for i, row in enumerate(plan):
    for j, el in enumerate(row):
        if (i, j) == start:
            unvisited.add((i, j), priority=0)
        else:
            unvisited.add((i, j), priority=float("inf"))

def get_neighbors(x, y, width, height):
    return list(
        (row, col)
        for row, col in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        if within_limits(row, col, width, height)
    )

def within_limits(x, y, width, height):
    return 0 <= x < height and 0 <= y < width

visited = dict()  # position: cost
while current_node := unvisited.pop():
    steps, coordinates = current_node
    visited[coordinates] = steps
    x, y = coordinates
    if steps == float("inf"):
        break
    if plan[x][y] == "#":
        continue
    if (x, y) == (end_x, end_y):
        break
    neighbors = get_neighbors(x, y, WIDTH, HEIGHT)
    for neighbor in neighbors:
        if not unvisited.contains(neighbor):
            # If already visited that node, continue.
            continue
        neighbor_x, neighbor_y = neighbor
        if plan[neighbor_x][neighbor_y] == "#":
            # Keep the inifinite steps, cannot go there.
            continue
        # Should be there, chacked a couple of lines above.
        neighbor_steps = unvisited.get_priority(neighbor)
        if steps + 1 < neighbor_steps:
            unvisited.add((neighbor_x, neighbor_y), steps+1)

# Just copy pasted the code above...
# ---
best_path_cache = {}
def find_best_path(start, plan, width, height):  # Returns cost to the finish
    if start in best_path_cache:
        return best_path_cache[start]

    unvisited = PriorityQueue()
    for i, row in enumerate(plan):
        for j, el in enumerate(row):
            if (i, j) == start:
                unvisited.add((i, j), priority=0)
            else:
                unvisited.add((i, j), priority=float("inf"))

    visited = dict()  # position: cost
    while current_node := unvisited.pop():
        steps, coordinates = current_node
        visited[coordinates] = steps
        x, y = coordinates
        if steps == float("inf"):
            break
        if plan[x][y] == "#":
            continue
        if (x, y) == (end_x, end_y):
            break
        neighbors = get_neighbors(x, y, width, height)
        for neighbor in neighbors:
            if not unvisited.contains(neighbor):
                # If already visited that node, continue.
                continue
            neighbor_x, neighbor_y = neighbor
            if plan[neighbor_x][neighbor_y] == "#":
                # Keep the inifinite steps, cannot go there.
                continue
            # Should be there, chacked a couple of lines above.
            neighbor_steps = unvisited.get_priority(neighbor)
            if steps + 1 < neighbor_steps:
                unvisited.add((neighbor_x, neighbor_y), steps+1)
    
    best_path_cache[start] = steps
    return steps
# ---

# Now find the best path.
path = { start: visited[start] }
path_list = [ start ]  # Guess could use an OrderedDict for that...
node = start
while node != end:
    x, y = node
    neighbors = get_neighbors(x, y, WIDTH, HEIGHT)
    # Find next node with minimum cost.
    cost, node = min(
        (visited[neighbor], neighbor)
        for neighbor in neighbors
        if neighbor in visited and neighbor not in path)
    path[node] = cost
    path_list.append(node)

# ---
# Just print the path.
# for node in path:
#     x, y = node
#     plan[x][y] = "O"

# plan[start_x][start_y] = "S"
# plan[end_x][end_y] = "E"

# print(plan_as_str(plan))
# print(steps)
# ---

# Now, I have the best path.
# I can cheat by going through a wall.
# For every point on a path I can get all possible cheats.
# The diff between the costs is how much I gain.

def get_cheats(x, y, width, height, plan):  # Retruns [(x_1, y_1), (x_2, y_2)]
    # First neighbour has to be a wall for a cheat to make sense.
    first_neighbors = (
        (neighbor_x, neighbor_y)
        for neighbor_x, neighbor_y in get_neighbors(x, y, width, height)
        if plan[neighbor_x][neighbor_y] == "#"
    )
    cheats = (
        ((neighbor_x, neighbor_y), (second_neighbor_x, second_neighbor_y))
        for neighbor_x, neighbor_y in first_neighbors
        for second_neighbor_x, second_neighbor_y in get_neighbors(neighbor_x, neighbor_y, width, height)
        if (plan[second_neighbor_x][second_neighbor_y] != "#"  # Doesn't make sense to go into another wall.
            and (second_neighbor_x, second_neighbor_y) != (x, y))  # Doesn't make sense to come back to the inital position.
    )
    return list(cheats)

possible_cheats = dict()  # time: count of cheats

i = 0 # path_list.index((7, 9))
finish = i + 1
while i < len(path_list) - 1:
# while i < finish:
    node = path_list[i]
    # print(node)
    x, y = node
    next_node = path_list[i + 1]
    # print(next_node)

    cheats = get_cheats(x, y, WIDTH, HEIGHT, plan)
    # print(cheats)
    for cheat in cheats:
        _, final_position = cheat
        # print(final_position)
        time_to_finish_from_next_node = path[path_list[-1]] - path[next_node]
        # print(time_to_finish_from_next_node)
        if final_position in path:
            # Maybe it doesn't have to be on the initial best path to get a better final result.
            # But I can just do Dijkstra from the cheat to the end.
            # For the initial small example I can do it I think.
            time_to_finish_by_cheating = path[path_list[-1]] - path[final_position] + 1  
        # ---
        else:
            time_to_finish_by_cheating = 2 + find_best_path(final_position, plan, WIDTH, HEIGHT)
        # ---
            # print(time_to_finish_by_cheating)
        if time_to_finish_by_cheating < time_to_finish_from_next_node:
            time_saved = time_to_finish_from_next_node - time_to_finish_by_cheating
            # print("time_saved", time_saved)
            if time_saved not in possible_cheats:
                possible_cheats[time_saved] = 0
            possible_cheats[time_saved] += 1
        # else:
            # Here I can handle this case when I get outside of the initial best path...
            # find_best_path(start, plan, width, height)
            ...
    i += 1

# print(sorted((cheat, possible_cheats[cheat]) for cheat in possible_cheats))
result = sum(possible_cheats[cheat] for cheat in possible_cheats if cheat >= 100)
print(result)

# Part 2
def taxicab_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

def get_cheats(x, y, width, height, plan):  # Returns list of points that has 20 taxicab distance from x, y.
    cheats = []
    for i in range(-21, 21):
        for j in range(-21, 21):
            new_x = x + i
            new_y = y + j
            if (
                taxicab_distance(x, y, new_x, new_y) <= 20 
                and within_limits(new_x, new_y, width, height)
                and (
                    plan[new_x][new_y] == "E"
                    or plan[new_x][new_y] == "."
                )
            ):
                cheats.append((new_x, new_y))
    return cheats

possible_cheats = dict()  # time: count of cheats

i = 0 # path_list.index((7, 9))
finish = i + 1
while i < len(path_list) - 1:
# while i < finish:
    node = path_list[i]
    # print(node)
    x, y = node
    next_node = path_list[i + 1]
    # print(next_node)

    cheats = get_cheats(x, y, WIDTH, HEIGHT, plan)
    # print(cheats)
    for cheat in cheats:
        final_position = cheat
        # print(final_position)
        time_to_finish_from_next_node = path[path_list[-1]] - path[next_node]
        # print(time_to_finish_from_next_node)
        cheat_distance = taxicab_distance(x, y, final_position[0], final_position[1])
        if final_position in path:
            # Maybe it doesn't have to be on the initial best path to get a better final result.
            # But I can just do Dijkstra from the cheat to the end.
            # For the initial small example I can do it I think.
            time_to_finish_by_cheating = path[path_list[-1]] - path[final_position] + cheat_distance - 1
        # ---
        else:
            # Thought after solving and going through Reddit:
            # Actually I completely missed the fact that there is only one valid path.
            # So no need to check that condition at all.
            time_to_finish_by_cheating = find_best_path(final_position, plan, WIDTH, HEIGHT) + cheat_distance
        # ---
            # print(time_to_finish_by_cheating)
        if time_to_finish_by_cheating < time_to_finish_from_next_node:
            time_saved = time_to_finish_from_next_node - time_to_finish_by_cheating
            # print("time_saved", time_saved)
            if time_saved not in possible_cheats:
                possible_cheats[time_saved] = 0
            possible_cheats[time_saved] += 1
        # else:
            # Here I can handle this case when I get outside of the initial best path...
            # find_best_path(start, plan, width, height)
            ...
    i += 1

# print(sorted((cheat, possible_cheats[cheat]) for cheat in possible_cheats if cheat >= 50))
result = sum(possible_cheats[cheat] for cheat in possible_cheats if cheat >= 100)
print(result)

# So actually no pathfidning was needed, because there is only one valid path.
