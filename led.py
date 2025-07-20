import rpi_gpio as GPIO
import time
GPIO.setmode(GPIO.BCM)
BUZZER_PIN = 18
GPIO.setup(BUZZER_PIN, GPIO.OUT)


# Set up GPIO 17 as output
LED_PIN = 17
GPIO.setup(LED_PIN, GPIO.OUT)

# Turn on LED
GPIO.output(LED_PIN, GPIO.HIGH)
GPIO.output(BUZZER_PIN, GPIO.HIGH)

# Keep it on for 5 seconds
time.sleep(20)
GPIO.output(LED_PIN, GPIO.LOW)
GPIO.output(BUZZER_PIN, GPIO.LOW)


# Clean up
GPIO.cleanup()
