class process:  # 프로세스
    def __init__(self, pid, priority, arrive_time, burst_time):
        self.pid = pid
        self.priority = priority
        self.arrive_time = arrive_time  # 해당 프로세스가 큐에 등록될 clock
        self.start_time = -1  # (Debug) 해당 프로세스의 수행이 실질적으로 시작된 clock
        self.burst_time = burst_time
        self.remaining = burst_time  # 해당 프로세스의 남아있는 시간 (Remaining), burst로 초기화
        self.is_ended = False  # 해당 프로세스의 작업 종료 여부
        self.end_time = -1  # 해당 프로세스가 끝날 경우 끝난 clock + 1이 세팅될 예정

    @property  # 속성값, 해당 인스턴스 호출시 자동으로 이 method의 반환값을 제공한다
    def waiting_time(self):  # 해당 프로세스의 waiting time
        return self.end_time - self.arrive_time - self.burst_time

    def do(self, clock):  # 해당 프로세스를 한 클럭씩 수행하는 시뮬레이션 역할을 담당하는 method
        if self.start_time == -1:  # (Debug) 실질적인 실행이 처음 시작된 경우
            self.start_time = clock  # (Debug) 현재 clock을 저장
        self.remaining -= 1  # 프로세스의 remaining time을 감소시킨다. (1 clock 실행한다)
        if not self.remaining:  # 프로세스의 remaining time이 없을 경우 == 프로세스의 실행이 모두 끝날 경우
            self.finish(clock)  # 프로세스 종료 method를 실행한다

    def finish(self, clock):  # 프로세스 종료 method
        self.end_time = clock + 1  # 프로세스가 종료된 다음 clock을 end time에 저장
        self.is_ended = True  # 종료 여부 체크

    @property
    def output(self):  # 해당 프로세스의 시뮬레이션 결과 출력용 instance
        return f"{self.pid} {self.waiting_time}"  # process number와 waiting time을 문자열 포맷으로 반환한다

    def __str__(self):  # (Debug) 디버그 화면에서 클래스 정보 전달을 용이하게 하기 위함
        return f"pid:{self.pid} start:{self.start_time} end:{self.end_time} arrival:{self.arrive_time} " + \
               f"burst:{self.burst_time} waiting:{self.waiting_time}"


class rq:  # Ready Queue의 공통된 부분을 정의해둔 부모 클래스
    name = 'Ready Queue'

    def __init__(self):  # 생성자 (Constructor)
        self.process = list()  # 해당 큐의 남아있는 프로세스의 리스트
        self.current = None  # 해당 큐에서 현재 실행중인 프로세스
        self.ended = list()  # 해당 큐에서 완료된 프로세스의 리스트

    @property
    def avg_waiting_inqueue(self):  # (Debug) 해당 큐에서 완료된 프로세스의 평균 waiting time
        n = 0
        for i in self.ended:
            n += i.waiting_time
        if len(self.ended):  # (Debug) zero-division Error 방지
            return n / len(self.ended)
        return n

    def status(self):  # 해당 큐에서 실행중이거나 실행 가능한 프로세스의 존재 여부를 반환하는 method
        if len(self.process) or not (self.current is None):
            return True
        return False  # 해당 큐가 비어있음을 의미

    def do(self, clock):  # 해당 큐의 프로세스를 실행하는 method
        if self.current is None:  # 현재 실행중인 프로세스가 없다면
            current = self.process.pop(0)  # 실행해야할 프로세스의 가장 첫번째를 가져온다
        else:
            current = self.current  # 현재 실행중인 프로세스가 있다면 해당 프로세스를 가져온다
        current.do(clock)  # 프로세스를 한 clock 실행한다 -> 프로세스의 remaining time을 줄이고, 만약 0이 된다면 종료 method를 실행한다
        if current.is_ended:  # 프로세스가 끝났을 경우
            self.ended.append(current)  # 현재 큐의 완료된 프로세스 리스트에 해당 프로세스를 추가한다
            self.current = None  # 현재 실행중인 프로세스를 담는 공간을 비운다
        else:
            self.current = current  # 프로세스가 끝나지 않았을 경우 현재 실행중인 프로세스로 저장하고 다음 순서를 기다린다

    def sort(self):  # 실행할 프로세스 리스트를 정렬하는 method, 각 큐에서 override해 사용할 예정
        pass


class fcfs(rq):
    name = 'FCFS'  # 먼저 들어온 프로세스를 먼저 처리하는 큐

    def sort(self):  # arrive_time 기준으로 정렬하려고 했으나 input 받아올때 하므로 의미없음
        # self.process = sorted(self.process, key=lambda pc: pc.arrive_time)
        pass


class sjf(rq):
    name = 'SJF'  # (non-preemptive) Shotest Job First, burst_time이 가장 낮은 프로세스부터 처리한다

    def sort(self):  # burst_time 기준으로 실행해야할 프로세스를 정렬한다 (현재 실행중인 프로세스는 따로 관리되므로 비선점형)
        self.process = sorted(self.process, key=lambda pc: pc.burst_time)
        pass


class rr(rq):
    name = 'RR'  # Round Robin
    isinquantum = False  # 실행중인 블록의 중간에 위치해 있는지를 체크하는 instance, quantum size가 2이므로 boolean형

    def do(self, clock):  # do method를 override
        if self.current is None:
            current = self.process.pop(0)
        else:
            current = self.current

        current.do(clock)

        if current.is_ended: # 만약 프로세스가 완료될경우
            self.ended.append(current)
            self.current = None
            self.isinquantum = False # 실행중인 블록을 초기화
        else:
            if self.isinquantum: # 만약 현재 프로세스의 실행 count가 quantum size에 도달했다면
                self.process.append(current) # 실행할 프로세스 리스트의 맨 뒤로 보낸다
                self.current = None
                self.isinquantum = False # 실행중인 블록 정보를 초기화
            elif not self.isinquantum: # 만약 현재 프로세스의 실행 count가 quantum size에 도달하지 않았다면
                self.isinquantum = True # 현재 프로세스의 실행 count를 증가시킨다
                self.current = current

    # def status(self):
    #     if len(self.process) or not (self.current is None) or self.isinquantum:
    #         return True
    #     return False

    # def _2qdo(self, clock):
    #     if self.isinquantum:
    #         if self.current is None:
    #             self.isinquantum = not self.isinquantum
    #             return None
    #         else:
    #             current = self.current
    #     else:
    #         if self.current is None:
    #             current = self.process.pop(0)
    #         else:
    #             current = self.current
    #
    #     current.do(clock)
    #
    #     if current.is_ended:
    #         self.ended.append(current)
    #         self.current = None
    #         self.isinquantum = not self.isinquantum
    #     else:
    #         self.current = current
    #         self.isinquantum = not self.isinquantum
    #     return None
