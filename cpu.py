from classes import fcfs, sjf, rr
from input import getinput

def highlevel(input_processes):
    rq = list()  # Ready Queue의 리스트를 생성한다
    rq.append(rr())  # 우선순위 1인 Round Robin queue를 먼저 추가
    rq.append(sjf())  # Shortest Job First queue를 추가
    rq.append(fcfs())  # First Come First Serve queue를 추가

    clock = 0  # 현재 clock number를 0으로 초기화

    isended = False
    while len(input_processes) or not isended:  # queue에 등록되지 않은 프로세스가 있거나 모든 큐가 비어있지 않다면 반복
        # 적합한 Ready Queue에 현재 clock의 프로세스 할당
        while len(input_processes):  # 만약 아직 queue에 등록되지 않은 프로세스가 있다면
            if input_processes[0].arrive_time == clock:  # 만약 다음 프로세스의 arrival time이 현재 clock이라면
                tmp = input_processes.pop(0)  # 다음 프로세스를 가져온다
                rq[tmp.priority - 1].process.append(tmp)  # 다음 프로세스의 적합한 큐에 프로세스를 등록한다
            else:
                break  # 현재 clock에 등록할 프로세스가 없다면 반복문 탈출

        for i in rq:  # Ready Queue list의 첫번째부터 (우선순위가 높은 Queue부터) 반복
            if i.status():  # 만약 해당 queue에 실행해야할 프로세스가 있다면
                i.sort()  # 각 queue에 override된 프로세스 정렬 method를 실행
                i.do(clock)  # 해당 queue에서 실행중이거나 실행해야할 프로세스를 실행
                break  # 현재 clock에는 하나의 프로세스만 실행 가능하므로 반복문 탈출

        # End check
        isended = True  # False값을 적용하는 필터링으로 모든 Queue가 비어있는지 검사
        for i in rq:  # 모든 Queue를 반복
            if i.status():  # 해당 Queue가 비어있지 않다면
                isended = False  # 모든 Queue가 비어있지 않다

        clock += 1  # 반복문 마지막에 clock값을 증가시킨다

    # Output
    result = list()
    for i in rq:  # 모든 큐 반복
        for j in i.ended:  # 해당 큐에서 완료된 프로세스 리스트에서의 각 프로세스들을
            result.append(j)  # result 리스트에 추가한다
    result = sorted(result, key=lambda pid: pid.pid)  # result 리스트를 process number 기준으로 정렬

    avg_waiting = 0
    if len(result):  # (Debug) zero-division Error 방지
        for i in result:
            avg_waiting += i.waiting_time  # 모든 프로세스의 waiting time을 더한다
        avg_waiting /= len(result)  # 모든 프로세스의 waiting time의 합을 프로세스의 갯수로 나눈다

    # (Debug)
    # print(f"Ended with {clock} clock, avg_waiting {round(float(avg_waiting), 2)}")
    # print()
    # for i in result:
    #     print(i)
    # print()
    return result


inputs = getinput('process.in') # 파일에서 프로세스 리스트를 입력받는다
result = highlevel(inputs) # 시뮬레이션

# Output
for i in result:
    print(i.output)


# inputs = list()
# for i in range(3):
#     inputs.append(getinput('process' + str(i+1) + '.in'))
#
# # input_processes = getinput('process.in')
#
# results = list()
# for i in range(3):
#     result = highlevel(inputs[i])
#     results.append(result)
#
# # Output
# for i in results:
#     for j in i:
#         print(j.output)
#     print()