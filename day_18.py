import heapq
import itertools

data = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""".strip()

HEIGHT = 7
WIDTH = 7
N = 12

with open("input_18", "r") as file:
    data = file.read().strip()

HEIGHT = 71  # 71
WIDTH = 71  # 71
N = 1024 #  1024

plan = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

bytes = list(
    (int(coordinates[0]), int(coordinates[1]))
    for coordinates in (
        line.split(",")
        for line in data.splitlines()
        ))


for byte in bytes[:N]:
    y, x = byte
    plan[x][y] = "#"

end_x, end_y = (HEIGHT-1, WIDTH-1)

def plan_as_str(plan):
    return "\n".join("".join(element for element in row) for row in plan)

# print(plan_as_str(plan))

# ---
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
for row in range(HEIGHT):
    for col in range(WIDTH):
        if (row, col) == (0, 0):
            unvisited.add((row, col), priority=0)
        else:
            unvisited.add((row, col), priority=float("inf"))

def get_neighbors(x, y, WIDTH, HEIGHT):
    return list(
        (row, col)
        for row, col in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        if within_limits(row, col, WIDTH, HEIGHT)
    )

def within_limits(x, y, WIDTH, HEIGHT):
    return 0 <= x < HEIGHT and 0 <= y < WIDTH

while current_node := unvisited.pop():
    steps, coordinates = current_node
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
            continue
        neighbor_x, neighbor_y = neighbor
        if plan[neighbor_x][neighbor_y] == "#":
            # Keep the inifinite steps, cannot go there.
            continue
        # Should be there, chacked a couple of lines above.
        neighbor_steps = unvisited.get_priority(neighbor)
        if steps + 1 < neighbor_steps:
            unvisited.add((neighbor_x, neighbor_y), steps+1)

print(steps)


# Part 2
def clear_plan(width, height):
    return [["." for _ in range(width)] for _ in range(height)]

plan = clear_plan(WIDTH, HEIGHT)

# I did binary search by hand
# pivot = len(bytes) // 2 + len(bytes) // 4 + len(bytes) // 8 
# Lower 2856
# Upper 2910
# pivot = 2856
# print(pivot)
for i in range(2856, 2910):
    plan = clear_plan(WIDTH, HEIGHT)
    for byte in bytes[:i+1]:
        y, x = byte
        plan[x][y] = "#"
    
    unvisited = PriorityQueue()
    for row in range(HEIGHT):
        for col in range(WIDTH):
            if (row, col) == (0, 0):
                unvisited.add((row, col), priority=0)
            else:
                unvisited.add((row, col), priority=float("inf"))

    while current_node := unvisited.pop():
        steps, coordinates = current_node
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
                continue
            neighbor_x, neighbor_y = neighbor
            if plan[neighbor_x][neighbor_y] == "#":
                # Keep the inifinite steps, cannot go there.
                continue
            # Should be there, chacked a couple of lines above.
            neighbor_steps = unvisited.get_priority(neighbor)
            if steps + 1 < neighbor_steps:
                unvisited.add((neighbor_x, neighbor_y), steps+1)
    
    if current_node is None or steps == float("inf"):
        print(i, bytes[i])
        break
print(steps)
