# Markovito Bot
A Telegram Bot for groups that generates random messages using Markov chain using group members chat history.
It only uses messages that users sent to the group where the bot is being used.

Powered by Markovify (https://github.com/jsvine/markovify), Telethon (https://github.com/LonamiWebs/Telethon) and the Telegram Bot API (https://core.telegram.org/bots/api)

## Starting up
In order to run the service, first install all three dependencies:
```
pip3 install markovify
pip3 install telethon
pip3 install python-telegram-bot
```

Then simply run `python3 markovito.py` to start the bot up.