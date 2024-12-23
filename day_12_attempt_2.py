data = """
AAAA
BBCD
BBCC
EEEC
""".strip()

data = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""".strip()

data = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
""".strip()

data = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
""".strip()

data = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".strip()

with open("input_12", "r") as file:
    data = file.read().strip()

plan = [[letter for letter in row] for row in data.splitlines()]

letters = set(data) - set("\n")

class Region:
    def __init__(self, letter):
        self.letter = letter
        self.points = set()
    
    def add(self, point):
        self.points.add(point)

    def can_accept(self, letter, point):
        if letter != self.letter:
            return False
        row, col = point
        return (
            (row-1, col) in self.points or 
            (row+1, col) in self.points or
            (row, col-1) in self.points or
            (row, col+1) in self.points
        )
    
    def can_merge_with(self, another):
        if self is another:
            return False
        if self.letter != another.letter:
            return False
        return any(self.can_accept(another.letter, point) for point in another.points)
    
    def merge(self, another):
        assert self.letter == another.letter
        self.points.update(another.points)
    
    def area(self):
        return len(self.points)
    
    def perimeter(self, plan):
        perimeter = 0
        for i, j in self.points:
            if (not 0 <= i - 1 < len(plan)) or plan[i - 1][j] != self.letter:
                perimeter += 1
            if (not 0 <= i + 1 < len(plan)) or plan[i + 1][j] != self.letter:
                perimeter += 1
            if (not 0 <= j - 1 < len(plan[i])) or plan[i][j - 1] != self.letter:
                perimeter += 1
            if (not 0 <= j + 1 < len(plan[i])) or plan[i][j + 1] != self.letter:
                perimeter += 1
        return perimeter
    
    def perimeter_points(self, plan):
        perimeter_points = set()
        for i, j in self.points:
            if (((not 0 <= i - 1 < len(plan)) or plan[i - 1][j] != self.letter) or
            ((not 0 <= i + 1 < len(plan)) or plan[i + 1][j] != self.letter) or
            ((not 0 <= j - 1 < len(plan[i])) or plan[i][j - 1] != self.letter) or
            ((not 0 <= j + 1 < len(plan[i])) or plan[i][j + 1] != self.letter)):
                perimeter_points.add((i, j))
        return perimeter_points
    
    def sides(self, plan):
        # Scan all sides and do something similar to find_ranges in attempt 1.
        points = sorted(self.points)
        rows = dict()  # row: list[int]
        for point in points:
            if point[0] in rows:
                rows[point[0]].append(point[1])
            else:
                rows[point[0]] = [point[1]]

        sides = 0 

        # Count sides "above".
        for row in rows:
            scanning_side = False
            cols = rows[row]
            i = 0

            while i < len(cols):
                if scanning_side and (cols[i] - cols[i-1] > 1):
                    scanning_side = False
                    sides += 1
                if (not (0 <= row-1 < len(plan))) or plan[row-1][cols[i]] != self.letter:
                    scanning_side = True
                else:
                    if scanning_side:
                        sides += 1
                    scanning_side = False
                i += 1
            
            if scanning_side:
                sides += 1
        
        # Count sides "below"
        for row in rows:
            scanning_side = False
            cols = rows[row]
            i = 0

            while i < len(cols):
                if scanning_side and (cols[i] - cols[i-1] > 1):
                    scanning_side = False
                    sides += 1
                if (not (0 <= row+1 < len(plan))) or plan[row+1][cols[i]] != self.letter:
                    scanning_side = True
                else:
                    if scanning_side:
                        sides += 1
                    scanning_side = False
                i += 1
            
            if scanning_side:
                sides += 1

        # Repeat the same but column wise. Sort by column, then by row.
        points = sorted(self.points, key=lambda point: (point[1], point[0]))
        cols = dict()  # col: list[int]
        for point in points:
            if point[1] in cols:
                cols[point[1]].append(point[0])
            else:
                cols[point[1]] = [point[0]]
        
        # Count sides "to the left".
        for col in cols:
            scanning_side = False
            rows = cols[col]
            i = 0

            while i < len(rows):
                if scanning_side and (rows[i] - rows[i-1] > 1):
                    scanning_side = False
                    sides += 1
                if (not (0 <= col-1 < len(plan[rows[i]]))) or plan[rows[i]][col-1] != self.letter:
                    scanning_side = True
                else:
                    if scanning_side:
                        sides += 1
                    scanning_side = False
                i += 1
            
            if scanning_side:
                sides += 1
        
        # Count sides "to the right".
        for col in cols:
            scanning_side = False
            rows = cols[col]
            i = 0

            while i < len(rows):
                if scanning_side and (rows[i] - rows[i-1] > 1):
                    scanning_side = False
                    sides += 1
                if (not (0 <= col+1 < len(plan[rows[i]]))) or plan[rows[i]][col+1] != self.letter:
                    scanning_side = True
                else:
                    if scanning_side:
                        sides += 1
                    scanning_side = False
                i += 1
            
            if scanning_side:
                sides += 1

        return sides
    
regions = list()
for i, row in enumerate(plan):
    for j, letter in enumerate(row):
        for region in regions:
            if region.can_accept(letter, (i, j)):
                region.add((i, j))
                break
        else:
            new_region = Region(letter)
            new_region.add((i, j))
            regions.append(new_region)

while any(
    region.can_merge_with(another_region)
    for region in regions
    for another_region in regions
):
    i = 0
    while i < len(regions):
        j = i + 1
        while j < len(regions):
            if regions[i].can_merge_with(regions[j]):
                regions[i].merge(regions[j])
                del regions[j]
            j += 1
        i += 1


# price = sum(region.area() * region.perimeter(plan) for region in regions)
price = sum(region.area() * region.sides(plan) for region in regions)
print(price)
