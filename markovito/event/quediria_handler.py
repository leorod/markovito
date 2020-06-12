from .handler import Handler
from ..data.markov_generator import generate_message
from ..data.user_resolver import UserResolver
from ..data.chat_resolver import ChatResolver
import asyncio
import re

class QueDiriaHandler(Handler):
    def __init__(self):
        self.user_resolver = UserResolver(asyncio.new_event_loop())
        self.chat_resolver = ChatResolver()
    
    def extract_mention(self, message):
        mention = list(filter(lambda ent: ent.type == 'mention', message.entities))[0]
        text = message.text[mention.offset:mention.offset + mention.length]
        return re.sub('^@', '', text)

    def get_mentioned_user(self, message):
        mentions = list(filter(lambda ent: ent.type == 'text_mention', message.entities))
        if len(mentions) > 0:
            return mentions[0].user.id
        else:
            return self.user_resolver.get_user_id(self.extract_mention(message))
    
    def build_message(self, update):
        chat_id = self.chat_resolver.get_chat_id(update.message.chat.id, update.message.chat.title)
        user_id = self.get_mentioned_user(update.message)
        print('chataidi', chat_id)
        return generate_message(str(chat_id) + '/' + str(user_id))
    
    def get_message(self, bot, update):
        return self.build_message(update)