import RPi.GPIO as GPIO
import time
PIN_BUTTON = 4
PIN_LED1 = 18
PIN_LED2 = 14
PIN_SERVO = 23
PIN_BUZZER = 24
timer = 0.2
servo_max, servo_min = 7, 2
servo_current = 0
def blinkLED(sec):
    GPIO.output(PIN_LED1, GPIO.HIGH)
    GPIO.output(PIN_LED2, GPIO.LOW)
    time.sleep(sec)
    GPIO.output(PIN_LED1, GPIO.LOW)
    GPIO.output(PIN_LED2, GPIO.HIGH)
    time.sleep(sec)

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BUZZER, GPIO.OUT)
GPIO.setup(PIN_LED1, GPIO.OUT)
GPIO.setup(PIN_LED2, GPIO.OUT)
GPIO.setup(PIN_SERVO, GPIO.OUT)
GPIO.setup(PIN_BUTTON, GPIO.IN)

# servo
servo = GPIO.PWM(PIN_SERVO, 50) 
# 50 Hz PWM frequency
servo.start(2) # start at 0 degrees
# time.sleep(1)
# servo.ChangeDutyCycle(7) # 90 degrees
# time.sleep(1)
# servo.ChangeDutyCycle(1)
# time.sleep(1)
def ServoMove(Up, timer):
    global servo_current
    # for i in range(2,7,0.1)
    if Up:
        if servo_current < servo_max:
            servo_current += 1
        else:
            servo_current = servo_max
    else:
        if servo_current > servo_min:
            servo_current -= 1
        else:
            servo_current = servo_min
    time.sleep(timer)
    print(f'servo_current: {servo_current}')
    servo.ChangeDutyCycle(servo_current)

    # servo_current += 1
    # if servo_current >= servo_max:
    #     servo_current = servo_max
# led
def stopAll():
    GPIO.output(PIN_BUZZER, GPIO.LOW)
    GPIO.output(PIN_LED2, GPIO.LOW)
    GPIO.output(PIN_LED1, GPIO.LOW)
    # servo.start(2) # start at 0 degrees

# buzzer
def Buzz(sec):
    GPIO.output(PIN_BUZZER, GPIO.HIGH)
    time.sleep(sec)
    GPIO.output(PIN_BUZZER, GPIO.LOW)
    time.sleep(sec)
# button
train = False
try:
    while True:
        if GPIO.input(PIN_BUTTON):
            print("pressed")
            train = not train
            time.sleep(timer)
        if train:
            Buzz(timer)
            blinkLED(timer)
            # servo.ChangeDutyCycle(7) # 90 degrees
            ServoMove(train, timer)
        if not train:
            stopAll()
            if servo_current > 2:
                GPIO.output(PIN_BUZZER, GPIO.HIGH)
                blinkLED(timer)
            ServoMove(train, timer)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")
# except:
#    print("some error") 

finally:
   print("clean up")
   stopAll()
   servo.start(2)
   GPIO.cleanup() # cleanup all GPIO 