import network # handles pico finding wifi
import urequests # pico visits website to get answer, makes the HTTP calling
import time # for blinking and sleeping between leds
from machine import Pin, PWM # added PWM for servos

# micropython libraries ^

ssid = "XXXXXXXX" 
password = 'XXXXXXXX' 

serverIP = "123.456.789.012" # Need local laptop IP, port, wifi name and password to connect, change accordingly
port = 5001
classifyURL = f"http://{serverIP}:{port}/classify"

#Specific LED pins
ledRecycling = Pin(5, Pin.OUT) 
ledTrash = Pin(10, Pin.OUT)
ledCompost = Pin(15, Pin.OUT)

#Specific servo pins
servoRecycling = PWM(Pin(4))
servoTrash = PWM(Pin(9))
servoCompost = PWM(Pin(14))

# standard frequency for most servos
servoRecycling.freq(50)
servoTrash.freq(50)
servoCompost.freq(50)

def settingServoAngle(servo, angle):
    # math to turn 0-180 degrees into numbers the pico understands
    min_duty = 1638 
    max_duty = 8192 
    duty = int(min_duty + (max_duty - min_duty) * (angle / 180))
    servo.duty_u16(duty)

def ledOff():
    ledRecycling.off()
    ledTrash.off()
    ledCompost.off() # reset before anything starts again

def blink(led, times=3, on_ms=500, off_ms=400):
    # blinking led function once answer is given
    for _ in range(times):
        led.on()
        time.sleep_ms(on_ms)
        led.off()
        time.sleep_ms(off_ms)

def connectWifi(): # Get pico connected to wifi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Connecting to WiFi", end="")
    for _ in range(20):
        if wlan.isconnected():
            print(f"\nConnected: {wlan.ifconfig()}")
            return True
        print(".", end="")
        time.sleep(1)
    print("\nFailed to connect.")
    return False

def getCategory():
    try:
        # ask AI for prompt reponse, max time 2 minutes
        response = urequests.get(classifyURL, timeout=120)
        
        # convert answer to json dictionary
        data = response.json()
        
        # close connection for speed and saving resource
        response.close()
        
        # Give back the category (default to "Trash" if something is weird)
        return data.get("category", "Trash")
        
        # Error handling
    except Exception as e:
        print("Request error, skipping this one:", e)
        return "Trash"
# if connection issues come, end the whole process
if not connectWifi():
    raise RuntimeError("WiFi connection failed")

print("Ready. Starting to classify...")

# Start with all bins closed (0 degrees)
settingServoAngle(servoRecycling, 0)
settingServoAngle(servoTrash, 0)
settingServoAngle(servoCompost, 0)

while True:
    ledOff() # resetting LEDs
    print("Classifying...")
    category = getCategory()
    print("Result:", category)

    if category == "Recycling":
        settingServoAngle(servoRecycling, 180) # Open door
        blink(ledRecycling)                  # Wait while blinking
        settingServoAngle(servoRecycling, 0) # Close door
        
    elif category == "Trash":
        settingServoAngle(servoTrash, 180) # Do this loop for all bin categories
        blink(ledTrash)
        settingServoAngle(servoTrash, 0)
        
    else:
        settingServoAngle(servoCompost, 180) # assume its compost, as prompt handles the wording error
        blink(ledCompost)
        settingServoAngle(servoCompost, 0)

    # wait 3 seconds before starting the next scan
    time.sleep(3)