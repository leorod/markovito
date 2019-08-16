from telegram.ext import Updater, CommandHandler
import json

class Bot:
    def __init__(self, token, handlers):
        updater = Updater(token)
        dp = updater.dispatcher
        for command, handler in handlers.items():
            dp.add_handler(CommandHandler(command, handler.handle))
        self.updater = updater
    
    def start(self):
        self.updater.start_polling()
        self.updater.idle()