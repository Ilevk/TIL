matrix = [[-1 for _ in range(16)] for _ in range(16)]

row, column, k = [int(i) for i in input().split()]


def solve(x, y):
    global matrix
    if x == 1 or y == 1: matrix[x][y] = 1
    if matrix[x][y] != -1: return matrix[x][y]
    matrix[x][y] = solve(x - 1, y) + solve(x, y - 1)

    return matrix[x][y]


if k == 0:
    print(solve(row, column))
else:
    kcolumn = k % column
    krow = (column + k - 1) // column
    if kcolumn == 0: kcolumn = column
    result = solve(krow, kcolumn) * solve(row - krow + 1, column - kcolumn + 1)
    print(result)
