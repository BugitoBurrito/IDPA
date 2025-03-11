#!/usr/bin/env python3
import lgpio as GPIO
import time
import sys

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
    2: 1,
    3: 2,
    4: 3,
    14: 4,
    15: 5,
    17: 6,
    18: 7,
}

# Current octave
current_octave = 1


def note_callback(chip, gpio, level, timestamp):
    if level == 1:
        note = NOTE_PINS.get(gpio, "Unknown")
        print(f"NOTE PRESSED: {note} (GPIO {gpio})")
        print(f"Would play: Oktave {current_octave}/sound_okatve{current_octave}_{note}.mp3")


def octave_callback(chip, gpio, level, timestamp):
    global current_octave
    if level == 1:
        current_octave = OCTAVE_PINS.get(gpio, current_octave)
        print(f"OCTAVE CHANGED: Now using Octave {current_octave} (GPIO {gpio})")


# Setup GPIO
try:
    chip = GPIO.open(0)  # Open GPIO chip 0
    print("Setting up GPIO pins...")

    # Set up note pins
    for pin in NOTE_PINS.keys():
        GPIO.set_mode(chip, pin, GPIO.INPUT)
        GPIO.set_pull_up_down(chip, pin, GPIO.PULL_DOWN)
        GPIO.callback(chip, pin, GPIO.RISING_EDGE, note_callback)
        print(f"  Set up note pin GPIO {pin} ({NOTE_PINS[pin]})")

    # Set up octave pins
    for pin in OCTAVE_PINS.keys():
        GPIO.set_mode(chip, pin, GPIO.INPUT)
        GPIO.set_pull_up_down(chip, pin, GPIO.PULL_DOWN)
        GPIO.callback(chip, pin, GPIO.RISING_EDGE, octave_callback)
        print(f"  Set up octave pin GPIO {pin} (Octave {OCTAVE_PINS[pin]})")

except Exception as e:
    print(f"Error setting up GPIO module: {e}")
    sys.exit(1)

# Main program
print("\n--- GPIO Piano Test Program ---")
print("Press GPIO buttons to see which notes and octaves are detected")
print("Current octave: 1")
print("Press Ctrl+C to exit")

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nTest program exited")

finally:
    GPIO.close(chip)
    print("GPIO cleaned up")
