import RPi.GPIO as GPIO
import logging
import argparse
import time
import sys

from sensors import Pir
from cam import WildCam
from bot import WildBot

def shutdown(cam,bot,pir):
        cam.close()
        bot.stop()
        pir.deactivate()
        logging.info('Shutdown')
        sys.exit(0)

def main():

    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level=logging.INFO
    )

    logger = logging.getLogger(__name__)


    parser = argparse.ArgumentParser()

    parser.add_argument('--bot_token', \
                        dest='bot_token', \
                        type=str, \
                        help='unique token of bot (KEEP PRIVATE!)')

    args = parser.parse_args()

    GPIO.setmode(GPIO.BCM)

    pir = Pir()
    pir.activate()

    cam = WildCam()
    bot = WildBot(args.bot_token)

    snooze = 5

    logging.info('Enter infinite loop')
    while True:
        logging.debug('loop iteration')

        # normal mode
        if bot.is_sensible_to_motion:
            pir.wait_for_movement()

            if bot.is_sensible_to_motion:
                photos = cam.shot(nr_of_shots=3,pause=4,night_mode=False)
                #video = cam.record(10,night_mode=True)
                bot.broadcast(photos,[])

        # test mode
        if bot.user_wants_test:
            bot.user_wants_test = False
            photos,videos = cam.test()
            bot.broadcast(photos,videos)

        # shutdown
        if bot.user_wants_shutdown:
            shutdown(cam,bot,pir)

        logging.info(f'sleep {snooze}s ...')
        time.sleep(snooze)

if __name__ == '__main__':
    main()
