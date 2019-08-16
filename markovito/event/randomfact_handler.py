from .handler import Handler
from ..data.markov_generator import generate_from_iterable
import requests

class RandomFactHandler(Handler):
    def __init__(self):
        self.source = 'http://mentalfloss.com/api/facts'

    def handle(self, bot, update):
        try:
            response = requests.get(self.source)
            facts = list(map(lambda x: x['fact'], response.json()))
            message = generate_from_iterable(facts)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        except Exception as e:
            bot.send_message(chat_id=update.message.chat_id, text=str(e))