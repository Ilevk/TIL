import sys
sys.stdin = open('input_1984.txt')

T = int(input())

arr = list()

for tc in range(T):
    arr.append( list( map(int, input().split()) ) )

for i, tc in enumerate(range(T)):
    arr[i].sort(reverse=True)
    print('#{} {}'.format(i+1, round((sum(arr[i])-arr[i][0] - arr[i][9])/8)))
