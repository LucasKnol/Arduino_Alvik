from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()

def setup():
  alvik.begin()
  delay(1000)
  
def loop():
  left_tof, cleft_tof, center_tof, cright_tof, right_tof = alvik.get_distance()
  print("left:", left_tof)
  print("center left:", cleft_tof)
  print("Center:", center_tof)
  print("center right:", cright_tof)
  print("right:", right_tof)
  print(" ")
  delay(1000)
  
def cleanup():
  alvik.stop()
  
start(setup, loop, cleanup)