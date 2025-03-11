#!/usr/bin/env python3
import RPi.GPIO as GPIO
import pygame
import time
import os
import sys
from threading import Thread

# Make sure pygame is installed
try:
    pygame.init()
    pygame.quit()  # Immediately quit to avoid resource issues
except ImportError:
    print("Pygame not installed. Please install with:")
    print("sudo pip3 install pygame")
    sys.exit(1)

# Check for Raspberry Pi 5
import platform
import subprocess


def is_raspberry_pi_5():
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read()
            return 'Raspberry Pi 5' in model
    except:
        return False


is_pi5 = is_raspberry_pi_5()
if is_pi5:
    print("Detected Raspberry Pi 5")
    # Pi 5 may need different audio configuration
    try:
        # Check if audio is configured
        subprocess.run(['amixer'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Audio system detected")
    except:
        print("Note: You may need to configure audio output with:")
        print("sudo raspi-config")
        print("Navigate to System Options -> Audio -> and select your preferred output")

# Initialize pygame mixer with error handling
try:
    # Pi 5 often works better with these settings
    if is_pi5:
        pygame.mixer.init(48000, -16, 2, 4096)
        print("Audio initialized with Pi 5 optimized settings")
    else:
        pygame.mixer.init(44100, -16, 2, 2048)
        print("Audio initialized successfully")
except Exception as e:
    print(f"Error initializing audio: {e}")
    print("Trying alternative audio initialization...")
    try:
        # Try with different frequency
        pygame.mixer.init(48000, -16, 1, 4096)
        print("Audio initialized with alternative parameters")
    except Exception as e:
        print(f"Alternative audio initialization failed: {e}")
        print("Audio playback may not be available.")
        print("For Raspberry Pi 5, try these steps:")
        print("1. Run 'sudo raspi-config'")
        print("2. Go to System Options -> Audio")
        print("3. Select your preferred output device")
        print("4. Reboot the Pi")

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
    7: "Eb",  # Added Eb on GPIO 7
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
        # Check if mixer is initialized
        if not pygame.mixer.get_init():
            print("Mixer not initialized, attempting to reinitialize...")
            try:
                pygame.mixer.init(44100, -16, 2, 2048)
            except:
                print("Failed to initialize audio again.")
                return

        # Stop any currently playing sounds
        pygame.mixer.music.stop()

        # Load and play the sound
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

        print(f"Successfully started playback of {sound_path}")
    except Exception as e:
        print(f"Error playing sound: {e}")
        print("Try running: 'sudo amixer cset numid=3 1' to set audio to headphone jack")
        print("Or 'sudo amixer cset numid=3 2' to set audio to HDMI")


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