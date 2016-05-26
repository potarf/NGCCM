import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
import re
from smbus import SMBus


VERBOSITY = 2

bus = SMBus(1)

def logerror(severity,str):
    if VERBOSITY >= severity:
	print time.asctime() + ': ' + str

def i2c_simple_read(address):
  try:
    value = bus.read_byte(address)
    logerror(2,'i2C SR addr=0x%02x OK val=0x%02x' % (address,value))
    return value
  except IOError:
    logerror(1,'i2C SR addr=0x%02x IOError' % address)
    return None

def i2c_simple_write(address,value):
  try:
    bus.write_byte(address,value)
    logerror(2,'i2C SW addr=0x%02x val=0x%02x OK' % (address,value))
    return True
  except IOError:
    logerror(1,'i2C SW addr=0x%02x val=0x%02x IOError' % (address,value))
    return None

def i2c_complex_read(address,register,length):
  try:
    value = bus.read_i2c_block_data(address,register,length)
#    logerror(2,'i2C SR addr=0x%02x reg=0x%02x OK val=0x%02x' % (address,register,value))
    return value
  except IOError:
    logerror(1,'i2C SR addr=0x%02x reg=0x%02x IOError' % (address,register))
    return None

def i2c_complex_write(address,register,value):
  try:
    bus.write_byte_data(address,register,value)
    logerror(2,'i2C SW addr=0x%02x reg=0x%02x val=0x%02x OK' % (address,register,value))
    return True 
  except IOError:
    logerror(1,'i2C SW addr=0x%02x reg=0x%02x val=0x%02x IOError' % (address,register,value))
    return None


  
    
class WSHandler(tornado.websocket.WebSocketHandler):

  def open(self):
    logerror(2,'Connection Established')

  def on_message(self, message):
    logerror(2,'Received message: %s' % message)

    match = re.search(r"SR\s+(\w+)",message,re.I|re.X)
    if match:
	addr = match.group(1)
	value = i2c_simple_read(int(addr,0))
        if (value != None):
            self.write_message(message + ' OK ' + hex(value))
	else:
	    self.write_message(message + ' ER')
        return

    match = re.search(r"SW\s+(\w+)\s+(\w+)",message,re.I|re.X)
    if match:
        addr = match.group(1)
        value = match.group(2)
        ret = i2c_simple_write(int(addr,0),int(value,0))
        if (ret != None):
            self.write_message(message + ' OK')
        else:
            self.write_message(message + ' ER')
        return

    match = re.search(r"CR\s+(\w+)\s+(\w+)",message,re.I|re.X)
    if match:
        addr = match.group(1)
        register = match.group(2)
        ret = i2c_complex_read(int(addr,0),int(register,0),4)
        if (ret != None):
            formattedMessage = ' '.join([message, 'OK']+ret)
            self.write_message(formatterMessage)
            #self.write_message(message + ' OK ' + hex(ret))
        else:
            self.write_message(message + ' ER')
        return
    
    match = re.search(r"CW\s+(\w+)\s+(\w+)\s+(\w+)",message,re.I|re.X)
    if match:
        addr = match.group(1)
        register = match.group(2)
        value = match.group(3)
        ret = i2c_complex_write(int(addr,0),int(register,0),int(value,0))
        if (ret != None):
            self.write_message(message + ' OK')
        else:
            self.write_message(message + ' ER')
        return


  def on_close(self):
    logerror(2,'Connection Closed')

application = tornado.web.Application([(r'/ws', WSHandler),])

if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8080)
  tornado.ioloop.IOLoop.instance().start()
