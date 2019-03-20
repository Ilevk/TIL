import sys
sys.stdin = open('1711_input.txt')

N = int(input())

score_board = [0 for _ in range(N)]
cards = list()
for i in range(N):
    cards.append([int(i) for i in input().split()])

for i in range(3):
    current_score = [1 for _ in range(N)]
    for j in range(N):
        for k in range(j+1, N):
            if current_score[k] == 0 :
                continue
            if cards[j][i] == cards[k][i] :
                current_score[j] = 0
                current_score[k] = 0
        if current_score[j] != 0:
            current_score[j] = cards[j][i]
    score_board[i] = current_score

result = [0 for _ in range(N)]
for i in range(3):
    for j in range(N):
        result[j] += score_board[j][i]

for i in range(3):
    print(result[i])