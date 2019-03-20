import sys
sys.stdin = open('1726_input.txt')

N = int(input())
inputs = list()
for i in range(N):
    inputs.append(float(input()))

# matrix = [[0 for _ in range(N)] for _ in range(N)]
max=0
for i in range(N):
    for j in range(N-i):
        current = 1
        for k in range(i-j):
            current *= inputs[j+k]
        if current > max:
            max = current
print("{:.3f}".format(max))