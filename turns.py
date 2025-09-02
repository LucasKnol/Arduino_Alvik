from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()

def forward(R, t):
    alvik.set_wheels_speed(R, R)
    delay(t)
    alvik.set_wheels_speed(0, 0)

def backward(R, t):
    alvik.set_wheels_speed(-R, -R)
    delay(t)
    alvik.set_wheels_speed(0, 0)

def pivot_90_right():
  alvik.set_wheels_speed(20, 0)
  delay(4800)

def pivot_90_left():
  alvik.set_wheels_speed(0, 20)
  delay(4800)

def spin_90_right():
  alvik.set_wheels_speed(20, -20)
  delay(2400)

def spin_90_left():
  alvik.set_wheels_speed(-20, 20)
  delay(2400)

def smooth_90_right():
  alvik.set_wheels_speed(30, 10)
  delay(4800)

def smooth_90_left():
  alvik.set_wheels_speed(10, 30)
  delay(4800)

def setup():
  alvik.begin()
  delay(1000)
  
def loop():
  #first int is wheelspeed second is the delay
  forward(40, 1000)
  pivot_90_right()
  pivot_90_left()
  backward(40, 1000)
  spin_90_right()
  spin_90_left()
  forward(40, 1000)
  smooth_90_right()
  smooth_90_left()

def cleanup():
  alvik.stop()
  
start(setup, loop, cleanup)