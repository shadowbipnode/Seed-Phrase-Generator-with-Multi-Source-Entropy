# **Seed Phrase Generator with Multi-Source Entropy**

## **Description**
This Python script generates a **BIP-39 seed phrase** using multiple sources of entropy, including:
- **Audio**: Captures audio from the microphone.
- **Mouse movements**: Tracks mouse activity during the recording process.
- **Webcam video**: Captures real-time video frames from the webcam.

The script combines these data sources to ensure a highly random and secure seed phrase generation. It also generates a **QR code** of the seed phrase and saves all related files (audio, video, QR code) for verification purposes.

---

## **Key Features**
1. **Audio Entropy**:
   - Records 10 seconds of audio and uses raw data for entropy.

2. **Mouse Entropy**:
   - Captures mouse movements during the recording period.

3. **Webcam Entropy**:
   - Records video from the webcam to add additional randomness.

4. **Seed Phrase Generation**:
   - Generates a BIP-39-compliant seed phrase.

5. **QR Code Output**:
   - Saves the seed phrase as a QR code for easy storage.

6. **Output Files**:
   - Audio: `recorded_entropy.wav`
   - Video: `webcam_mouse_output.avi`
   - QR Code: `seed_qr.png`

---

## **Prerequisites**
Ensure you have Python 3.8 or later installed. Check your Python version with:
```bash
python3 --version
```

### Required Libraries
Install the necessary libraries using `pip`:
```bash
pip install sounddevice numpy hashlib mnemonic qrcode opencv-python pynput scipy pillow
```

---

## **Installation**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/asyscom/seed-phrase-generator.git
   cd seed-phrase-generator
   ```

2. **Create a Virtual Environment (Optional but Recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## **How to Use**
1. Run the script:
   ```bash
   python3 happy3.py
   ```

2. **During Execution**:
   - Move the mouse as instructed on-screen.
   - Speak or make noise near the microphone.
   - Stay in front of the webcam to add visual randomness.

3. **Outputs**:
   - `recorded_entropy.wav`: The audio recording.
   - `webcam_mouse_output.avi`: The video recording with mouse movements.
   - `seed_qr.png`: A QR code of the generated seed phrase.

4. **Seed Phrase**:
   - The seed phrase is printed in the terminal. 
   - Keep this phrase secure as it’s your key for recovery!

---

## **Entropy Levels**
This script combines three levels of entropy to create the seed phrase:

1. **Audio Entropy**:
   - Derived from raw audio data captured from the microphone.
   - Adds randomness through ambient noise and voice inputs.

2. **Mouse Entropy**:
   - Captures mouse movements during the recording.
   - Random mouse movement increases entropy significantly.

3. **Visual Entropy**:
   - Captures real-time frames from the webcam.
   - Frame data adds a layer of visual randomness.

The combined entropy ensures robust randomness and security for the generated seed phrase.

---

## **Security**
- **Offline Execution**:
  - Run the script on an air-gapped (offline) computer to prevent data leaks.

- **Backup Securely**:
  - Store the generated files (audio, video, QR code) in secure, offline locations.

- **QR Code**:
  - Never share the QR code with untrusted parties.

- **Seed Phrase**:
  - The seed phrase is your recovery key. Treat it as highly confidential and secure.

---

## **Known Issues**
1. **OpenCV GUI Timer Error**:
   - You may see a `QObject::killTimer` warning while displaying the video. This is a known OpenCV issue and does not affect functionality.

2. **Hardware Limitations**:
   - Ensure your microphone and webcam are functional before running the script.

---

## **Contributing**
If you’d like to contribute:
1. Fork the repository.
2. Create a branch for your feature:
   ```bash
   git checkout -b new-feature
   ```
3. Submit a pull request.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.
