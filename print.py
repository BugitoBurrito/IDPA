#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys

# Set GPIO mode with error handling
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    print("GPIO initialized successfully")
except Exception as e:
    print(f"GPIO initialization error: {e}")
    print("Make sure you're running with sudo")
    sys.exit(1)

# Define GPIO pins for notes
NOTE_PINS = {
    22: "B",
    23: "Bb",
    24: "A",
    10: "Ab",
    9: "G",
    25: "Gb",
    11: "F",
    8: "E",
    7: "Eb",
    0: "D",
    1: "Db",
    5: "C"
}

# Define GPIO pins for octaves
OCTAVE_PINS = {
    2: 1,  # GPIO 2 for Octave 1
    3: 2,  # GPIO 3 for Octave 2
    4: 3,  # GPIO 4 for Octave 3
    14: 4,  # GPIO 14 for Octave 4
    15: 5,  # GPIO 15 for Octave 5
    17: 6,  # GPIO 17 for Octave 6
    18: 7,  # GPIO 18 for Octave 7
}

# Current octave
current_octave = 1


# GPIO event callbacks
def note_callback(channel):
    note = NOTE_PINS[channel]
    print(f"NOTE PRESSED: {note} (GPIO {channel})")
    print(f"Would play: Oktave {current_octave}/sound_okatve{current_octave}_{note}.mp3")


def octave_callback(channel):
    global current_octave
    current_octave = OCTAVE_PINS[channel]
    print(f"OCTAVE CHANGED: Now using Octave {current_octave} (GPIO {channel})")


# Setup GPIO pins and event detection
try:
    print("Setting up GPIO pins...")

    # Set up note pins
    for pin in NOTE_PINS.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=note_callback, bouncetime=300)
        print(f"  Set up note pin GPIO {pin} ({NOTE_PINS[pin]})")

    # Set up octave pins
    for pin in OCTAVE_PINS.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=octave_callback, bouncetime=300)
        print(f"  Set up octave pin GPIO {pin} (Octave {OCTAVE_PINS[pin]})")

except Exception as e:
    print(f"Error setting up GPIO: {e}")
    GPIO.cleanup()
    sys.exit(1)

# Main program
print("\n--- GPIO Piano Test Program ---")
print("Press GPIO buttons to see which notes and octaves are detected")
print("Current octave: 1")
print("Press Ctrl+C to exit")

try:
    # Keep the program running
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nTest program exited")

finally:
    # Clean up GPIO on exit
    GPIO.cleanup()
    print("GPIO cleaned up")