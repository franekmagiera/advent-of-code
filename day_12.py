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

class Range:
    # Both inclusive: it's a [left, right] range.
    def __init__(self, left, right):
        assert left <= right
        self.left = left
        self.right = right

    def overlaps(self, another: "Range") -> bool:
        return (
            (self.left <= another.right and self.right >= another.left) or 
            (another.left <= self.right and another.right >= self.left)
        )
    
    def length(self) -> int:
        return self.right - self.left + 1
    
    def __repr__(self) -> str:
        return f"Range({self.left}, {self.right})"
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Range):
            return self.left == value.left and self.right == value.right
        return False

assert Range(1, 5).overlaps(Range(2, 6))
assert Range(5, 8).overlaps(Range(1,6))
assert Range(1, 5).overlaps(Range(2, 3))
assert Range(2, 3).overlaps(Range(1, 5))
assert Range(1, 5).overlaps(Range(5, 8))
assert Range(5, 8).overlaps(Range(1, 5))
assert Range(7, 7).overlaps(Range(1, 8))
assert not Range(1, 3).overlaps(Range(4, 6))
assert not Range(4, 6).overlaps(Range(0, 2))
assert Range(7,7).overlaps(Range(6,7))


def find_ranges(letter, row) -> list[tuple[int, Range]]:
    ranges = []
    in_range = False
    range_start = -1
    for i, char in enumerate(row):
        if char == letter:
            if not in_range:
                in_range = True
                range_start = i
        elif char != letter:
            if in_range == True:
                ranges.append(Range(range_start, i-1))
            in_range = False
            range_start = -1
    if in_range:
        ranges.append(Range(range_start, len(row)-1))
    return ranges

assert find_ranges("A", ["A", "A", ".", ".", "A", "A", ".", "A"]) == [Range(0,1), Range(4,5), Range(7, 7)] 

class Region:
    def __init__(self):
        self.ranges = dict()
        self.min = None
        self.max = None
    
    def add(self, row, range):
        self.min = row if self.min is None else min(row, self.min)
        self.max = row if self.max is None else max(row, self.max)
        if row in self.ranges:
            self.ranges[row].append(range)
        else:
            self.ranges[row] = [range]
    
    def can_accept(self, row, range) -> bool:
        return (
            self.ranges.get(row - 1) and any(region_range.overlaps(range) for region_range in self.ranges.get(row - 1)) or
            self.ranges.get(row + 1) and any(region_range.overlaps(range) for region_range in self.ranges.get(row + 1)) or
            self.ranges.get(row) and any(region_range.overlaps(range) for region_range in self.ranges.get(row))
        )
    
    def can_merge_with(self, another) -> bool:
        return (
            another.ranges.get(self.min - 1) is not None and
            any(
                range.overlaps(another_range)
                for range in self.ranges.get(self.min)
                for another_range in another.ranges.get(self.min - 1)
            )
        ) or (
            another.ranges.get(self.max + 1) is not None and
            any(
                range.overlaps(another_range)
                for range in self.ranges.get(self.max)
                for another_range in another.ranges.get(self.max + 1)
            )
        ) or (
            self.ranges.get(another.min - 1) is not None and
            any(
                range.overlaps(another_range)
                for range in self.ranges.get(another.min - 1)
                for another_range in another.ranges.get(another.min)
            )
        ) or (
            self.ranges.get(another.max + 1) is not None and
            any(
                range.overlaps(another_range)
                for range in self.ranges.get(another.max + 1)
                for another_range in another.ranges.get(another.max)
            )
        )
    
    def merge_with(self, another):
        for row in another.ranges:
            for range in another.ranges[row]:
                if row in self.ranges:
                    self.ranges[row].append(range)
                else:
                    self.ranges[row] = [range]
    
    def area(self):
        return sum(
            range.length()
            for row in self.ranges
            for range in self.ranges[row]
        )
    
    def perimeter(self, letter, plan):
        perimeter = 0
        for row in self.ranges:
            for range in self.ranges[row]:
                j = range.left
                while j <= range.right:
                    if (not (0 <= row-1 < len(plan))) or (plan[row-1][j] != letter):
                        perimeter += 1
                    if (not (0 <= row+1 < len(plan))) or (plan[row+1][j] != letter):
                        perimeter += 1
                    if (not (0 <= j-1 < len(plan[row]))) or (plan[row][j-1] != letter):
                        perimeter += 1
                    if (not (0 <= j+1 < len(plan[row]))) or (plan[row][j+1] != letter):
                        perimeter += 1
                    j += 1
        return perimeter

recreated_plan = [[0 for _ in range(len(plan[i]))] for i in range(len(plan))]
price = 0
for letter in letters:
    regions = list()
    for i, row in enumerate(plan):
        ranges = find_ranges(letter, row)
        for range in ranges:
            for region in regions:
                if region.can_accept(i, range):
                    region.add(i, range)
                    break
            else:
                region = Region()
                region.add(i, range)
                regions.append(region)
        while any(
            region.can_merge_with(another_region)
            for region in regions
            for another_region in regions
        ):
            # Keep merging.
            i = 0
            while i < len(regions):
                j = i + 1
                while j < len(regions):
                    if regions[i].can_merge_with(regions[j]):
                        regions[i].merge_with(regions[j])
                        del regions[j]
                    j += 1
                i += 1
    area = sum(region.area() for region in regions)
    assert area == sum(1 for char in data if char == letter)
    price += sum(region.perimeter(letter, plan) * region.area() for region in regions)

    # Here recreate the data from regions.
    for region in regions:
        for row in region.ranges:
            for range in region.ranges[row]:
                j = range.left
                while j <= range.right:
                    recreated_plan[row][j] = letter
                    j += 1
    
    for region in regions:
        # Assert that every row overlaps with the next one.
        for row in region.ranges:
            if row+1 in region.ranges:
                assert any(
                    range.overlaps(another_range)
                    for range in region.ranges[row]
                    for another_range in region.ranges[row+1]
                )
    
    for region in regions:
        # Assert rows are in increasing order.
        i = region.min 
        while i <= region.max:
            assert i in region.ranges
            i += 1
    
    for region in regions:
        for row in region.ranges:
            sorted_ranges = sorted(region.ranges[row], key=lambda range: range.left)
            i = 0
            while i < len(sorted_ranges) - 1:
                assert sorted_ranges[i].right < sorted_ranges[i+1].left
                i += 1 

recreated_data = "\n".join(["".join(row) for row in recreated_plan])
with open("output_day_12", "w") as file:
    file.write(recreated_data)

assert recreated_plan == plan

print(price)

# 1452035 too low

# No idea why it's wrong.
