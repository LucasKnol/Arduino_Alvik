from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()

horizontal_count = 0   # counts how many times robot is horizontal
was_tilted = False     # assume robot starts flat

def setup():
    alvik.begin()
    delay(1000)

def loop():
    global horizontal_count, was_tilted

    # Read orientation sensor values
    roll, pitch, yaw = alvik.get_orientation()

    # Force pitch to always be positive
    pitch = abs(pitch)

    print("Pitch:", pitch, "Roll:", roll)
    delay(100)

    # Default movement
    if horizontal_count <= 1:
        alvik.set_wheels_speed(30, 30)

    # Check if robot is horizontal
    if pitch < 3:
        if was_tilted:  # Only count if coming from tilted
            horizontal_count += 1
            was_tilted = False   # Mark as flat
            if horizontal_count == 1:
                alvik.set_wheels_speed(0, 0)  # stop briefly
                alvik.left_led.set_color(1, 1, 0)  # yellow
                delay(5000)
                alvik.set_wheels_speed(30, 30)  # continue moving
                alvik.left_led.set_color(0, 0, 0)  # off
            elif horizontal_count == 2:
                alvik.set_wheels_speed(0, 0)  # stop completely
                alvik.left_led.set_color(0, 1, 1)  # cyan
                delay(500)
                blink_purple()
    else:
        # Robot is tilted → reset flag so next flat counts
        was_tilted = True


def blink_purple():
    # reset colors first
    alvik.left_led.set_color(0, 0, 0)
    alvik.right_led.set_color(0, 0, 0)
    delay(200)

    i = 0
    while i < 3:
        # Turn LEDs bright purple
        alvik.left_led.set_color(255, 0, 255)   # red + blue
        alvik.right_led.set_color(255, 0, 255)
        delay(500)  # 500 milliseconds
    
        # Turn LEDs off
        alvik.left_led.set_color(0, 0, 0)
        alvik.right_led.set_color(0, 0, 0)
        delay(500)  # 500 milliseconds
    
        i += 1

# for i in range(3): 
  # alvik.left_led.set_color(255, 0, 255) 
  # bright purple (red + blue) 
  # alvik.right_led.set_color(255, 0, 255) 
  # delay(500) 
  # alvik.left_led.set_color(0, 0, 0) # off # alvik.right_led.set_color(0, 0, 0) 
  # delay(500)


def cleanup():
    alvik.stop()

start(setup, loop, cleanup)
