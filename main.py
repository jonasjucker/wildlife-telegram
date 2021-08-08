import RPi.GPIO as GPIO
import logging

from sensors import Pir
from cam import WildCam
from bot import WildBot

def main():

    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
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

    try:
        while True:
            pir.wait_for_movement()
            cam.shot(nr_of_shots=3,pause=1,night_mode=True)
            cam.record(3,night_mode=True)
            bot.broadcast()

    except KeyboardInterrupt:
        cam.close()
        bot.stop()
        pir.deactivate()
        logging.info('Cleanup')

if __name__ == '__main__':
    main()
