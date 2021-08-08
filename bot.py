import argparse
import logging
import time

from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)




def start(update: Update, context: CallbackContext):
    reply_text = "Hi! I am LonelyCam. If you want to subscribe write /subscribe. \
                  Write /unsubscribe to no longer receive cute pics"

    reply_keyboard = [
        ['/subscribe', '/unsubscribe'],
    ]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text(reply_text, reply_markup=markup)

def subscribe(update: Update, context: CallbackContext):
    reply_text = "You sucessfully subscribed."
    update.message.reply_text(reply_text)

    # add user to subscription list
    user_id = update.effective_user.id
    context.bot_data.setdefault('user_id', set()) # create key if not present
    context.bot_data['user_id'].add(user_id)

def unsubscribe(update: Update, context: CallbackContext):
    reply_text = "You sucessfully unsubscribed."
    update.message.reply_text(reply_text)

    # remove user from subscription list
    user_id = update.effective_user.id
    context.bot_data.setdefault('user_id', set()) # create key if not present
    if user_id in context.bot_data['user_id']:
        context.bot_data['user_id'].remove(user_id)
    print(context.bot_data.setdefault('user_id', set()))


def main() -> None:
    """Run the bot."""

    parser = argparse.ArgumentParser()

    parser.add_argument('--bot_token', \
                        dest='bot_token', \
                        type=str, \
                        help='unique token of bot (KEEP PRIVATE!)')


    args = parser.parse_args()

    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename='backup/bot.pkl')
    updater = Updater(args.bot_token, persistence=persistence)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('subscribe',subscribe, pass_args=True))
    dp.add_handler(CommandHandler('unsubscribe',unsubscribe, pass_args=True))

    # start the bot
    updater.start_polling()
    time.sleep(10)
    updater.stop()

    #updater.idle()

if __name__ == '__main__':
    main()
