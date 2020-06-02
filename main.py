import logging

logging.basicConfig()

import keepalive

keepalive.keep_alive()

import bot

# from threading import Thread

import os

tokens = []
tokens.append(os.getenv("TOKEN"))

bots = []

import asyncio

for i in tokens:
    bots.append(bot.Bot(i, True))
    print("Added bot")

for i in bots:
    i.run()

loop = asyncio.get_event_loop()

for i in bots:
    loop.create_task(i.client.start(i.token, bot=i.is_bot_account))

loop.run_forever()
print("Done starting bots!")
