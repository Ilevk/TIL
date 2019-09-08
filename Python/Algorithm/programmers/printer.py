import copy

def solution(priorities, location):
    answer = 0
    idx_list = [i for i in range(len(priorities))]
    sorted_priorities = copy.deepcopy(priorities)
    sorted_priorities = sorted(sorted_priorities, reverse=True)
    pri_idx = 0
    print_idx = 0
    print(priorities)
    while len(priorities) > 0 :
        if priorities[0] == sorted_priorities[pri_idx]:
            pri_idx += 1
            print_idx += 1
            if idx_list[0] == location:
                answer = print_idx
                break
            priorities.pop(0)
            idx_list.pop(0)
        else :
            priorities.append(priorities.pop(0))
            idx_list.append(idx_list.pop(0))
    print(sorted_priorities)
    print(idx_list)
       
    return answer


print(solution([1, 1, 9, 1, 1, 1], 0))