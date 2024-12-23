import re

data = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""".strip()

with open("input_23", "r") as file:
    data = file.read().strip()

computers = set()
connections = list()
for line in data.splitlines():
    pattern = re.compile(r"(\w+)-(\w+)")
    match = pattern.match(line)
    first_computer, second_computer = match.group(1), match.group(2)
    computers.add(first_computer)
    computers.add(second_computer)
    connections.append((first_computer, second_computer))

computers = list(sorted(computers))
computers = { computer: index for index, computer in enumerate(computers) }
index_to_computer = { index: computer for index, computer in enumerate(computers) }

connections_matrix = [[0 for _ in computers] for _ in computers]

for connection in connections:
    first_computer, second_computer = connection
    first_computer_index = computers[first_computer]
    second_computer_index = computers[second_computer]
    connections_matrix[first_computer_index][second_computer_index] = 1
    connections_matrix[second_computer_index][first_computer_index] = 1

for i, row in enumerate(connections_matrix):
    for j, _ in enumerate(row):
        if i == j:
            connections_matrix[i][j] = 1

def get_sets_of_three(connections_matrix, computers, index_to_computer):
    threes = set()

    for computer in computers:
        computer_connected_to = []
        i = computers[computer]
        for j, connected in enumerate(connections_matrix[i]):
            if j > i and connected == 1:
                computer_connected_to.append(j)
        for j, second_computer in enumerate(computer_connected_to):
            for third_computer in computer_connected_to[j+1:]:
                if connections_matrix[second_computer][third_computer] == 1:
                    threes.add((
                        index_to_computer[i],
                        index_to_computer[second_computer],
                        index_to_computer[third_computer]
                    ))

    return threes

threes = get_sets_of_three(connections_matrix, computers, index_to_computer)

contains_t_count = sum(1 for three in threes if any(computer.startswith("t") for computer in three))
print(contains_t_count)

# Part 2
# Solving the max clique problem on my own is too much for me today, let's try NetworkX.
import networkx as nx

G = nx.Graph()
G.add_edges_from(connections)
password = ",".join(sorted(max(nx.find_cliques(G), key=len)))
print(password)
