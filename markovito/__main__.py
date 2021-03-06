from markovito.bot import Bot
from markovito.event.randomfact_handler import RandomFactHandler
from markovito.event.quediria_handler import QueDiriaHandler
import json
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.DEBUG)
log = logging.getLogger(__name__)

def get_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    log.info("Starting up...")
    config = get_config()
    handlers = {
        "randomfact": RandomFactHandler(),
        "quediria": QueDiriaHandler()
    }
    bot = Bot(config["bot_token"], handlers)
    bot.start()