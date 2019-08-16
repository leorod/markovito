from .handler import Handler
from ..data.markov_generator import generate_message
from ..data.group_scraper import get_user_id
import asyncio
import re

class QueDiriaHandler(Handler):
    def __init__(self):
        pass
    
    def extract_mention(self, message):
        mention = list(filter(lambda ent: ent.type == 'mention', message.entities))[0]
        text = message.text[mention.offset:mention.offset + mention.length]
        return re.sub('^@', '', text)

    async def get_mentioned_user(self, message):
        mentions = list(filter(lambda ent: ent.type == 'text_mention', message.entities))
        if len(mentions) > 0:
            return mentions[0].user.id
        else:
            return await get_user_id(self.extract_mention(message))
    
    async def build_message(self, bot, update):
        try:
            chat_id = str(update.message.chat.id).replace('-', '')
            user_id = await self.get_mentioned_user(update.message)
            message = generate_message(chat_id + '/' + str(user_id))
            bot.send_message(chat_id=update.message.chat_id, text=message)
        except FileNotFoundError as e:
            bot.send_message(chat_id=update.message.chat_id, text="Something went wrong. Couldn't load dataset.")
        except Exception as e:
            bot.send_message(chat_id=update.message.chat_id, text=str(e))
    
    def handle(self, bot, update):
        try:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.build_message(bot, update))
        except Exception as e:
            bot.send_message(chat_id=update.message.chat_id, text=str(e))