import argparse
import logging

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    PicklePersistence,
    CallbackContext,
)

class WildBot:

    def __init__(self,token):

        # Create the Updater and pass it your bot's token.
        persistence = PicklePersistence(filename='backup/bot.pkl')
        self.updater = Updater(token, persistence=persistence)

        self.dp = self.updater.dispatcher
        self.dp.add_handler(CommandHandler('start',self._start))
        self.dp.add_handler(CommandHandler('subscribe',self._subscribe))
        self.dp.add_handler(CommandHandler('unsubscribe',self._unsubscribe))

        # start the bot
        self.updater.start_polling()

    def stop(self):
        self.updater.stop()

    def _start(update: Update, context: CallbackContext):
        reply_text = "Hi! I am LonelyCam. If you want to subscribe write /subscribe. \
                      Write /unsubscribe to no longer receive cute pics"

        reply_keyboard = [
            ['/subscribe', '/unsubscribe'],
        ]

        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(reply_text, reply_markup=markup)

    def _subscribe(self,update: Update, context: CallbackContext):
        reply_text = "You sucessfully subscribed."
        update.message.reply_text(reply_text)

        # add user to subscription list
        user_id = update.effective_user.id
        context.bot_data.setdefault('user_id', set()) # create key if not present
        context.bot_data['user_id'].add(user_id)

        logging.info(context.bot_data.setdefault('user_id', set()))

    def _unsubscribe(self,update: Update, context: CallbackContext):
        reply_text = "You sucessfully unsubscribed."
        update.message.reply_text(reply_text)

        # remove user from subscription list
        user_id = update.effective_user.id
        context.bot_data.setdefault('user_id', set()) # create key if not present
        if user_id in context.bot_data['user_id']:
            context.bot_data['user_id'].remove(user_id)

        logging.info(context.bot_data.setdefault('user_id', set()))

    def broadcast(self,photos,video):
        message = 'Hello from subscription'
        for user_id in self.dp.bot_data['user_id']:
            logging.info(user_id)
            self.dp.bot.send_message(chat_id=user_id, text=message)

            for photo in photos:
                self.dp.bot.send_photo(chat_id=user_id, photo=open(photo, 'rb'))
            logging.info('photos sent')

            self.dp.bot.send_video(chat_id=user_id, video=open(video, 'rb'))
            logging.info('video sent')

