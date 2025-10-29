from arduino import *
from arduino_alvik import ArduinoAlvik

# Global variables
Distance = 0
exitDistance = 0
complete = False

def calibration(alvik):
    """Rotate to find the largest (farthest) distance — the exit box."""
    global Distance, exitDistance
    
    alvik.set_wheels_speed(-15, 15)  # Rotate in place
    for _ in range(1000): 
        left, cleft, center, cright, right = alvik.get_distance()
        delay(10)
        if center > Distance:
            Distance = center
            # Flash LEDs when new max found
            alvik.left_led.set_color(1, 0, 0)
            alvik.right_led.set_color(1, 0, 0)
            delay(100)
            alvik.left_led.set_color(0, 0, 0)
            alvik.right_led.set_color(0, 0, 0)
    
    # Stop rotation and store the exit distance
    alvik.set_wheels_speed(0, 0)
    exitDistance = Distance
    delay(1000)

def celebration_dance(alvik):
    """Do a quick celebration sequence with LEDs and motion."""
    # Spin right
    alvik.left_led.set_color(1, 0, 0)
    alvik.right_led.set_color(0, 1, 0)
    alvik.set_wheels_speed(20, -20)
    delay(1000)

    # Spin left
    alvik.left_led.set_color(0, 0, 1)
    alvik.right_led.set_color(1, 1, 0)
    alvik.set_wheels_speed(-20, 20)
    delay(1000)

    # Wiggle
    alvik.left_led.set_color(1, 0, 1)
    alvik.right_led.set_color(0, 1, 1)
    for _ in range(2):
        alvik.set_wheels_speed(25, 25)
        delay(300)
        alvik.set_wheels_speed(-25, -25)
        delay(300)
    
    # Final spin and LED flash
    alvik.left_led.set_color(1, 1, 1)
    alvik.right_led.set_color(1, 1, 1)
    alvik.set_wheels_speed(20, -20)
    delay(1500)
    alvik.set_wheels_speed(0, 0)
    
    for _ in range(3):
        alvik.left_led.set_color(0, 1, 0)
        alvik.right_led.set_color(0, 1, 0)
        delay(200)
        alvik.left_led.set_color(0, 0, 0)
        alvik.right_led.set_color(0, 0, 0)
        delay(200)

def FindExit(alvik):
    global exitDistance, complete
    
    alvik.set_wheels_speed(-5, 5)  # Rotate slowly to scan
    for _ in range(20000):
        left, cleft, center, cright, right = alvik.get_distance()
        delay(1)
        
        if abs(exitDistance - center) < 3:
            alvik.set_wheels_speed(0, 0)
            delay(500)
            
            # Drive forward until 10 cm from the box
            while True:
                left, cleft, center, cright, right = alvik.get_distance()
                distance_to_box = center
                if distance_to_box <= 10:  # stop 10 cm from the box
                    break
                alvik.set_wheels_speed(30, 30)
                delay(50)  # small delay to avoid overwhelming sensor
                
            alvik.set_wheels_speed(0, 0)
            delay(500)
            
            # Celebration
            celebration_dance(alvik)
            complete = True
            break



def run_escape_room(alvik):
    """Main function to run the escape room routine."""
    global complete, Distance, exitDistance
    
    Distance = 0
    exitDistance = 0
    complete = False
    
    delay(1000)
    calibration(alvik)
    FindExit(alvik)
    
    alvik.stop()
    print("Escape room complete!")
