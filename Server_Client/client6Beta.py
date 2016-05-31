from websocket import create_connection
import re, sys, optparse, commands

################################################################################
#                      Parse Script Options and Arguments                      #
################################################################################
parser = optparse.OptionParser("usage: %prog [options] <input file> \n")
parser.add_option("-v", "--verbosity",
                  dest="verbosity", type='int', default=0,
                  help="amount of detail in output")
parser.add_option("-a", "--address",
                  dest="serverAddress", type="string",
                  default="ws://192.168.1.22:8080/ws",
                  help ="address of server node")
options, args = parser.parse_args()
if len(args) != 1:
    print "Please specify input file. Exiting"
    sys.exit()

inputFileName = args[0]
VERBOSITY = options.verbosity
serverAddress = options.serverAddress
################################################################################


################################################################################
#                           Function Definitions                               #
################################################################################
def send_message(str):
    ws.send(str)
    if VERBOSITY >= 2: print "Sent '%s'" % str
    result = ws.recv()
    if VERBOSITY >= 2: print "Received '%s'" % result
    return(result)

def read_byte(address):
    message = send_message("SR "+hex(address))
    if VERBOSITY >= 1: print message
    match = re.search(r"OK\s+(\w+)",message,re.I|re.X)
    if match:
        return int(match.group(1),0)
    return None

def read_byte_s(address):
    ret = read_byte(address)
    if ret == None: return None
    return hex(ret)

def write_byte(address,value):
    message = send_message("SW "+hex(address)+" "+hex(value))
    if VERBOSITY >= 1: print message

def read_byte_data(address,register):
    message = send_message("CR "+hex(address)+" "+hex(register))
    if VERBOSITY >= 1: print message
    match = re.search(r"OK\s+(\w+)",message,re.I|re.X)
    if match:
        return int(match.group(1),0)
    return None

def read_byte_data_s(address,register):
    ret = read_byte_data(address,register)
    if ret == None: return None
    return hex(ret)

def write_byte_data(address,register,value):
    message = send_message("CW "+hex(address)+" "+hex(register)+" "+hex(value))
    if VERBOSITY >= 1: print message

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
################################################################################


################################################################################
#                                   Setup                                      #
################################################################################
ws = create_connection(serverAddress)
infile = open(inFileName, 'r')
################################################################################


################################################################################
#                                 Execute                                      #
################################################################################
definedSequences = dict()

#infile = open('testFile.txt', 'r')

#load lines from testfile
lines = list(infile.readlines())

#remove commented lines
for line in lines:
    if re.match("\s*#", line):
        lines.remove(line)

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
            line = match('\s+(.*)\n').group(1)
            definedSequences[lastDefined]["commands"].append(line)
    i += 1

commandList = []

#execute sequences and commands
while i < len(lines):
    line = lines[i]
    if len(line) >= 2:
        if re.match('\s*SW|\s*SR|\s*CW|\s*CR|\s*P|\s*EQ', line):
            commandList.append(line[:-1])
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
#    p = re.match('P\s+(.+)', c):
#    if p:
#        print p.group(1)
#    eq = re.match('EQ\s+(.)')

#    elif re.match('EQ'):
    #If read command
    if re.match('\s*.W', c):
        print send_message(c)
    #if write command
    elif re.match('\s*.R', c):
        print send_message(c)


#for j in xrange(100):
#   if j%10 == 0: print j
#   for i in xrange(0x100):
#      write_byte(0x74,i)
#      if read_byte(0x74) != i:
#	 print 'MISMATCH!'
################################################################################


################################################################################
#                                  Cleanup                                     #
################################################################################
ws.close()
infile.close()
################################################################################
