data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

with open("input_4", "r") as file:
    data = file.read()

data = [[letter for letter in line] for line in data.split('\n')]

rows = len(data)
cols = len(data[0])

def check(data, rows, cols, row, col, progress_row, progress_col):
    i = row
    j = col
    word = ""
    while 0 <= i < rows and 0 <= j < cols and len(word) < 4:
        word += data[i][j]
        i = progress_row(i)
        j = progress_col(j)
    return word == "XMAS"

def check_right(data, rows, cols, row, col):
    return check(data, rows, cols, row, col, lambda x: x, lambda y: y + 1)

def check_left(data, rows, cols, row, col):
    return check(data, rows, cols, row, col, lambda x: x, lambda y: y - 1)

def check_up(data, rows, cols, row, col):
    return check(data, rows, cols, row, col, lambda x : x - 1, lambda y: y)

def check_down(data, rows, cols, row, col):
    return check(data, rows, cols, row, col, lambda x: x + 1, lambda y: y)

def check_diagonal_up_right(data, rows, cols, row, col):
    return check(data, rows, cols, row, col, lambda x: x - 1, lambda y: y + 1)

def check_diagonal_down_right(data, rows, cols, row, col):
    return check(data, rows, cols, row, col, lambda x: x + 1, lambda y: y + 1)

def check_diagonal_up_left(data, rows, cols, row, col):
    return check(data, rows, cols, row, col, lambda x: x - 1, lambda y: y - 1)

def check_diagonal_down_left(data, rows, cols, row, col):
    return check(data, rows, cols, row, col, lambda x: x + 1, lambda y: y - 1)

def puzzle1(data, rows, cols):
    count = 0
    for i in range(rows):
        for j in range(cols):
            if data[i][j] == "X":
                count += (check_right(data, rows, cols, i, j) +
                    check_left(data, rows, cols, i, j) +
                    check_up(data, rows, cols, i, j) +
                    check_down(data, rows, cols, i, j) +
                    check_diagonal_up_right(data, rows, cols, i, j) +
                    check_diagonal_down_right(data, rows, cols, i, j) +
                    check_diagonal_up_left(data, rows, cols, i, j) +
                    check_diagonal_down_left(data, rows, cols, i, j))
    return count

print(puzzle1(data, rows, cols))

def puzzle2(data, rows, cols):
    count = 0
    for i in range(rows):
        for j in range(cols):
            if data[i][j] == "A":
                count += check_x(data, rows, cols, i, j)
    return count

def check_x(data, rows, cols, row, col):
    def valid_index(i, j):
        return 0 <= i < rows and 0 <= j < cols
    
    if not (valid_index(row-1, col-1) and valid_index(row-1, col+1) and valid_index(row+1, col-1) and valid_index(row+1, col+1)):
        return False
    
    first_diagonal = data[row-1][col-1] + data[row+1][col+1]
    second_diagonal = data[row+1][col-1] + data[row-1][col+1]

    return (first_diagonal == "SM" or first_diagonal == "MS") and (second_diagonal == "SM" or second_diagonal == "MS")

print(puzzle2(data, rows, cols))
