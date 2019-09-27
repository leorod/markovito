from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import json
import asyncio

class TelegramScraper:
    def __init__(self, config):
        self.config = config
    
    async def get_user_id(self, username):
        async with TelegramClient(self.config['session_name'], self.config['api_id'], self.config['api_hash'], loop=asyncio.get_event_loop()) as client:
            await client.connect()
            if not await client.is_user_authorized():
                client.send_code_request(self.config['phone'])
                client.sign_in(self.config["phone"], input('Enter the code: '))
            response = await client.get_entity(username)
            return response.id