import RPi.GPIO as GPIO
import logging

class Pir:

    def __init__(self):
        self.pin = 23
        GPIO.setup(self.pin, GPIO.IN)


    def activate(self):

        def execute_on_detection(self):
            logging.debug('Movement detected')

        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=execute_on_detection)

    def deactivate(self):
        GPIO.cleanup(self.pin)

    def wait_for_movement(self):
        no_movement = True
        logging.info('Wait for movement...')
        while no_movement:
            if GPIO.event_detected(self.pin):
               no_movement = False
        logging.info('Movement detected')

if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    pirtest = Pir()

    pirtest.activate()

    pirtest.wait_for_movement()
    pirtest.deactivate()
    pirtest.wait_for_movement()
    pirtest.wait_for_movement()

    pirtest.wait_for_movement()

    pirtest.deactivate()
