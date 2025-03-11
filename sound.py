#!/usr/bin/env python3
import pygame
import os
import time
import sys
import subprocess


def check_audio_devices():
    """Check and display available audio devices"""
    print("Checking audio configuration...")

    # Check audio outputs using amixer
    try:
        result = subprocess.run(['amixer', 'cget', 'numid=3'],
                                capture_output=True, text=True)
        print("Current audio output setting:")
        print(result.stdout)
    except:
        print("Could not check amixer settings")

    # Try to get ALSA device info
    try:
        result = subprocess.run(['aplay', '-l'],
                                capture_output=True, text=True)
        print("\nAvailable audio devices:")
        print(result.stdout)
    except:
        print("Could not list audio devices")


def set_audio_output(output):
    """Set audio output: 0=auto, 1=headphone jack, 2=HDMI"""
    try:
        subprocess.run(['amixer', 'cset', 'numid=3', str(output)])
        print(f"Set audio output to: {output}")
        if output == 0:
            print("Output: Auto")
        elif output == 1:
            print("Output: 3.5mm Headphone Jack")
        elif output == 2:
            print("Output: HDMI")
    except Exception as e:
        print(f"Error setting audio output: {e}")


def play_first_sound(output_device=None):
    # Check audio devices first
    check_audio_devices()

    # Set output device if specified
    if output_device is not None:
        set_audio_output(output_device)

    # Initialize pygame mixer with error handling
    try:
        pygame.mixer.init(48000, -16, 2, 4096)
        print("Audio initialized successfully")
    except Exception as e:
        print(f"Error initializing audio: {e}")
        print("Trying alternative audio initialization...")
        try:
            # Try with different parameters
            pygame.mixer.init(44100, -16, 2, 2048)
            print("Audio initialized with alternative parameters")
        except Exception as e:
            print(f"Alternative audio initialization failed: {e}")
            print("Audio playback may not be available.")
            sys.exit(1)

    # Set volume to maximum
    try:
        pygame.mixer.music.set_volume(1.0)
        print("Volume set to maximum")
    except Exception as e:
        print(f"Could not set volume: {e}")

    # Set the path to the first sound (C note in Octave 1)
    sound_path = "Oktave 1/sound_okatve1_C.mp3"

    # Check if file exists
    if not os.path.exists(sound_path):
        print(f"Error: Sound file not found: {sound_path}")
        print("Make sure you have the correct folder structure and file.")
        sys.exit(1)

    try:
        print(f"Playing: {sound_path}")

        # Load and play the sound
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

        print("Sound playing now...")

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        print("Playback finished")

    except Exception as e:
        print(f"Error playing sound: {e}")
        print("\nTroubleshooting tips:")
        print("1. Try headphone jack: 'sudo amixer cset numid=3 1'")
        print("2. Try HDMI: 'sudo amixer cset numid=3 2'")
        print("3. Check system volume: 'amixer set Master 100%'")
        print("4. Install codecs: 'sudo apt-get install -y libmpg123-dev'")

    finally:
        # Clean up pygame
        pygame.mixer.quit()


if __name__ == "__main__":
    print("Sound Test: Playing C note from Octave 1")

    # Check if output device was specified
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        output_device = int(sys.argv[1])
        play_first_sound(output_device)
    else:
        print("No output device specified. Using system default.")
        print("You can specify an output device: python3 sound.py [0|1|2]")
        print("  0 = Auto, 1 = Headphone Jack, 2 = HDMI")
        play_first_sound()