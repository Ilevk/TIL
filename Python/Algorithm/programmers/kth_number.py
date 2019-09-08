import copy 

def solution(array, commands):
    answer = []
    for com in commands :
        start = com[0]-1
        end = com[1]
        k = com[2] -1
        temp_list = copy.deepcopy(array[start : end])
        temp_list = sorted(temp_list)
        answer.append(temp_list[k])
    return answer

print(solution([1, 5, 2, 6, 3, 7, 4], [[2, 5, 3], [4, 4, 1], [1, 7, 3]]	))