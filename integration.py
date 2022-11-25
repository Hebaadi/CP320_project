

import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
triggerPIN = 18
echoPIN = 24
servoPIN = 17
motor_clockwise = 5
motor_anticlockwise = 6


#set GPIO direction (IN / OUT)
GPIO.setup(triggerPIN, GPIO.OUT)
GPIO.setup(echoPIN, GPIO.IN)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(motor_clockwise, GPIO.OUT)
GPIO.setup(motor_anticlockwise, GPIO.OUT)


#start servo at angle 0
servo = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
servo.start(2.5) # Initialization
 
def distance():
    # set Trigger to HIGH
    GPIO.output(triggerPIN, True)
 
    # pulse for 10 micro seconds
    time.sleep(0.00001)
    GPIO.output(triggerPIN, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echoPIN) == 0:
        StartTime = time.time()
 
    # time it took to get back
    while GPIO.input(echoPIN) == 1:
        StopTime = time.time()
 
    # time the sound took from sensor and back
    TimeElapsed = StopTime - StartTime

    # using speed and time period to calculate distance
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def set_servo(dutyCycle):
    #change the duty cycle
    servo.ChangeDutyCycle(dutyCycle)
    time.sleep(0.5)

    #calculate angle and print it
    angle = ((dutyCycle-2.5)/10)*180 #mapping duty cycle to angle in degrees, 2.5%-12.5% duty cycle turns servo 0-180 degrees
    print("Servo angle set to: " + str(angle) + "\n")





# main loop


try:
    while True:
        #getting distance
        dist = distance()
        print (" Distance: " + str(dist)+ "\n")

        #setting servo angle
        if dist<10:
            set_servo(2.5)
        elif dist>10 and dist<20:
            angle = ((dist-10)/10)+2.5 #mapping the distance to the duty cycle
            set_servo(angle)
        else:
            set_servo(12.5)

        #setting motor direction
        if dist>1 and dist<3:
            GPIO.output(motor_clockwise, TRUE)
            GPIO.output(motor_anticlockwise, FALSE)
        elif dist>3 and dist<5:
            GPIO.output(motor_clockwise, FALSE)
            GPIO.output(motor_anticlockwise, TRUE)
        else:
            GPIO.output(motor_clockwise, FALSE)
            GPIO.output(motor_anticlockwise, FALSE)

except KeyboardInterrupt:
    pass

servo.stop()
GPIO.cleanup()

