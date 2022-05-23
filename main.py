import RPi.GPIO as GPIO
import logging
import argparse
import time
import sys
import os

from sensors import Pir
from cam import WildCam
from bot import WildBot
from location import CamLocation
from events import EventHandler
from image_processing import collective_image

def bot_launch(bot_token,retry=3, wait=1):

    for i in range(retry):
        try:
            bot = WildBot(bot_token)
        except Exception as e:
            logging.warning(f'Bot cannot connect: {e}')
            logging.info(f'Retry again in {wait} seconds')
            bot = WildBot(bot_token, offline=True)
            time.sleep(wait)
        else:
            break

    return bot

def shutdown(cam,bot,pir):
        cam.close()
        pir.deactivate()
        bot_shutdown(bot)
        logging.info('Shutdown')
        sys.exit(0)

def bot_shutdown(bot):
    if bot.is_offline_for_failover:
        logging.info('Shutdown-failover-bot')
    else:
        bot.stop()
        logging.info('Shutdown-bot')

def main():

    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level=logging.INFO,
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

    event = EventHandler('photos','videos','test')

    bot = bot_launch(args.bot_token, retry=10, wait=5)

    spot = CamLocation(47.3,8.5,"Somewhere in the forest", "Switzerland", "Europe/Zurich")

    snooze = 5

    logging.info('Enter infinite loop')
    while True:
        logging.debug('loop iteration')

        # normal mode
        if bot.is_sensible_to_motion:
            pir.wait_for_movement()

            if bot.is_sensible_to_motion:
                photos = cam.shot(nr_of_shots=2,pause=10,night_mode=spot.is_night(),name_generator=event.new_record_name)
                #video = cam.record(10,night_mode=True, new_record_name,name_generator=event.new_record_name))

                if not bot.already_down:
                    logging.info('Skip boradcast for now')
                #    bot.broadcast(photos,[])

        # summary of all photo-events
        if bot.user_wants_event_summary:
            bot.user_wants_event_summary = False
            event_names = event.list('p',ignore=['.gitkeep','test'])
            counter = 0
            photos = []
            for name in event_names:
                photos = collective_image(name,'composites',25,identifier=counter)
                counter += 1
                bot.broadcast(photos,[],message=f'Event: {event.strip(name)}')

        # test mode
        if bot.user_wants_test:
            bot.user_wants_test = False
            photos,videos = cam.test(event.new_test_record_name)
            bot.broadcast(photos,videos)

        # shutdown
        if bot.user_wants_shutdown:
            shutdown(cam,bot,pir)

        # bot-shutdown
        if bot.user_wants_bot_shutdown and not bot.already_down:
            bot_shutdown(bot)
            bot_already_down = True

        # reconnect bot
        if bot.has_no_connection:
            bot_shutdown(bot)
            bot = bot_launch(args.bot_token,retry=5, wait=3)

        logging.info(f'snooze {snooze}s ...')
        time.sleep(snooze)

if __name__ == '__main__':
    main()
