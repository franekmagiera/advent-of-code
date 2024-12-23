import re

data = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""".strip()

with open("input_17", "r") as file:
    data = file.read().strip()

def parse_input(data):
    reg_a = re.compile(r"Register A: (\d+)")
    reg_b = re.compile(r"Register B: (\d+)")
    reg_c = re.compile(r"Register C: (\d+)")

    program = re.compile(r"Program: (.+)")

    return VM(
        int(reg_a.search(data).group(1)),
        int(reg_b.search(data).group(1)),
        int(reg_c.search(data).group(1)),
        [int(char) for char in program.search(data).group(1).split(",")]
    )

class VM:
    def __init__(self, reg_a, reg_b, reg_c, program):
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c

        self.program = program

        self.pc = 0

        self.out = []

    def __repr__(self):
        return f"reg_a={self.reg_a}, reg_b={self.reg_b}, reg_c={self.reg_c}, pc={self.pc}, program={self.program}"

    def run(self):
        while self.pc < len(self.program):
            self.execute_instruction()
    
    def reset(self):
        self.out = []
        self.pc = 0

    def execute_instruction(self):
        assert self.pc % 2 == 0
        instruction = self.program[self.pc]
        self.pc += 1
        operand = self.program[self.pc]
        self.pc += 1

        match instruction:
            case 0:
                numerator = self.reg_a
                denominator = 2 ** self._get_combo_operand(operand)
                result = numerator // denominator
                self.reg_a = result
            case 1:
                result = self.reg_b ^ operand
                self.reg_b = result
            case 2:
                result = self._get_combo_operand(operand) % 8
                self.reg_b = result
            case 3:
                if self.reg_a != 0:
                    self.pc = operand
            case 4:
                result = self.reg_b ^ self.reg_c
                self.reg_b = result
            case 5:
                result = self._get_combo_operand(operand) % 8
                self.out.append(result)
            case 6:
                numerator = self.reg_a
                denominator = 2 ** self._get_combo_operand(operand)
                result = numerator // denominator
                self.reg_b = result
            case 7:
                numerator = self.reg_a
                denominator = 2 ** self._get_combo_operand(operand)
                result = numerator // denominator
                self.reg_c = result

    def _get_combo_operand(self, value):
        match value:
            case 0 | 1 | 2 | 3:
                return value
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c
            case 7:
                raise RuntimeError("Combo operant 7 is reserved")


vm = parse_input(data)
vm.run()
output = ",".join(str(value) for value in vm.out)

print(output)

# Part 2
# ----------------------
print(20 * "-")

data = """
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""".strip()


# 35184372088832 is the lowest value I need to check
# 281474976710655 is the highest value I need to check

# 35184372088833 produces 2 first 
data = """
Register A: 109019930331546
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,4,5,0,3,1,6,5,5,3,0
""".strip()

vm = parse_input(data)
vm.run()
output = ",".join(str(value) for value in vm.out)

print(output)

# ---
# After 1 iteration
# X = vm.reg_a
# reg_b = X % 8  # 1 take 3 lowest bits
# reg_b = reg_b ^ 5  # 2 bitwise xor with 0b101
# reg_c = X // 2 ** reg_b  # 3 do the adv
# reg_b = reg_b ^ reg_c  # 4
# reg_a = X // 2**3  # 5
# reg_b = reg_b ^ 6  # 6 bitwise xor with 0b110
# print(reg_b % 8)  # 7
# reg_b mod 8 has to be 2 to satisfy the program
# so its 3 lowest bits have to be 010
# so xored with 0b110 they have to give 010
# reg_b before step 6 has to have 100 as 3 lowest bits
# so in step 4 they have to yield 100 as 3 lowest bits (reg_b and reg_c bitwise xor)
# it can be only 011 111 or 100 000

# so step 2 can yield only 011 or 111 or 100 or 000 - so in step 3 it will cut off 3, 7, 4 or 0 lowest digits
# so reg_b after step 1 has to be (so after it is xored with 0b101 it produces on of the above)
#   110, 010, 001, 101 
# so one of those HAS to be 3 lowest bits of initial REG A value

# At the same time, what does step 3 do? it cuts reg_b bits off of reg_a

# Repeat if reg_a != 0
# ----

# I get 100 so I cut off 4

# vm.reg_a = 0b1000000000000000000000000000000000000000000001
# vm.run()
# output = ",".join(str(value) for value in vm.out)
# print(output)

# vm.reset()
# for i in range(2**21):
#     vm.reg_a = i
#     # print(bin(i))
#     vm.run()
#     output = ",".join(str(value) for value in vm.out)
#     if output == "3,1,6,5,5,3,0":
#         print(bin(i), output)
#     vm.reset()


# One of those bit patterns for sure has to begin the number I'm looking for
# 0b11000110010011100011 3,1,6,5,5,3,0
# 0b11000110010011100101 3,1,6,5,5,3,0
# 0b11000110100011100011 3,1,6,5,5,3,0
# 0b11000110100011100101 3,1,6,5,5,3,0
# 0b11111001000001100101 3,1,6,5,5,3,0
# numbers = [
# 0b11000110010011100101110001110001000100110011 ,
# 0b11000110010011100101110001110001000110001110 ,
# 0b11000110010011100101110001110001000111001110 ,
# 0b11000110010011100101110001110001000111100000 ,
# 0b11000110010011100101110001110001000111100001 ,
# 0b11000110010011100101110001110001111001100001 ,
# 0b11000110100011100101110001110001000100110011 ,
# 0b11000110100011100101110001110001000110001110 ,
# 0b11000110100011100101110001110001000111001110 ,
# 0b11000110100011100101110001110001000111100000 ,
# 0b11000110100011100101110001110001000111100001 ,
# 0b11000110100011100101110001110001111001100001 ,
# 0b11111001000001100101110001110001000100110011 ,
# 0b11111001000001100101110001110001000110001110 ,
# 0b11111001000001100101110001110001000111001110 ,
# 0b11111001000001100101110001110001000111100000 ,
# 0b11111001000001100101110001110001000111100001 ,
# 0b11111001000001100101110001110001111001100001 ,
# ]

# vm.reset()
# for number in numbers:
#     n = number << 3
#     for i in range(8):
#         vm.reg_a = n + i
#         vm.run()
#         output = ",".join(str(value) for value in vm.out)
#         if output == "2,4,1,5,7,5,4,5,0,3,1,6,5,5,3,0":
#             print(bin(n+i), ",")# , output)
#         vm.reset()
