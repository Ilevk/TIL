import sys

sys.stdin = open('input_4875.txt')

T = int(input())


# -1 이 탐색중, 0이 탐색x, 1이 탐색 완료
def dfs(tc, x, y, N, mask, maze, c):
    if x >= N or y >= N or x < 0 or y < 0:
        return False
    if (c != 0 and maze[x][y] != 3)  and (mask[x][y] != 0 or maze[x][y] != 0):
         return False

    mask[x][y] = -1

    if c != 0 and maze[x][y] == 3:
        print('#{} {}'.format(tc+1, c-1))
        return True

    c += 1
    if x + 1 < N:
        re1 = dfs(tc, x + 1, y, N, mask, maze, c)
    else:
        re1 = False
    if x - 1 >= 0:
        re2 = dfs(tc, x - 1, y, N, mask, maze, c)
    else:
        re2 = False
    if y + 1 < N:
        re3 = dfs(tc, x, y + 1, N, mask, maze, c)
    else:
        re3 = False
    if y - 1 >= 0:
        re4 = dfs(tc, x, y - 1, N, mask, maze, c)
    else:
        re4 = False
    mask[x][y] = 1
    return re1 or re2 or re3 or re4

for tc in range(T):
    N = int(input())

    maze = list()
    mask = list()

    for _ in range(N):
        maze.append([ int(i) for i in input()])
        mask.append([0 for _ in range(N)])

    for i in range(N):
        for j in range(N):
            if maze[i][j] == 2:
                x = i
                y = j
    c = 0
    re = dfs(tc, x, y, N, mask, maze, c)
    if not re :
        print('#{} {}'.format(tc+1, 0))