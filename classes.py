class process:
    def __init__(self, pid, priority, arrive_time, burst_time):
        self.is_ended = False
        self.end_time = -1
        self.burst_time = burst_time
        self.rest = burst_time
        self.pid = pid
        self.priority = priority
        self.arrive_time = arrive_time

    @property
    def wating_time(self):
        return self.end_time - self.arrive_time + 1

    def do(self, clock):
        self.rest -= 1
        if not self.rest:
            self.finish(clock)
            return self
        return self

    def finish(self, clock):
        self.end_time = clock
        self.is_ended = True

    def __str__(self):
        return f"pid : {self.pid} is_ended : {self.is_ended} end_time : {self.end_time}" + f"\n{self.rest}"


class rq:
    name = 'Ready Queue'
    process = list()
    ended = list()
    current = None

    def status(self):
        if len(self.process) or not (self.current is None):
            return True
        return False

    def do(self, clock):
        if self.current is None:
            current = self.process.pop(0)
        else:
            current = self.current
        current.do(clock)
        if current.is_ended:
            self.ended.append(current)
            self.current = None
        else:
            self.current = current

    def sort(self):
        pass


class fcfs(rq):
    name = 'FCFS'

    def sort(self):
        # self.process = sorted(self.process, key=lambda pc: pc.arrive_time)
        pass


class sjf(rq):
    name = 'SJF'

    def sort(self):
        self.process = sorted(self.process, key=lambda pc: pc.rest)
        pass


class rr(rq):
    name = 'RR'
    isinquantum = False

    def status(self):
        if len(self.process) or not (self.current is None) or not self.isinquantum:
            return True
        return False

    def do(self, clock):
        if self.current is None:
            current = self.process.pop(0)
        else:
            current = self.current

        current.do(clock)

        if current.is_ended:
            self.ended.append(current)
            self.current = None
            self.isinquantum = False
        else:
            if self.isinquantum:
                self.process.append(current)
                self.current = None
                self.isinquantum = False
            elif not self.isinquantum:
                self.isinquantum = True
                self.current = current

    def _2qdo(self, clock):
        if self.isinquantum:
            if self.current is None:
                self.isinquantum = not self.isinquantum
                return None
            else:
                current = self.current
        else:
            if self.current is None:
                current = self.process.pop(0)
            else:
                current = self.current

        current.do(clock)

        if current.is_ended:
            self.ended.append(current)
            self.current = None
            self.isinquantum = not self.isinquantum
        else:
            self.current = current
            self.isinquantum = not self.isinquantum
        return None
