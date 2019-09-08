def solution(participant, completion):
    answer = ''
    completion_dict = dict()
    
    for p in completion :
        if p in completion_dict:
            completion_dict[p] += 1
        else :
            completion_dict[p] = 1
            
    for c in participant : 
        if c in completion_dict:
            if completion_dict[c] == 0:
                answer = c
                break
            completion_dict[c] -= 1
        else :
            answer = c
    return answer

print(solution(['leo', 'kiki', 'eden'], ['eden', 'kiki']))