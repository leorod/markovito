from .handler import Handler
from ..data.markov_generator import generate_message
from ..data.telegram_scraper import TelegramScraper
import asyncio
import re

class QueDiriaHandler(Handler):
    def __init__(self, config):
        self.telegram_scraper = TelegramScraper(config)
    
    def extract_mention(self, message):
        mention = list(filter(lambda ent: ent.type == 'mention', message.entities))[0]
        text = message.text[mention.offset:mention.offset + mention.length]
        return re.sub('^@', '', text)

    async def get_mentioned_user(self, message):
        mentions = list(filter(lambda ent: ent.type == 'text_mention', message.entities))
        if len(mentions) > 0:
            return mentions[0].user.id
        else:
            return await self.telegram_scraper.get_user_id(self.extract_mention(message))
    
    async def build_message(self, update):
        chat_id = str(update.message.chat.id).replace('-', '')
        user_id = await self.get_mentioned_user(update.message)
        return generate_message(chat_id + '/' + str(user_id))
    
    def get_message(self, bot, update):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(self.build_message(update))