import sounddevice as sd
import numpy as np
import hashlib
from mnemonic import Mnemonic
import qrcode
import cv2
from PIL import Image
from scipy.io.wavfile import write
from pynput.mouse import Listener
import threading
import time

# Recording parameters
DURATION = 10  # Duration of recording in seconds
SAMPLERATE = 44100  # Sampling rate
mouse_positions = []  # To track mouse movements
stop_mouse_listener = False  # To stop the mouse listener


def record_mouse_positions():
    """Track mouse movements for a limited duration."""
    def on_move(x, y):
        if stop_mouse_listener:
            return False  # Stop the listener
        mouse_positions.append((x, y))

    print("Move your mouse now to add entropy!")
    with Listener(on_move=on_move) as listener:
        while not stop_mouse_listener:
            time.sleep(0.1)  # Limit data collection frequency
    print("Mouse recording stopped.")


def record_webcam_and_save(duration, output_video="webcam_mouse_output.avi"):
    """Capture video from the webcam and overlay mouse movements."""
    width, height = 640, 480
    fps = 24
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    cap = cv2.VideoCapture(0)  # Use the webcam
    start_time = time.time()
    print("Webcam recording started. Keep interacting with your mouse.")
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            break

        # Draw mouse movements on the video
        for x, y in mouse_positions:
            cv2.circle(frame, (x % width, y % height), 5, (0, 0, 255), -1)  # Draw red circles

        # Write the frame to the video file
        video_writer.write(frame)

    cap.release()
    video_writer.release()
    print("Webcam recording stopped.")


def display_webcam_live(output_video="webcam_mouse_output.avi"):
    """Display the recorded video in real-time."""
    cap = cv2.VideoCapture(output_video)
    print("Displaying the recorded video.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Webcam and Mouse Recording", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def record_entropy(duration, samplerate, output_audio="recorded_entropy.wav"):
    """Record audio and save it as a WAV file for entropy."""
    print(f"Recording {duration} seconds of audio for entropy...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is complete
    print("Audio recording complete.")

    # Save the audio to a WAV file
    write(output_audio, samplerate, audio_data)
    print(f"Audio saved to {output_audio}")
    return audio_data.tobytes()


def normalize_mouse_positions():
    """Normalize mouse positions to ensure values are within the range of 0-255."""
    normalized = []
    for x, y in mouse_positions:
        normalized.append(x % 256)
        normalized.append(y % 256)
    return bytes(normalized)


def generate_seed_from_entropy(entropy_bytes):
    """Generate a BIP-39 seed phrase using combined entropy."""
    hash_bytes = hashlib.sha256(entropy_bytes).digest()  # Compute SHA256 hash
    mnemonic = Mnemonic("english")  # Initialize BIP-39 mnemonic generator
    seed_phrase = mnemonic.to_mnemonic(hash_bytes)
    return seed_phrase


def generate_qr_code(data, output_path="seed_qr.png"):
    """Generate a QR code for the seed phrase and save it as an image."""
    qr = qrcode.QRCode(
        version=1,  # Control the size of the QR code (1 is the smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    print(f"QR code saved at {output_path}")
    return output_path


def main():
    global stop_mouse_listener
    try:
        # Start mouse tracking in a separate thread
        mouse_thread = threading.Thread(target=record_mouse_positions)
        mouse_thread.start()

        # Record video from the webcam in a separate thread
        webcam_thread = threading.Thread(target=record_webcam_and_save, args=(DURATION,))
        webcam_thread.start()

        # Record audio for entropy and save it
        entropy_bytes = record_entropy(DURATION, SAMPLERATE)

        # Wait for the recording period to end
        time.sleep(DURATION)

        # Stop the mouse listener
        stop_mouse_listener = True
        mouse_thread.join()
        webcam_thread.join()

        # Normalize mouse data
        normalized_mouse_data = normalize_mouse_positions()

        # Combine all entropy sources
        combined_entropy = entropy_bytes + normalized_mouse_data

        # Generate the seed phrase
        seed_phrase = generate_seed_from_entropy(combined_entropy)
        print("\nGenerated Seed Phrase:")
        print(seed_phrase)

        # Generate and save the QR code for the seed phrase
        qr_path = generate_qr_code(seed_phrase)

        # Display the recorded video
        display_webcam_live(output_video="webcam_mouse_output.avi")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
