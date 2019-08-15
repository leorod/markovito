from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import requests
import re
import json
import markov_generator
import group_scraper
import asyncio
import logging
import random

def extract_mention(message):
    mention = list(filter(lambda ent: ent.type == 'mention', message.entities))[0]
    text = message.text[mention.offset:mention.offset + mention.length]
    return re.sub('^@', '', text)

async def get_mentioned_user(message):
    mentions = list(filter(lambda ent: ent.type == 'text_mention', message.entities))
    if len(mentions) > 0:
        return mentions[0].user.id
    else:
        return await group_scraper.get_user_id(extract_mention(message))

async def send_message(bot, update):
    try:
        print(update.message)
        chat_id = str(update.message.chat.id).replace('-', '')
        user_id = await get_mentioned_user(update.message)
        message = markov_generator.generate_message(chat_id + '/' + str(user_id))
        bot.send_message(chat_id=update.message.chat_id, text=message)
    except FileNotFoundError as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text="Something went wrong. Couldn't load dataset.")
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text=str(e))

def handle(bot, update):
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(send_message(bot, update))
    except Exception as e:
        print(e)

def random_fact(bot, update):
    try:
        response = requests.get('http://mentalfloss.com/api/facts?page=' + str(random.randint(0, 10)) + '&limit=1')
        facts = list(map(lambda x: x['fact'], response.json()))
        message = markov_generator.generate_from_iterable(facts)
        bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text=str(e))

def main():
    try:
        with open('config/bot.json', 'r') as f:
            updater = Updater(json.load(f)['token'])
        dp = updater.dispatcher
        dp.add_handler(CommandHandler('quediria', handle))
        dp.add_handler(CommandHandler('randomfact', random_fact))
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()