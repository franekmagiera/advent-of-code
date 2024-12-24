data = """
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
""".strip()

data = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
""".strip()

with open("input_24", "r") as file:
    data = file.read().strip()

initial_values, connections = data.split("\n\n")

# I don't know what will be there in Part 2, so I'll try to do Part 1 as simple
# as possible, if Part 2 is harder I have ideas from SICP to fall back on :)

# But the simplest solution is to just initialize all wires, then keep going
# through the rest, figuring out for which wires I already have values, and
# setting them.

wires_labels = set()

wires = {}
for initial_value in initial_values.splitlines():
    wire, value = initial_value.split(": ")
    wires[wire] = int(value)
    wires_labels.add(wire)

for connection in connections.splitlines():
    function, output = connection.split(" -> ")
    wires_labels.add(output)

while len(wires) != len(wires_labels):
    for connection in connections.splitlines():
        function, output = connection.split(" -> ")
        a, function, b = function.split(" ")
        if output not in wires and a in wires and b in wires:
            match function:
                case "AND":
                    wires[output] = wires[a] and wires[b]
                case "XOR":
                    wires[output] = wires[a] ^ wires[b]
                case "OR":
                    wires[output] = wires[a] or wires[b]

import re
pattern = re.compile(r"z\d\d")
z_wires = sorted((wire_label for wire_label in wires_labels if pattern.match(wire_label)), reverse=True)
result = int("".join(str(wires[wire]) for wire in z_wires), 2)
print(result)

# Part 2

def add(x, y):
    wires_labels = set()
    wires = {}
    x_bin = format(x, "045b")
    y_bin = format(y, "045b")

    for bit, index in zip(x_bin, range(44, -1, -1)):
        wire = f"x{format(index, "02d")}" 
        wires[wire] = int(bit)
        wires_labels.add(wire)

    for bit, index in zip(y_bin, range(44, -1, -1)):
        wire = f"y{format(index, "02d")}" 
        wires[wire] = int(bit)
        wires_labels.add(wire)

    for connection in connections.splitlines():
        function, output = connection.split(" -> ")
        wires_labels.add(output)


    while len(wires) != len(wires_labels):
        for connection in connections.splitlines():
            function, output = connection.split(" -> ")
            a, function, b = function.split(" ")
            if output not in wires and a in wires and b in wires:
                match function:
                    case "AND":
                        wires[output] = wires[a] and wires[b]
                    case "XOR":
                        wires[output] = wires[a] ^ wires[b]
                    case "OR":
                        wires[output] = wires[a] or wires[b]

    pattern = re.compile(r"z\d\d")
    z_wires = sorted((wire_label for wire_label in wires_labels if pattern.match(wire_label)), reverse=True)
    result = int("".join(str(wires[wire]) for wire in z_wires), 2)
    return result

# zXX always has to be a result of a XOR, let's find all which are not.
pattern = re.compile(r"z\d\d")
for connection in connections.splitlines():
    function, output = connection.split(" -> ")
    a, function, b = function.split(" ")
    if pattern.match(output) and function != "XOR":
        print(a, function, b, output)

# So I found all the zXX outputs that are not results of a XOR (only z45 is fine
# to be a result of an OR, as it is the last bit). Then I figured - zXX has to
# somehow depend on xXX-1 and yXX-1, so I took a look the wires involved with
# xXX-1 and yXX-1 and found potential candidates to swap them.  This seemed to
# do the trick as my arbitrary chosen values seemed to start producing good
# results after those changes.

# Next I went bit by bit setting x to 2**i and keeping y at 1 and checking their sum.
# Noticed something was up with bit 34.
# Finally guessed that it's something to do with cvh -> usually zXX depends on
# yXX-1 XOR xXX-1 which was actually tfn, so I swapped cvh with tfn.

# Here's a simple loop to check if I missed something:
import random
for _ in range(1000):
    x = random.randint(0, 2**45-1)
    y = random.randint(0, 2**45-1)
    if add(x,y) != x+y:
        print(x)
        print(bin(x))
        print(x, y, add(x, y), x+y)
        print(x, y, bin(add(x, y)), bin(x+y))


# z14 hbk
# kvn z18
# z23 dbb
# cvh tfn

print(",".join(sorted(["z14", "hbk", "kvn", "z18", "z23", "dbb", "cvh", "tfn"])))
