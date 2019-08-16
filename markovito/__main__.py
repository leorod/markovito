from markovito.bot import Bot
from markovito.event.randomfact_handler import RandomFactHandler
from markovito.event.quediria_handler import QueDiriaHandler
import json

def get_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    config = get_config()
    handlers = {
        "randomfact": RandomFactHandler(),
        "quediria": QueDiriaHandler()
    }
    bot = Bot(config["bot_token"], handlers)
    bot.start()