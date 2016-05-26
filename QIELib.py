#!/usr/bin/python

################################################################################
#                                    Setup                                     #
################################################################################

######from smbus import SMBus

#SMBus_Setup
#def SMBus_Setup():
#    return SMBus(1) #For Raspberry Pi using i2c bus 1

#bus = SMBus_Setup()

################################################################################
#                           Basic IO and expressions                           #
################################################################################

#SR : SimpleRead
def SR(bus, device):
    #simple read from device and return value
    return bus.read_byte(address)

#SW : SimpleWrite
def SW(bus, device, val):
    #simple write val to device
    bus.write_byte(device, val)

#CR : ComplexRead
def CR(bus, device, register):
    #read of register on device and return value
    return bus.read_byte_data(device, register)

#CW : ComplexWrite
def CW(bus, device, register, value):
    #write value to register on device
    bus.write_byte_data(device, register, value)

def EQ(a1, a2, cmd1, cmd2):
    cmd1 if a1 == a2 else cmd2

#def MISMATCH(A1, A2):
#    print "There was a mismatch: read " + str(A1) + " expected " + str(A2)

#def OK():
#    print "All is well!"

################################################################################
#                                 Basic tests                                  #
################################################################################
