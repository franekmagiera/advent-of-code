from dataclasses import dataclass
from fractions import Fraction
import re

data = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip()

with open("input_13", "r") as file:
    data = file.read().strip()

data = data.split("\n\n")

@dataclass
class Equations:
    # Xa + Yb = Z
    # Wa + Pb = R
    X: int
    Y: int
    Z: int
    W: int
    P: int
    R: int

    # Returns a, b if they are integers.
    def solve(self) -> tuple[int, int] | None:
        a = Fraction(self.R * self.Y - self.P * self.Z, self.W * self.Y - self.P * self.X)
        if not a.is_integer():
            return None
        a = a.as_integer_ratio()[0]
        b = Fraction(self.Z, self.Y) - Fraction(self.X * a, self.Y)
        if not b.is_integer():
            return None
        return (a, b.as_integer_ratio()[0])

def parse_equation(claw_machine_description):
    button_a = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
    button_b = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
    prize = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    button_a_match = button_a.search(claw_machine_description)
    button_b_match = button_b.search(claw_machine_description)
    prize_match = prize.search(claw_machine_description)

    return Equations(
        int(button_a_match.group(1)),
        int(button_b_match.group(1)),
        int(prize_match.group(1)) + 10000000000000,
        int(button_a_match.group(2)),
        int(button_b_match.group(2)),
        int(prize_match.group(2)) + 10000000000000
    )

tokens_needed = sum(
    3 * result[0] + result[1]
    for result in (
        parse_equation(claw_machine_description).solve()
        for claw_machine_description in data
    )
    if result is not None
)

print(tokens_needed)
