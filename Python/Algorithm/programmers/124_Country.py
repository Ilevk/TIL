def solution(n):
    answer = ''
    
    while n > 0 : 
        if (n % 3) == 1 : 
            answer +='1'
        elif (n % 3) == 2:
            answer +='2'
        elif (n % 3) == 0 :
            answer += '4'
            
        n = int(n / 3)
        print(n)
    answer = answer[::-1]
    return answer

solution(3)