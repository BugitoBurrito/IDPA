#!/usr/bin/env python3
import RPi.GPIO as GPIO
import pygame
import time
import os
from threading import Thread

# Initialize pygame mixer
pygame.mixer.init()

# Set GPIO mode and fix for "Cannot determine SOC peripheral base address" error
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
except Exception as e:
    print(f"GPIO initialization error: {e}")
    print("Attempting alternative initialization...")
    # Try with explicit hardware configuration
    import os

    os.environ['GPIOZERO_PIN_FACTORY'] = 'mock'
    # Alternative for RPi.GPIO
    # If you're running this on a specific Pi model, you might need to set:
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(...)

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
    # Note: Eb missing GPIO assignment in the Excel file
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

# Default octave
current_octave = 1

# Setup GPIO pins as inputs with pull-down resistors
try:
    for pin in NOTE_PINS.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    for pin in OCTAVE_PINS.keys():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
except Exception as e:
    print(f"Failed to setup GPIO pins: {e}")
    print("If you're running on a Pi, make sure you're running as root (sudo) or have proper permissions.")


# Sound player function
def play_sound(octave, note):
    sound_path = f"Oktave {octave}/sound_okatve{octave}_{note}.mp3"
    print(f"Playing: {sound_path}")

    # Check if file exists
    if not os.path.exists(sound_path):
        print(f"Error: Sound file not found: {sound_path}")
        return

    try:
        # Stop any currently playing sounds
        pygame.mixer.music.stop()

        # Load and play the sound
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing sound: {e}")


# GPIO event callbacks
def note_callback(channel):
    global current_octave
    note = NOTE_PINS[channel]

    # Create a new thread to play the sound
    sound_thread = Thread(target=play_sound, args=(current_octave, note))
    sound_thread.daemon = True
    sound_thread.start()


def octave_callback(channel):
    global current_octave
    current_octave = OCTAVE_PINS[channel]
    print(f"Switched to Octave {current_octave}")


# Add event detection for all pins (only trigger on rising edge)
try:
    # Make sure all pins are set up first
    for pin in NOTE_PINS.keys():
        # Double-check input setup
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=note_callback, bouncetime=300)

    for pin in OCTAVE_PINS.keys():
        # Double-check input setup
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=octave_callback, bouncetime=300)
except Exception as e:
    print(f"Error setting up event detection: {e}")
    print("Make sure all GPIO pins are properly configured as inputs.")

# Main program
try:
    print("GPIO Sound Player Running...")
    print(f"Current Octave: {current_octave}")
    print("Press Ctrl+C to exit")

    # Keep the program running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nExiting program")

finally:
    # Clean up GPIO on exit
    GPIO.cleanup()
    pygame.mixer.quit()