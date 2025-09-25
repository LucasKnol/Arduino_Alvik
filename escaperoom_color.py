from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()
reachedEnd = 0  # keep your original counter

def forward(R, t):
    alvik.set_wheels_speed(R, R)
    delay(t)
    alvik.set_wheels_speed(0, 0)

def backward(R, t):
    alvik.set_wheels_speed(-R, -R)
    delay(t)
    alvik.set_wheels_speed(0, 0)

def setup():
    alvik.begin()
    delay(1000)

def loop():
    global reachedEnd
    left, cleft, center, cright, right = alvik.get_distance()
    print(cleft, "|", center, "|", cright)
    colors = alvik.get_color_raw()
    print(colors)
    delay(100)

    # Increment counter only once when center sensor sees something very close
    if center < 5 and reachedEnd == 0:
        reachedEnd += 1

    # Forward if nothing reached, backward if end reached
    if reachedEnd == 0:
        forward(50, 200) 
    elif reachedEnd >= 1:
        backward(50, 200)

def cleanup():
    alvik.stop()

start(setup, loop, cleanup)
