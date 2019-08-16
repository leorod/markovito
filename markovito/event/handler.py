from abc import ABC, abstractmethod
import logging
log = logging.getLogger(__name__)

class Handler(ABC):
    def handle(self, bot, update):
        try:
            log.info("Command received: %s", update.message.text)
            log.debug("Received message: %s", update)
            message = self.get_message(bot, update)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        except Exception as e:
            bot.send_message(chat_id=update.message.chat_id, 
                text="Something went wrong. Please try again or see usage with /help")
            log.exception(e)
    
    @abstractmethod
    def get_message(self, bot, update):
        """pass"""