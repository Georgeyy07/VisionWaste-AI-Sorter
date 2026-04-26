# VisionWaste AI-Sorter
# AUTHORS: George Kassir and Mazen Elsabban

## Features
- AI Powered Answering: Uses the LLava model via Ollama to identify waste items through a webcam.
- Automatic Sorting: Three servo motors prop up lids for hands free sorting.
- Visual Indication: Color coded LEDs provide immediate feedback on classification results.

## Dependencies and Libraries

Laptop Side (Server)
- Ollama: To run the LLava vision model.
- Flask: To host the classification API.
- OpenCV (cv2): To handle webcam image capture.
- Requests: To communicate with the Ollama API.

Raspberry Pi Pico 2 W Side (Firmware)
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
- LED Trash - GPIO 10 - Digital Out
- LED Compost - GPIO 15 - Digital Out
- GRND in any respected position on Pico


## Build and Run Instructions

## 1. Setup the AI Server (Laptop)
1. Install Ollama and pull the model: "ollama pull llava", check if pulled -> "ollama list".
2. Install Python libraries: "pip install flask opencv-python requests".
3. Run the server: "python webcam.py".

## 2. Setup the Pico 2 W
1. Open pico.py and update the following:
   - ssid: Your WiFi Name.
   - password: Your WiFi Password.
   - serverIP: The Local IP of your laptop (note public IP does not equal local IP).
2. Upload pico.py to your Raspberry Pi Pico 2 W using a proper IDE.

### 3. Testing
- Run demo.py first to ensure all Servos and LEDs are wired correctly and moving to the right angles.
- Once confirmed, run webcam.py first using the top right run button (for VScode)
- Then run pico.py using the bottom run buttom for micropico to start the live classification loop.


# This project has been super fun and educational. I hope you find the documentation and code useful for your own builds. Feedback is always welcome, feel free to open an issue or pull a request! Yours Truly George and Mazen. 
