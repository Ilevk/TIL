def solution(progresses, speeds):
    answer = []
    days = [0 for _ in progresses]
    
    for i, p in enumerate(progresses) : 
        day = (100-p) / speeds[i]
        if ((100-p) % speeds[i]) != 0 :
            day += 1
        days[i] = int(day)
    
    current_idx = 0
    count = 1
    for i, day in enumerate(days[1:]):
        if days[current_idx] >= day :
            count += 1 
        else :
            answer.append(count)
            count = 1
            current_idx = i+1

    if current_idx == (len(days) - 1):
        answer.append(count)
    return answer

print(solution([93, 30, 55], [1, 30, 5]))