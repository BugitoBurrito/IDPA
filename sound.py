#!/usr/bin/env python3
import pygame
import os
import time
import sys


def play_first_sound():
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

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        print("Playback finished")

    except Exception as e:
        print(f"Error playing sound: {e}")
        print("Try running: 'sudo amixer cset numid=3 1' to set audio to headphone jack")
        print("Or 'sudo amixer cset numid=3 2' to set audio to HDMI")

    finally:
        # Clean up pygame
        pygame.mixer.quit()


if __name__ == "__main__":
    print("Sound Test: Playing C note from Octave 1")
    play_first_sound()