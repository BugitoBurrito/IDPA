import pygame
import os
import RPi.GPIO as GPIO
import time


def play_sound(sound_file):
    try:
        # Initialize pygame mixer
        pygame.mixer.init()

        # Check if file exists
        if not os.path.exists(sound_file):
            print(f"Error: File '{sound_file}' not found")
            return False

        # Load and play the sound
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

        # Wait for the sound to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error playing sound: {str(e)}")
        return False
    finally:
        pygame.mixer.quit()

    return True


if __name__ == "__main__":
    # GPIO Setup mit BOARD-Nummerierung
    GPIO.setmode(GPIO.BOARD)
    GPIO_PIN = 3  # Physischer Pin 3 entspricht GPIO2
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Pfad zur Sound-Datei
    sound_file = os.path.join("okatve", "sound_okatve1_A.mp3")

    # Speichern des vorherigen Zustands für die Flankenerkennung
    previous_state = GPIO.input(GPIO_PIN)

    print("Programm gestartet. Warte auf GPIO-Eingabe (Pin 3)...")

    try:
        while True:
            # Aktuellen Zustand lesen
            current_state = GPIO.input(GPIO_PIN)

            # Debug-Ausgabe
            print(f"Aktueller Zustand: {current_state}")

            # Positive Flanke erkennen (Wechsel von 0 auf 1)
            if current_state == 1 and previous_state == 0:
                print("Positive Flanke erkannt! Spiele Sound...")
                play_sound(sound_file)

            # Aktuellen Zustand für den nächsten Durchlauf speichern
            previous_state = current_state

            # Kurze Pause, um CPU-Last zu reduzieren
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Programm durch Benutzer beendet.")
    finally:
        GPIO.cleanup()