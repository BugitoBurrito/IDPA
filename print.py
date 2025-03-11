# Special handling for Octave 1 and 2 (GPIO 2 and 3)
print("\nApplying special configuration for Octave 1 and 2...")
try:
    # Force stronger pull-down for GPIO 2 (Octave 1)
    if 2 in OCTAVE_PINS:
        # Release and reclaim with explicit pull-down
        lgpio.gpio_free(h, 2)
        lgpio.gpio_claim_input(h, 2, lgpio.SET_PULL_DOWN)
        print("  Applied strong pull-down for GPIO 2 (Octave 1)")

    # Force stronger pull-down for GPIO 3 (Octave 2)
    if 3 in OCTAVE_PINS:
        # Release and reclaim with explicit pull-down
        lgpio.gpio_free(h, 3)
        lgpio.gpio_claim_input(h, 3, lgpio.SET_PULL_DOWN)
        print("  Applied strong pull-down for GPIO 3 (Octave 2)")
except Exception as e:
    print(f"  Error applying special configuration: {e}")  # !/usr/bin/env python3
import lgpio
import time
import sys

# Define GPIO pins for notes
NOTE_PINS = {
    22: "Bb",  # Corrected - GPIO 22 is Bb
    23: "B",  # Corrected - GPIO 23 is B
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

# Initialize lgpio and open the chip
try:
    h = lgpio.gpiochip_open(0)  # Open GPIO chip 0 (Raspberry Pi's main GPIO chip)
    print("LGPIO initialized successfully")
except Exception as e:
    print(f"LGPIO initialization error: {e}")
    print("Make sure lgpio is installed: sudo apt install python3-lgpio")
    print("Make sure you're running with sudo")
    sys.exit(1)

# Current octave
current_octave = 1

# Store previous GPIO states to detect changes
previous_states = {}

# Setup GPIO pins as inputs with pull-down resistors
try:
    print("Setting up GPIO pins...")

    # Set up all pins and track their initial states
    all_pins = list(NOTE_PINS.keys()) + list(OCTAVE_PINS.keys())
    for pin in all_pins:
        try:
            # Set up as input with pull-down
            lgpio.gpio_claim_input(h, pin, lgpio.SET_PULL_DOWN)

            # Store initial state
            previous_states[pin] = lgpio.gpio_read(h, pin)

            # Print setup info
            if pin in NOTE_PINS:
                print(f"  Set up note pin GPIO {pin} ({NOTE_PINS[pin]})")
            else:
                print(f"  Set up octave pin GPIO {pin} (Octave {OCTAVE_PINS[pin]})")
        except Exception as e:
            print(f"  Error setting up GPIO {pin}: {e}")

except Exception as e:
    print(f"Error setting up GPIO: {e}")
    lgpio.gpiochip_close(h)
    sys.exit(1)

# Main program
print("\n--- LGPIO Piano Test Program ---")
print("Press GPIO buttons to see which notes and octaves are detected")
print("Current octave: 1")
print("Press Ctrl+C to exit")

try:
    # Keep the program running
    while True:
        # Check all pins for state changes
        for pin in all_pins:
            try:
                current_state = lgpio.gpio_read(h, pin)

                # Check for rising edge (0 to 1)
                if current_state == 1 and previous_states[pin] == 0:
                    if pin in NOTE_PINS:
                        note = NOTE_PINS[pin]
                        print(f"NOTE PRESSED: {note} (GPIO {pin})")
                        print(f"Would play: Oktave {current_octave}/sound_okatve{current_octave}_{note}.mp3")
                    elif pin in OCTAVE_PINS:
                        current_octave = OCTAVE_PINS[pin]
                        print(f"OCTAVE CHANGED: Now using Octave {current_octave} (GPIO {pin})")
                        # Force print a message for Octave 1 and 2 (GPIOs 2 and 3)
                        if pin == 2:
                            print(f"Octave 1 selected (GPIO 2)")
                        elif pin == 3:
                            print(f"Octave 2 selected (GPIO 3)")

                # Update previous state
                previous_states[pin] = current_state
            except Exception as e:
                print(f"Error reading GPIO {pin}: {e}")
                # Prevent repeated error messages
                time.sleep(1)

        # Short delay to avoid high CPU usage
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nTest program exited")

finally:
    # Clean up LGPIO on exit
    lgpio.gpiochip_close(h)
    print("GPIO cleaned up")