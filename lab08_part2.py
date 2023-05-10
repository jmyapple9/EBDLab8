import threading
import RPi.GPIO as GPIO
import time

BUTTON = 4
LED1, LED2= 14, 18
SERVO = 23
BUZZER = 24
timer = 0.2
servo_max, servo_min = 7, 2
servo_current = servo_min
state, prev_state = 0, 0
# STATE = {
#     NO_TRAIN: 0,        # 0: no train
#     COME_WARNING: 1,    # 1: coming warning
#     PASSING: 2,         # 2: passing
#     LEAVE_WARNING: 3    # 3: leaving warning
# }

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN)
servo = GPIO.PWM(SERVO, 50) # 50 Hz PWM frequency
servo.start(2) # start at 0 degrees

def led_buzzer_flash():
    while not stop_event.is_set():
        if state in {1,2,3}:
            GPIO.output(LED1, GPIO.HIGH)
            GPIO.output(LED2, GPIO.LOW)
            GPIO.output(BUZZER, GPIO.HIGH)
            time.sleep(timer)
            GPIO.output(LED1, GPIO.LOW)
            GPIO.output(LED2, GPIO.HIGH)
            GPIO.output(BUZZER, GPIO.LOW)
            time.sleep(timer)
        else:
            GPIO.output(LED1, GPIO.LOW)
            GPIO.output(LED2, GPIO.LOW)
            GPIO.output(BUZZER, GPIO.LOW)


def motor():
    global servo_current
    while not stop_event.is_set():
        if state == 1:
            if servo_current < servo_max:
                servo_current += 0.5
            else:
                servo_current = servo_max
        elif state == 3:
            if servo_current > servo_min:
                servo_current -= 0.5
            else:
                servo_current = servo_min
        else:
            None
        
        servo.ChangeDutyCycle(servo_current)
        time.sleep(timer)



if __name__ == '__main__':
    stop_event = threading.Event()
    thread1 = threading.Thread(target=led_buzzer_flash)
    thread2 = threading.Thread(target=motor)

    thread1.start()
    thread2.start()

    try:
        None
        while True:
            if prev_state == 0:
                if GPIO.input(BUTTON):
                    print("pressed")
                    state = 1
                    time.sleep(timer)
                else:
                    state = 0
            elif prev_state == 1:
                if servo_current == servo_max:
                    state = 2
                else:
                    state = 1
            elif prev_state == 2:
                if GPIO.input(BUTTON):
                    print("pressed")
                    state = 3
                    time.sleep(timer)
                else:
                    state = 2
            elif prev_state == 3:
                if servo_current == servo_min:
                    state = 0
                else:
                    state = 3
            else:
                print("ERROR STATE!")


            # if GPIO.input(PIN_BUTTON):
            #     print("pressed")
            #     time.sleep(timer)
            prev_state = state
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        stop_event.set()
    finally:
        # thread1.join()
        # thread2.join()
        GPIO.cleanup()
        print("clean up")
        # print("Done")
