import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)

GPIO.setup(5,GPIO.OUT)

GPIO.setup(6,GPIO.OUT)
GPIO.cleanup()
