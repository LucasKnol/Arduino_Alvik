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

def spin_in_place(R, t):
    alvik.set_wheels_speed(R, -R)
    delay(t)
    alvik.set_wheels_speed(0, 0)

def blink_lights(times=5, interval=300):
    for _ in range(times):
        alvik.set_lights(0, 255, 0)  # green
        delay(interval)
        alvik.set_lights(0, 0, 0)    # off
        delay(interval)

def setup():
  alvik.begin()
  delay(1000)
  
def loop():
    left, cleft, center, cright, right = alvik.get_distance()
    print(cleft, "|", center, "|", cright)
    delay(100)

    # 1. Emergency back up if very close
    if cleft < 10 or center < 10 or cright < 10:
        backward(20, 500)
        return

    # 2. Move forward if center and sides are clear
    if center > 30 and cleft > 30 and cright > 20:
        forward(40, 500)
        return

    # 3. Spin if partially blocked but not critical
    if left < 20 or cleft < 20 or cright < 20 or right < 20:
        spin_in_place(20, 20)
        return

    # 4. Stop if unsure
    else:
      alvik.set_wheels_speed(0, 0)


  
def cleanup():
  alvik.stop()
  
start(setup, loop, cleanup)
