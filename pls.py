import sys


abc = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


class Parancs:
    def __init__(self, input):
        input = input.split(',')
        self.name = input[0]
        self.priority = input[1]
        self.startTime = input[2]
        self.cpuBurst = input[3]

    def __str__(self):
        return f"{self.name},{self.priority},{self.startTime},{self.cpuBurst}"


commands = []


for line in sys.stdin:
    commands.append(Parancs(line.replace("\n", '')))


for c in commands:
    print(c)
