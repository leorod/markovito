from telegram.ext import Updater, CommandHandler
import json
import logging
log = logging.getLogger(__name__)

class Bot:
    def __init__(self, token, handlers):
        updater = Updater(token)
        dp = updater.dispatcher
        for command, handler in handlers.items():
            dp.add_handler(CommandHandler(command, handler.handle))
        self.updater = updater
    
    def start(self):
        log.info("Listening...")
        self.updater.start_polling()
        self.updater.idle()