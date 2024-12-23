data = "2333133121414131402"

with open("input_9", "r") as file:
    data = file.read().strip()

def build_sparse_format_array(data):
    sparse_format = []
    for i, char in enumerate(data):
        if i % 2 == 0:
            # It is a file.
            sparse_format.extend([str(i // 2)] * int(char))
        else:
            # It is free space:
            sparse_format.extend(["."] * int(char))
    return sparse_format

sparse_format = build_sparse_format_array(data)

# print("".join(sparse_format))

def find_next_free_space(starting_index, sparse_format):
    i = starting_index
    while i < len(sparse_format) and sparse_format[i] != ".":
        i += 1
    return i

next_free_space = find_next_free_space(0, sparse_format)

def find_next_file_block(starting_index, sparse_format):
    i = starting_index
    while i >= 0 and sparse_format[i] == ".":
        i -= 1
    return i

next_file_block = find_next_file_block(len(sparse_format) - 1, sparse_format)

while next_free_space < next_file_block:
    sparse_format[next_free_space], sparse_format[next_file_block] = sparse_format[next_file_block], sparse_format[next_free_space]
    next_free_space = find_next_free_space(next_free_space, sparse_format)
    next_file_block = find_next_file_block(next_file_block, sparse_format)

# print("".join(sparse_format))

def compute_checksum(sparse_format):
    checksum = 0
    for position, file_id in enumerate(sparse_format):
        if file_id == ".":
            continue
        checksum += position * int(file_id)
    return checksum

print(compute_checksum(sparse_format))

# Part 2
sparse_format = build_sparse_format_array(data)

free_spaces = list()  # list(length, left, right)

i = 0
while i < len(sparse_format):
    if sparse_format[i] == ".":
        left = i
        while i < len(sparse_format) and sparse_format[i] == ".":
            i += 1
        size = i - left 
        free_spaces.append((size, left, i - 1))
    i += 1

# Find largest file_id.
i = len(sparse_format) - 1
while i >= 0 and sparse_format[i] == ".":
    i -= 1
current_file_id = int(sparse_format[i])

def find_file_block_range(starting_index, file_id, sparse_format):
    b = starting_index
    while b >= 0 and sparse_format[b] != str(file_id):
        b -= 1
    a = b
    while a >= 0 and sparse_format[a] == str(file_id):
        a -= 1
    return (a+1, b)

file_block_start, file_block_end = find_file_block_range(i, current_file_id, sparse_format)
while current_file_id >= 0:
    file_block_size = file_block_end - file_block_start + 1
    for idx, free_space in enumerate(free_spaces):
        if free_space[1] > file_block_start:
            break
        if free_space[0] == file_block_size:
            free_spaces.pop(idx)
            sparse_format[free_space[1]:free_space[2]+1], sparse_format[file_block_start:file_block_end+1] = sparse_format[file_block_start:file_block_end+1], sparse_format[free_space[1]:free_space[2]+1],
            break
        if free_space[0] > file_block_size:
            remaining_space = free_space[0] - file_block_size
            free_spaces[idx] = (remaining_space, free_space[1]+file_block_size, free_space[2])
            sparse_format[free_space[1]:free_space[1]+file_block_size], sparse_format[file_block_start:file_block_end+1] = sparse_format[file_block_start:file_block_end+1] , sparse_format[free_space[1]:free_space[1]+file_block_size]
            break
    current_file_id -= 1
    file_block_start, file_block_end = find_file_block_range(file_block_start, current_file_id, sparse_format)

print(compute_checksum(sparse_format))
