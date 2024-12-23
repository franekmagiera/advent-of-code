data = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()

with open("input_7", "r") as file:
    data = file.read().strip()

def parse_line(line: str) -> tuple[int, list[int]]:
    colon = line.index(":")
    test_value = int(line[:colon])
    numbers = [int(number) for number in line[colon+1:].split()]
    return (test_value, numbers)

equations: list[(int, list[int])] = [parse_line(line) for line in data.splitlines()]

# I will associate "going left" with addition (+) and
# "going" right with multiplication (*)
# class Node:
#     result_so_far: int
#     left: "Node" | None
#     right: "Node" | None

#     def __init__(self, result_so_far, left=None, right=None):
#         self.result_so_far = result_so_far
#         self.left = left
#         self.right = right
    
#     def is_viable(self) -> bool:
#         return True

# class Rejected(Node):
#     def __init__(self):
#         super().__init__(self, 0)
    
#     def is_viable(self) -> bool:
#         return False

# class Tree:
#     head: Node | None

#     def __init__(self):
#         self.head = None

# Or... I can keep a stack of leaves and process that stack everytime I want to add a new number.

viable_subsolutions = list() 

class Explorer:
    def __init__(self, goal: int, initial_value: int):
        self.viable_subsolutions = [] if initial_value > goal else [initial_value]
        self.goal = goal 
    
    # Try adding a new number.
    def next_step(self, number: int) -> None:
        new_viable_solutions = list()
        # If continuing with the partial result would exceed the goal,
        # the subsolution is subtly dropped.
        for partial_result in self.viable_subsolutions:
            multiplication_result = partial_result * number
            addition_result = partial_result + number
            concatenation_result = int(str(partial_result) + str(number))
            if multiplication_result <= self.goal:
                new_viable_solutions.append(multiplication_result)
            if addition_result <= self.goal:
                new_viable_solutions.append(addition_result)
            if concatenation_result <= self.goal:
                new_viable_solutions.append(concatenation_result)
        self.viable_subsolutions = new_viable_solutions
    
    def has_viable_solutions(self) -> bool:
        return len(self.viable_subsolutions) > 0
    
    def has_met_goal(self) -> bool:
        return any(partial_solution == self.goal for partial_solution in self.viable_subsolutions) 

# Checks if the equation could be true.
def could_be_satisfied(goal: int, values: list[int]) -> bool:
    if not values:
        return False

    explorer = Explorer(goal, values[0])

    for number in values[1:]:
        explorer.next_step(number)
        
    return explorer.has_met_goal() 

valid_equations = [equation for equation in equations if could_be_satisfied(equation[0], equation[1])]

total_calibration_result = sum(test_value for test_value, _ in valid_equations)
print(total_calibration_result)
