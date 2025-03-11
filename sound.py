#!/usr/bin/env python3
import os
import subprocess
import sys
import time


def setup_audio():
    """Configure audio settings for Raspberry Pi"""
    try:
        # Set audio to headphone jack (most common output)
        subprocess.run(['amixer', 'cset', 'numid=3', '1'], stderr=subprocess.PIPE)

        # Set volume to 100%
        subprocess.run(['amixer', 'set', 'Master', '100%'], stderr=subprocess.PIPE)

        # Wait for settings to apply
        time.sleep(0.5)

        return True
    except Exception as e:
        print(f"Error setting up audio: {e}")
        return False


def play_sound(sound_path):
    """Play sound using mpg123 (most reliable for MP3 on Raspberry Pi)"""
    try:
        # Check if mpg123 is installed
        result = subprocess.run(['which', 'mpg123'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("Installing mpg123...")
            subprocess.run(['sudo', 'apt-get', 'update', '-y'], stderr=subprocess.PIPE)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'mpg123'], stderr=subprocess.PIPE)

        # Play sound using mpg123
        print(f"Playing sound: {sound_path}")
        subprocess.run(['mpg123', sound_path])
        return True

    except Exception as e:
        print(f"Error playing sound: {e}")
        return False


def main():
    # Sound path
    sound_path = "Oktave 1/sound_okatve1_C.mp3"

    # Check if file exists
    if not os.path.exists(sound_path):
        print(f"Error: Sound file not found: {sound_path}")
        print(f"Current directory: {os.getcwd()}")
        print("Make sure you have the correct folder structure and file.")
        sys.exit(1)

    # Set up audio
    print("Setting up Raspberry Pi audio...")
    setup_audio()

    # Play sound
    success = play_sound(sound_path)

    if success:
        print("Sound played successfully!")
    else:
        print("\nTroubleshooting:")
        print("1. Try setting audio output manually:")
        print("   sudo amixer cset numid=3 1  # For headphone jack")
        print("   sudo amixer cset numid=3 2  # For HDMI")
        print("2. Check connections to your speakers/headphones")
        print("3. Try playing directly with: mpg123 'Oktave 1/sound_okatve1_C.mp3'")
        print("4. Install audio packages: sudo apt-get install -y alsa-utils mpg123")


if __name__ == "__main__":
    print("Raspberry Pi Sound Test: Playing C note from Octave 1")
    main()