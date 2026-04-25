from machine import Pin, PWM
import time

servoRecycling = PWM(Pin(4))
servoTrash = PWM(Pin(9))
servoCompost = PWM(Pin(14))

ledRecycling = Pin(5, Pin.OUT)
ledTrash = Pin(10, Pin.OUT)
ledCompost = Pin(15, Pin.OUT)

for i in [servoRecycling, servoTrash, servoCompost]:
    i.freq(50)

def setServoAngle(servo, angle):
    minDuty = 1638
    maxDuty = 8192
    duty = int(minDuty + (maxDuty - minDuty) * (angle / 180))
    servo.duty_u16(duty)

def testServo(name, servo, led):
    print(f"Testing {name}...")
    led.value(1)
    
    print(f"  {name} : OPEN (180°)")
    setServoAngle(servo, 180)
    time.sleep(2)
    
    print(f"  {name} : CLOSE (0°)")
    setServoAngle(servo, 0)
    time.sleep(2)
    
    led.value(0)
    print(f"  {name} done.")

print("Starting \n")

testServo("Recycling", servoRecycling, ledRecycling)
testServo("Trash", servoTrash, ledTrash)
testServo("Compost", servoCompost, ledCompost)

print("Finished")