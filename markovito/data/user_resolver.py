from telethon import TelegramClient
import json
import asyncio

with open('config/config.json', 'r') as f:
    api_config = json.load(f)

class UserResolver:
    def __init__(self, loop):
        self.loop = loop
        self.client = TelegramClient(api_config['session_name'], api_config['api_id'], api_config['api_hash'], loop=loop)
        self.started = False
    
    def _sync(self, coroutine):
        if self.loop.is_running():
            return coroutine
        else:
            return self.loop.run_until_complete(coroutine)
    
    async def startup(self):
        await self.client.start(bot_token=api_config['bot_token'])

    def get_user_id(self, username):
        if not self.started:
            self._sync(self.startup())
        response = self._sync(self.client.get_entity(username))
        return response.id