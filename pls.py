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
'''
for line in sys.stdin.readlines():
    commands.append(Parancs(line))

commands.append(Command("A,0,0,6"))
commands.append(Command("B,0,1,5"))
commands.append(Command("C,1,5,2"))
commands.append(Command("D,1,10,1"))
'''

commands.append(Command("A,1,2,7"))
commands.append(Command("B,1,2,3"))



def finished():
    for c in commands:
        if (c.cpuBurst == 0):
            commands.remove(c)


def get_best(noms: list[Command]):
    best = noms[0]
    for i in range(len(noms)):
        if (noms[i] != best):
            if (noms[i].priority > best.priority):
                best = noms[i]
            elif (noms[i].priority == best.priority):
                if (noms[i].name < best.name):
                    best = noms[i]
    return best


def regenerate():
    lows.clear()
    highs.clear()
    for c in commands:
        if (c.priority == 0):
            lows.append(c)
        else:
            highs.append(c)


def runnalbe(c: Command):
    if (current_tick >= c.startTime):
        return True


def nominee_maker():
    nominees = []
    for l in lows:
        if (runnalbe(l)):
            nominees.append(l)
    for h in highs:
        if (runnalbe(h)):
            nominees.append(h)
    return nominees


current_tick = 0
while (len(commands) != 0):
    regenerate()
    nominees = nominee_maker()
    if (len(nominees) != 0):
        best = get_best(nominees)
        for c in commands:
            if (c.name == best.name):
                commands.remove(c)
        res += best.name
        best.cpuBurst -= 1
        commands.append(best)
    finished()
    current_tick += 1

print(res)
