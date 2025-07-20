import rpi_gpio as GPIO
import time
GPIO.setmode(GPIO.BCM)


# Set up GPIO 17 as output
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

# Turn on LED
GPIO.output(LED_PIN, GPIO.HIGH)

# Keep it on for 5 seconds
time.sleep(5)
GPIO.output(LED_PIN, GPIO.LOW)


# Clean up
GPIO.cleanup()
