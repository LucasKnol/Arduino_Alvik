from arduino import *
from arduino_alvik import ArduinoAlvik

alvik = ArduinoAlvik()
alvik.begin()
print("=== Arduino Alvik Program Launcher ===")

# Program list to run sequentially
programs = [
    'escaperoom_test.py',
    'escaperoom_ramp.py',
    'escaperoom_color.py'
]

for i, program in enumerate(programs, 1):
    print(f"\n>>> Running Program {i}: {program} <<<\n")
    alvik.set_builtin_led(True)

    try:
        # Execute the program file
        exec(open(program).read())
        print(f"\n✓ Program {i} completed successfully!")
    except Exception as e:
        print(f"✗ Error in {program}: {e}")

    # Ensure robot stops between programs
    alvik.stop()
    alvik.left_led.set_color(0, 0, 0)
    alvik.right_led.set_color(0, 0, 0)
    alvik.set_builtin_led(False)

    delay(1000)  # Small pause before next program

print("\n=== All programs completed! ===")
alvik.stop()
