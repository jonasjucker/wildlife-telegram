import logging
import socket
import time
from exchange import set_bot_action

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    PicklePersistence,
    CallbackContext,
)




class WildBot:

    def __init__(self,token,offline=False):

        if not offline:
            # Create the Updater and pass it your bot's token.
            persistence = PicklePersistence(filename='backup/bot.pkl')
            self.updater = Updater(token, persistence=persistence)

            self.dp = self.updater.dispatcher
            self.dp.add_handler(CommandHandler('start',self._start))
            self.dp.add_handler(CommandHandler('subscribe',self._subscribe))
            self.dp.add_handler(CommandHandler('unsubscribe',self._unsubscribe))
            self.dp.add_handler(CommandHandler('test',self._test))
            self.dp.add_handler(CommandHandler('motion_control',self._motion_control))
            self.dp.add_handler(CommandHandler('bot_shutdown',self._bot_shutdown))
            self.dp.add_handler(CommandHandler('shutdown',self._shutdown))
            self.dp.add_handler(CommandHandler('where_am_I',self._get_ip_address))
            self.dp.add_handler(CommandHandler('summary',self._summary))

            # start the bot
            self.updater.start_polling()

        self.user_wants_shutdown = False
        self.user_wants_test = False
        self.is_sensible_to_motion = False
        self.user_wants_bot_shutdown = False
        self.already_down = False
        self.is_offline_for_failover = offline
        self.user_wants_event_summary = False

        # flag to mark that bot could not be connected and
        # a failover instance is used
        # based on this flag a restart is triggered
        self.has_no_connection = offline


    def _change_motion_sensibility(self):
        
        self.is_sensible_to_motion = not self.is_sensible_to_motion

    def stop(self):
        self.updater.stop()
        self.already_down = True

    def _start(self,update: Update, context: CallbackContext):
        reply_text = "Hi! I am LonelyCam. If you want to subscribe write /subscribe. \
                      Write /unsubscribe to no longer receive cute pics"

        reply_keyboard = [
            ['/subscribe', '/unsubscribe'],
            ['/motion_control', '/test'],
            ['/bot_shutdown', '/shutdown'],
            ['/where_am_I','/summary'],
        ]

        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

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

    def _test(self,update: Update, context: CallbackContext):
        reply_text = "Test LonelyCam! Please wait..."
        update.message.reply_text(reply_text)

        self.user_wants_test = True
        set_bot_action(True)
        user_id = update.effective_user.id
        logging.info(f'user: {user_id} scheduled test')
    
    def _motion_control(self,update: Update, context: CallbackContext):
        reply_text = "Modify motions sensitivity of LonelyCam"
        update.message.reply_text(reply_text)

        self._change_motion_sensibility()
        set_bot_action(True)
        user_id = update.effective_user.id
        logging.info(f'user: {user_id} changed motion sensibility')

    def _bot_shutdown(self,update: Update, context: CallbackContext):
        reply_text = "You are about to shut down the bot of LonelyCam."
        update.message.reply_text(reply_text)

        self.user_wants_bot_shutdown = True
        set_bot_action(True)
        user_id = update.effective_user.id
        logging.info(f'user: {user_id} scheduled bot-shutdown')

    def _shutdown(self,update: Update, context: CallbackContext):
        reply_text = "You are about to shut down LonelyCam."
        update.message.reply_text(reply_text)

        self.user_wants_shutdown = True
        set_bot_action(True)
        user_id = update.effective_user.id
        logging.info(f'user: {user_id} scheduled shutdown')

    def _get_ip_address(self,update: Update, context: CallbackContext):
        ip_address = '';
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip_address = s.getsockname()[0]
        s.close()

        reply_text = f"IP-ADDRESS: {ip_address}"
        update.message.reply_text(reply_text)

        set_bot_action(True)

    def _connection_error(self,error):
        logging.warning(f'Bot connection lost: {error}')
        self.has_no_connection = True

    def _summary(self,update: Update, context: CallbackContext):
        reply_text = "Collecting summary of events"
        update.message.reply_text(reply_text)

        self.user_wants_event_summary = True
        set_bot_action(True)
        user_id = update.effective_user.id
        logging.info(f'user: {user_id} requested summary of events')


    def broadcast(self,photos,videos,message='Hello from subscription'):
        if self.is_offline_for_failover:
            logging.info('Bot not connected -> skip bot.broadcast')
        else:
            for user_id in self.dp.bot_data['user_id']:
                logging.info(user_id)
                try:
                    self.dp.bot.send_message(chat_id=user_id, text=message)
                except Exception as e:
                    self._connection_error(e)
                    return

                if photos:
                    try:
                        for photo in photos:
                            self.dp.bot.send_photo(chat_id=user_id, photo=open(photo, 'rb'))
                    except Exception as e:
                        self._connection_error(e)
                        return
                    logging.info('photos sent')

                if videos:
                    try:
                        for video in videos:
                            self.dp.bot.send_video(chat_id=user_id, video=open(video, 'rb'))
                    except Exception as e:
                        self._connection_error(e)
                        return
                    logging.info('videos sent')


