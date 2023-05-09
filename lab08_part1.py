import RPi.GPIO as GPIO
import time

# GPIO.cleanup()
PIN_BUTTON = 4
PIN_LED = 18
PIN_LED2 = 14
PIN_SERVO = 23
PIN_BUZZER = 24
# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BUZZER, GPIO.OUT)
GPIO.setup(PIN_LED, GPIO.OUT)
GPIO.setup(PIN_LED2, GPIO.OUT)
GPIO.setup(PIN_SERVO, GPIO.OUT)
GPIO.setup(PIN_BUTTON, GPIO.IN)
# servo
servo = GPIO.PWM(PIN_SERVO, 50) 
# 50 Hz PWM frequency
servo.start(0) # start at 0 degrees
time.sleep(1)
servo.ChangeDutyCycle(10) # 90 degrees
time.sleep(1)
servo.ChangeDutyCycle(1)
time.sleep(1)
# led
GPIO.output(PIN_LED, GPIO.HIGH)
time.sleep(1)
GPIO.output(PIN_LED, GPIO.LOW)
time.sleep(1)
# led2
GPIO.output(PIN_LED2, GPIO.LOW)
time.sleep(1)
GPIO.output(PIN_LED2, GPIO.HIGH)
time.sleep(1)
# buzzer
GPIO.output(PIN_BUZZER, GPIO.HIGH)
time.sleep(1)
GPIO.output(PIN_BUZZER, GPIO.LOW)
time.sleep(1)
# button
try:
    while True:
        if GPIO.input(PIN_BUTTON):
            print("pressed")
            
            time.sleep(1)
except KeyboardInterrupt:
    # print("STOP")
    None
except:  
    # print("Other error or exception occurred!" )
    None
finally:  
    GPIO.cleanup()
