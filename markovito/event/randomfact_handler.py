from .handler import Handler
from ..data.markov_generator import generate_from_iterable
import requests

class RandomFactHandler(Handler):
    def __init__(self):
        self.source = 'http://mentalfloss.com/api/facts'

    def get_message(self, bot, update):
        response = requests.get(self.source)
        facts = list(map(lambda x: x['fact'], response.json()))
        return generate_from_iterable(facts)