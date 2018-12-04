from classes import process


def filter_word(character):
    NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
    # 입력받은 문자가 위 리스트에 있으면 True
    if character in NUMBERS:
        return True
    else:
        return False


def getrawinput(dir):
    f = open(dir, 'r')
    data = list()
    while True:
        tmp = f.readline()
        if tmp == '':
            break
        tmp = tmp.strip()

        newstr = ''
        for i in filter(filter_word, tmp):
            newstr += i

        while '  ' in newstr:
            newstr = newstr.replace('  ', ' ')
        data.append(newstr)
    f.close()
    return data


def makedataset(raw):
    # return {raw[0]: makeprocess(raw)}
    return makeprocess(raw)


def makeprocess(dataset):
    return process(pid=int(dataset[0]), priority=int(dataset[1]),
                   arrive_time=int(dataset[2]), burst_time=int(dataset[3]))


def getinput(dir, spawner=makedataset):
    raw = getrawinput(dir)
    data = list()
    for i in raw:
        splitted = i.split(' ')
        if not len(splitted) == 4:
            raise Exception('Input data is invalid')
        data.append(spawner(splitted))
    return sorted(data, key=lambda pc: pc.arrive_time)

if __name__=="__main__":
    data = getinput('process.in', spawner=makedataset)
    print(data)
