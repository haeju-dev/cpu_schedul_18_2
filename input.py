from classes import process

# 필터
def filter_word(character):
    NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
    # 입력받은 문자가 위 리스트에 있으면 True
    if character in NUMBERS:
        return True
    else:
        return False

# Raw Data를 파일에서 받아와 리스트로 변환하는 함수
def getrawinput(dir):
    f = open(dir, 'r')
    data = list()
    while True:
        tmp = f.readline()
        if tmp == '': # EOF시 종료
            break
        tmp = tmp.strip() # 양옆의 공백 제거

        newstr = ''
        for i in filter(filter_word, tmp): # 입력값에서 필터함수를 적용해 숫자와 공백만 추출
            newstr += i

        while '  ' in newstr: # 공백이 여러개 붙어있을 경우 공백이 하나가 될때까지 병합
            newstr = newstr.replace('  ', ' ')
        data.append(newstr)
    f.close()
    return data

# Dataset으로부터 Process 클래스를 생성하는 함수
def makeprocess(dataset):
    return process(pid=int(dataset[0]), priority=int(dataset[1]),
                   arrive_time=int(dataset[2]), burst_time=int(dataset[3]))

# 실질적인 Input을 종합 처리하는 함수, spawner parameter로 입력된 함수를 통해 데이터셋을 리스트로 반환한다.
def getinput(dir, spawner=makeprocess):
    raw = getrawinput(dir) # Raw Data
    data = list()
    for i in raw: # Raw Data list 각각에서 하나씩
        splitted = i.split(' ') # 공백으로 구분하여
        if not len(splitted) == 4: # 구분된 토큰 갯수가 4개가 아니면 에러
            raise Exception('Input data is invalid')
        data.append(spawner(splitted)) # 에러가 안날경우 data 리스트에 spawner에서 반환된 클래스를 추가
    return sorted(data, key=lambda pc: pc.arrive_time) # arrive_time으로 정렬해 반환

if __name__=="__main__": # (Debug) 실행시간에는 관계없음
    data = getinput('process.in', spawner=makeprocess)
    print(data)
