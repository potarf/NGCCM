from websocket import create_connection
import re

VERBOSITY = 0 

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

ws = create_connection("ws://192.168.1.22:8080/ws")

print send_message("SR 0x74")
print send_message("SW 0x74 0x02")
print send_message("SR 0x74")
write_byte(0x74,0xFF)
print read_byte_s(0x74)
#write_byte_data(0x70,0x3,0x0)
#write_byte_data(0x70,0x1,0x0)
#print read_byte_data_s(0x70,0x0)
#print read_byte_data_s(0x70,0x1)
#print read_byte_data_s(0x70,0x2)
#print read_byte_data_s(0x70,0x3)
#print read_byte_data_s(0x70,0x4)
#print read_byte_data_s(0x70,0x5)

print send_message("SW 0x1c 0x00")
print send_message("SR 0x1c")
print send_message("CR 0x1c 0x00")

#for j in xrange(100):
#   if j%10 == 0: print j
#   for i in xrange(0x100):
#      write_byte(0x74,i)
#      if read_byte(0x74) != i:
#	 print 'MISMATCH!'

ws.close()
