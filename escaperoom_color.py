from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()
reachedEnd = 0

# Store colors as list of dicts: { 'rgb': (r,g,b), 'count': n }
saved_colors = []
stable_color = None
stable_count = 0
last_saved_color = None  # color of the last paper saved
stop_robot = False  

def forward(R, t):
    alvik.set_wheels_speed(R, R)
    delay(t)
    alvik.set_wheels_speed(0, 0)

def backward(R, t):
    alvik.set_wheels_speed(-R, -R)
    delay(t)
    alvik.set_wheels_speed(0, 0)

def turn_right():
  if stop_robot == True:
    alvik.set_wheels_speed(0, 0)
  else:
   alvik.set_wheels_speed(20, -20)
   delay(2400)

def color_distance(c1, c2):
    """Euclidean distance between two RGB tuples"""
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    return ((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2) ** 0.5

def find_closest_color(new_color, tolerance=20):
    """Return index of matching color within tolerance, or -1 if new"""
    for i, cdata in enumerate(saved_colors):
        if color_distance(new_color, cdata['rgb']) < tolerance:
            return i
    return -1

def blink_lights():
  for i in range(3):
    # Turn LEDs bright purple (red + blue)
    alvik.left_led.set_color(1, 0, 1)   # 1 = max brightness
    alvik.right_led.set_color(1, 0, 1)
    delay(500)  # wait 500 ms

    # Turn LEDs off
    alvik.left_led.set_color(0, 0, 0)
    alvik.right_led.set_color(0, 0, 0)
    delay(500)  # wait 500 ms


def backward_check_color():
    global stop_robot
    r, g, b = alvik.get_color_raw()
    current_color = (r, g, b)
    idx = find_closest_color(current_color)
    if idx != -1 and saved_colors[idx]['count'] == 1:
        print(f"Color #{idx+1} seen only once — turning right")
        turn_right()  # adjust speed/duration as needed
        stop_robot = True 
        blink_lights()
        alvik.set_wheels_speed(0, 0)
        

def setup():
    alvik.begin()
    delay(1000)
    print("\n=== Alvik Walking Color Scanner Started ===\n")

def loop():
    global reachedEnd, stable_color, stable_count, last_saved_color, stop_robot

    if stop_robot:
        alvik.stop()
        return 

    left, cleft, center, cright, right = alvik.get_distance()
    r, g, b = alvik.get_color_raw()
    current_color = (r, g, b)

    # End detection logic
    if center < 5 and reachedEnd == 0:
        reachedEnd += 1

    # === Moving forward ===
    if reachedEnd == 0:
        forward(50, 200)

        # Stabilize color readings
        if stable_color is None:
            stable_color = current_color
            stable_count = 1
        elif color_distance(current_color, stable_color) < 10:
            stable_count += 1
        else:
            stable_color = current_color
            stable_count = 1

        # Save new color only if stable and different from last saved
        if stable_count >= 3:
            if last_saved_color is None or color_distance(stable_color, last_saved_color) > 20:
                idx = find_closest_color(stable_color)
                if idx == -1:
                    saved_colors.append({'rgb': stable_color, 'count': 1})
                    print(f"N New Color #{len(saved_colors)} saved: {stable_color}")
                else:
                    saved_colors[idx]['count'] += 1
                    print(f"R Color #{idx+1} seen again ({saved_colors[idx]['count']}x)")
                
                last_saved_color = stable_color

            stable_count = 0

    # === Moving backward ===
    elif reachedEnd >= 1:
        backward(50, 200)
        backward_check_color()  # check color and turn if needed

    delay(20)

def cleanup():
    alvik.stop()
    print("\n=== Scanning Finished ===")
    print("Saved colors summary:\n")
    for i, cdata in enumerate(saved_colors, 1):
        print(f"Color #{i}: {cdata['rgb']} — Detected {cdata['count']} times")

start(setup, loop, cleanup)
