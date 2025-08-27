from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()

def setup():
  alvik.begin()
  delay(1000)
  
def loop():
  #straight ahead
  alvik.set_wheels_speed(40, 40)
  delay(2000)

  #90 degrees
  alvik.set_wheels_speed(20, 0)
  delay(4800)

  #180 degrees
  alvik.set_wheels_speed(40, 0)
  delay(4800)

def cleanup():
  alvik.stop()
  
start(setup, loop, cleanup)