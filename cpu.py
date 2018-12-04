from classes import fcfs, sjf, rr
from input import getinput

input_processes = getinput('process.in')

rq = list()
rq.append(rr())
rq.append(sjf())
rq.append(fcfs())

clock = 0

isended = False
while len(input_processes) or not isended:
    # 적합한 Ready Queue에 현재 clock의 프로세스 할당
    if len(input_processes):
        if input_processes[0].arrive_time == clock:
            tmp = input_processes.pop(0)
            rq[tmp.priority - 1].process.append(tmp)

    for i in rq:
        if i.status():
            i.sort()
            i.do(clock)
            break

    # End check
    isended = True
    for i in rq:
        if i.status():
            isended = False

    clock += 1

print('ended')

result = list()
for i in rq:
    for j in i.ended:
        result.append(j)
result = sorted(result, key=lambda pid:pid.pid)

print(result)