#testThing.py
import re

def parseSequence(string):
    a = re.search("\((.+)\)", string)
    if a:
        b = ''.join(a.group(1).split())
        params = b.split(",")
    else:
        params = []
    b = re.match('(.+)(?=\()', string)
    if b:
        return (b.group(1), params)
    else:
        return string

definedSequences = dict()

infile = open('testFile.txt', 'r')

lines = infile.readlines()
#define sequences
lastDefined = ""
i = 0
while i < len(lines):
    line = lines[i]
    if len(line) >= 2:
        if line == "END_SEQUENCES\n":
            i += 1
            break
        if line[-2] == ':':
            a = parseSequence(line)
            definedSequences[a[0]] = {"commands":list(), "parameters":a[1]}
            lastDefined = a[0]
        else:
            line = line[2:-1]
            definedSequences[lastDefined]["commands"].append(line)
    i += 1

commandList = []




#execute sequences and commands
while i < len(lines):
    line = lines[i]
    if len(line) >= 2:
        if re.match('SW | SR | CW | CR | P', line):
            commandList.append(line[:-2])
        else:
            a = parseSequence(line)
            templist = list(definedSequences[a[0]]["commands"])
            temp = '~'.join(templist)
            for n in xrange(len(a[1])):
                temp = re.sub(definedSequences[a[0]]["parameters"][n], a[1][n], temp)
            for c in temp.split('~'):
                commandList.append(c)
    i += 1
for c in commandList:
    print c
