#!/usr/bin/python

import sys
import optparse
from smbus import SMBus
import time

#######################
# Get options
#######################

parser = optparse.OptionParser("usage: %prog [options] <decimal to write>")

#parser.add_option ('-a', dest='address', type='string',
#                   default = '70',
#                   help="Hex value of address of i2c device.")

options, args = parser.parse_args()

if len(args) != 1:
	print "Please specify decimal integer to write via i2c"
	sys.exit()


byteToWrite = int(args[0])
#######################

bus = SMBus(1)
address = 0x70

print bus.read_byte(address)
bus.write_byte(address, byteToWrite)
print bus.read_byte(address)
