import sys

sys.stdin = open('input_5099.txt')

T = int(input())

for tc in range(T):
    oven_size, pizza = map(int, input().split())

    cheeze = list(map(int, input().split()))

    idx = [i for i in range(pizza)]
    oven = list()

    for _ in range(oven_size):
        oven.append(idx.pop(0))

    while len(oven) != 0:

        current_pizza = oven.pop(0)
        cheeze[current_pizza] = cheeze[current_pizza]//2

        if cheeze[current_pizza] != 0 :
            oven.append(current_pizza)
            pass

        elif cheeze[current_pizza] == 0 and len(idx) != 0 :
            oven.append(idx.pop(0))

        elif len(oven) == 0 and cheeze[current_pizza] == 0 and len(idx) == 0 :
            print('# {} {}'.format(tc+1, current_pizza+1))
            break