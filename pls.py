# import sys


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

'''
for line in sys.stdin.readlines():
    commands.append(Parancs(line))
'''
commands.append(Command("A,0,0,5"))
commands.append(Command("B,0,1,3"))
commands.append(Command("C,1,1,1"))
commands.append(Command("D,0,4,1"))
commands.append(Command("E,1,3,2"))

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


def runnalbe(c: Command):
    if (current_tick >= c.startTime):
        return True


while (len(lows) != 0 or len(highs) != 0):
    if (len(highs) != 0 and runnalbe(highs[0])):
        temp = highs[0]
        highs.pop(0)
        if (temp.cpuBurst == 1):
            current_tick += 1
            temp.cpuBurst -= 1
            if (len(res) == 0):
                res += temp.name
            if (res[-1] != temp.name):
                res += temp.name
        else:
            current_tick += 2
            temp.cpuBurst -= 2
            if (len(res) == 0):
                res += temp.name
            if (res[-1] != temp.name):
                res += temp.name
        highs.append(temp)
    elif (len(lows) != 0 and runnalbe(lows[0])):
        lows.sort(key=lambda x: (x.startTime, x.cpuBurst, x.name))
        lows[0].cpuBurst -= 1
        if (len(res) == 0):
            res += lows[0].name

        if (res[-1] != lows[0].name):
            res += lows[0].name
        current_tick += 1
    else:
        current_tick += 1
    finished(lows)
    finished(highs)

print(res)
