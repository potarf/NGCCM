#testThing.py
import re

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
            definedSequences[line[:-2]] = list()
            lastDefined = line[:-2]
        else:
            line = line[2:-2]
            definedSequences[lastDefined].append(line)
    i += 1
print lastDefined
print definedSequences

commandList = []


#execute sequences and commands
while i < len(lines):
    line = lines[i]
    if len(line) >= 2:
        if re.match('SW | SR | CW | CR', line):
            commandList.append(line[:-2])
        elif line[:-1] in definedSequences.keys():
            for c in definedSequences[line[:-1]]:
                commandList.append(c)
    i += 1
print commandList
