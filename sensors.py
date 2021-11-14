import RPi.GPIO as GPIO
import logging
from exchange import set_bot_action,is_bot_action

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
        no_bot_action = True
        logging.info('Wait for movement...')
        while no_movement and no_bot_action: 
            no_bot_action = not is_bot_action()

            if GPIO.event_detected(self.pin):
               no_movement = False
               logging.info('Movement detected')

        set_bot_action(False)
