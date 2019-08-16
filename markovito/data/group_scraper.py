from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import json
import asyncio

with open('config/config.json', 'r') as f:
    api_config = json.load(f)

async def get_user_id(username):
    async with TelegramClient(api_config['session_name'], api_config['api_id'], api_config['api_hash'], loop=asyncio.get_event_loop()) as client:
        await client.connect()
        if not await client.is_user_authorized():
            client.send_code_request(api_config['phone'])
            client.sign_in(api_config["phone"], input('Enter the code: '))
        response = await client.get_entity(username)
        return response.id