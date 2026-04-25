# VisionWaste AI-Sorter
EECS1021
# AUTHORS: George Kassir and Mazen Elsabban

## Features
- AI Powered Answering: Uses the LLava model via Ollama to identify waste items through a webcam.
- Automatic Sorting: Three servo motors actuate lids for hands-free sorting.
- Visual Indication: Color coded LEDs provide immediate feedback on classification results.

## Dependencies and Libraries

Laptop Side (Server)
- Ollama: To run the LLava vision model.
- Flask: To host the classification API.
- OpenCV (cv2): To handle webcam image capture.
- Requests: To communicate with the Ollama API.

Pico 2 W Side (Firmware)
- MicroPython Firmware (Pico 2 W compatible)
- urequests: For making HTTP calls to the laptop.
- machine: For Pin and PWM (Servo/LED) control.
- network: For WiFi connecting.

## Hardware Setup

Components
- Raspberry Pi Pico 2 W
- 3x Servo Motors (Recycling, Trash, Compost)
- 3x LEDs (Recycling, Trash, Compost)
- Breadboard and Jumper Wires
- Laptop utilizing laptop webcam

Pin Mapping
- Servo Recycling - GPIO 4 - PWM Signal 
- Servo Trash - GPIO 9 - PWM Signal
- Servo Compost - GPIO 14 - PWM Signal
- LED Recycling - GPIO 5 - Digital Out
- LED Trash - GPIO 10 - Digital Out -
- LED Compost - GPIO 15 - Digital Out 

## Build and Run Instructions

## 1. Setup the AI Server (Laptop)
1. Install ollama and pull the model: "ollama pull llava", check if pulled -> "ollama list".
2. Install Python libraries: "pip install flask opencv-python requests".
3. Run the server: "python webcam.py.

## 2. Setup the Pico 2 W
1. Open pico.py and update the following:
   - ssid: Your WiFi Name.
   - password: Your WiFi Password.
   - serverIP: The Local IP of your laptop (note public IP does not equal local IP).
2. Upload pico.py to your Raspberry Pi Pico using the proper IDE.

### 3. Testing
- Run demo.py first to ensure all Servos and LEDs are wired correctly and moving to the right angles.
- Once confirmed, run pico.py to start the live classification loop.


# It's been great working on this project, hopefully you can enjoy it too.
