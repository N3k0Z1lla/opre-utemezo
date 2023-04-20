import sys


class Command:
    def __init__(self, input):
        input = input.split(',')
        self.name = input[0]
        self.priority = int(input[1])
        self.startTime = int(input[2])
        self.cpuBurst = int(input[3])
        self.waitTime = 0

    def __repr__(self):
        return self.name


commands = []
lows = []
highs = []
res = ""
current_tick = 1


for line in sys.stdin.readlines():
    commands.append(Command(line))


original = commands.copy()
deadTasks = []
for c in commands:
    if (c.priority == 0):
        lows.append(c)
    else:
        highs.append(c)

highs.sort(key=lambda x: (x.startTime, x.name))


def finished(ls: list[Command]):
    for c in ls:
        if (c.cpuBurst <= 0):
            ls.remove(c)
            print("done:", c.name)
            deadTasks.append(c)


def runnalbe(c: Command, ct: int):
    if (ct >= c.startTime):
        return True


while (len(lows) != 0 or len(highs) != 0):
    if (len(highs) != 0 and runnalbe(highs[0], current_tick)):
        temp = highs[0]
        highs.pop(0)
        if (temp.cpuBurst == 1):
            current_tick += 1
            temp.cpuBurst -= 1
            print("fut:", temp.name)
            if (len(res) == 0):
                res += temp.name
            if (res[-1] != temp.name):
                res += temp.name
        else:
            current_tick += 2
            print('r')
            temp.cpuBurst -= 2
            print("fut:", temp.name)
            if (len(res) == 0):
                res += temp.name
            if (res[-1] != temp.name):
                res += temp.name
        highs.append(temp)
    elif (len(lows) != 0 and runnalbe(lows[0], current_tick)):
        lows.sort(key=lambda x: (x.startTime, x.cpuBurst, x.name))
        lows[0].cpuBurst -= 1
        print("fut:", lows[0].name)
        if (len(res) == 0):
            res += lows[0].name
        if (res[-1] != lows[0].name):
            res += lows[0].name
        current_tick += 1
    else:
        current_tick += 1
    for c in lows:
        if (runnalbe(c, current_tick - 1)):
            print("wait:", c.name)
            c.waitTime += 1
    for c in highs:
        if (runnalbe(c, current_tick - 1)):
            c.waitTime += 1
            print("wait:", c.name)
    finished(lows)
    finished(highs)
    print(" ")
print(res)

for c in original:
    for d in deadTasks:
        if (c.name == d.name):
            c.waitTime = d.waitTime

restime = ""
for c in original:
    restime += c.name + ":" + str(c.waitTime) + ","
print(restime[:-1])
