import sys

def debugprint(*a):
    # print(*a)
    pass

class Command:
    def __init__(self, input):
        input = input.split(',')
        self.name = input[0]
        self.priority = int(input[1])
        self.startTime = int(input[2])
        self.cpuBurst = int(input[3])
        self.burstTime = self.cpuBurst
        self.waitTime = 0

    def __repr__(self):
        return self.name


commands = []
lows = []
highs = []
res = ""
current_tick = 1


for line in sys.stdin.readlines():
    if line.strip():
        commands.append(Command(line))

commands.sort(key=lambda x: (x.startTime, x.name))

original = commands.copy()
deadTasks = []


def generate(ct: int):
    toRemove = []
    for c in commands:
        if (runnalbe(c, ct)):
            if (c.priority == 0):
                lows.append(c)
                toRemove.append(c)
            else:
                highs.append(c)
                toRemove.append(c)
    for c in toRemove:
        commands.remove(c)


def finished(ls: list[Command], ct: int):
    for c in ls:
        if (c.cpuBurst == 0):
            c.waitTime = ct - c.burstTime - c.startTime - 1
            debugprint("done:", c.name)
            deadTasks.append(c)
            return c


def runnalbe(c: Command, ct: int):
    if (ct > c.startTime):
        return True


srtf = None
twoJump = False
while (commands or lows or highs):
    generate(current_tick)
    debugprint(current_tick)
    lows.sort(key=lambda x: (x.cpuBurst))
    if srtf and lows[0].cpuBurst < srtf.cpuBurst:
        lows.remove(srtf)
        lows.append(srtf)
    temp1 = None
    for c in lows:
        if (runnalbe(c, current_tick)):
            temp1 = c
            break
    if (len(highs) != 0 and runnalbe(highs[0], current_tick)):
        temp = highs[0]
        highs.pop(0)
        if (srtf):
            lows.append(lows.pop(0))
        if (temp.cpuBurst == 1):
            current_tick += 1
            debugprint('r1')
            temp.cpuBurst -= 1
            debugprint("fut:", temp.name, temp.cpuBurst)
            if (len(res) == 0):
                res += temp.name
            if (res[-1] != temp.name):
                res += temp.name
        else:
            current_tick += 2
            generate(current_tick)
            debugprint('r2')
            temp.cpuBurst -= 2
            twoJump = True
            debugprint("fut:", temp.name, temp.cpuBurst)
            if (len(res) == 0):
                res += temp.name
            if (res[-1] != temp.name):
                res += temp.name
        # if (highs and runnalbe(highs[0], current_tick)):
        #     highs.append(temp)
        # elif (temp.cpuBurst != 0):
        #     highs.insert(0, temp)
        highs.append(temp)
        debugprint(highs)
        srtf = None
    elif (temp1 is not None):
        debugprint(lows)
        temp1.cpuBurst -= 1
        debugprint("fut:", temp1.name, temp1.cpuBurst)
        if (len(res) == 0):
            res += temp1.name
        if (res[-1] != temp1.name):
            res += temp1.name
        current_tick += 1
        if temp1.cpuBurst != 0:
            srtf = temp1
        else:
            srtf = None
    else:
        current_tick += 1

    xd = finished(lows, current_tick)
    if (xd in lows):
        lows.remove(xd)

    xd = finished(highs, current_tick)
    if (xd in highs):
        highs.remove(xd)
    debugprint(" ")
    twoJump = False
print(res)

for c in original:
    for d in deadTasks:
        if (c.name == d.name):
            c.waitTime = d.waitTime

restime = ""
for c in original:
    restime += c.name + ":" + str(c.waitTime) + ","
print(restime[:-1])
