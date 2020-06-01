import os

import discord

from autoactions import puslowmode, messagelog
from chattriggers import setsetting, getsetting, addslowmode, onslowmode, helpcmd
from startuptasks import startupmessage, setstatus


class Bot:
    def __init__(self, token, isbotaccount):
        self.token = token
        self.isbotaccount = isbotaccount

        self.startuptasks = []
        self.startuptasks.append(startupmessage.StartUpMessage("Startup Message"))
        self.startuptasks.append(setstatus.BotStatus("set bot status"))

        self.autoactions = []
        self.autoactions.append(puslowmode.PUSlowMode("per user slow mode"))
        self.autoactions.append(messagelog.MessageLog("Message Log"))

        self.chattriggers = []
        # self.chattriggers.append(replywithdot.ReplyWithDot("replywithdot", ["."], self.spamqueue))
        self.chattriggers.append(setsetting.SetSetting("setsetting", ["*set "]))
        self.chattriggers.append(getsetting.GetSetting("getsetting", ["*get "]))
        self.chattriggers.append(addslowmode.AddSlowMode("add slow mode", ["*addslowmode ", "*asm "]))
        self.chattriggers.append(onslowmode.OnSlowMode("On slow Mode", ["*onslowmode", "*osm"]))
        self.chattriggers.append(helpcmd.HelpCMD("Help Command", ["*help"]))

    def run(self):
        startuptasks = self.startuptasks
        autoactions = self.autoactions
        chattriggers = self.chattriggers

        class Client(discord.Client):

            async def on_ready(self):  # on ready
                for i in startuptasks:
                    self.loop.create_task(i.run(client))

            async def on_message(self, message):  # on message

                if str(message.guild.id) == os.environ.get("EXCLUSIONSERVER"):
                    return

                # await message.channel.trigger_typing()

                # print(str(message.author) + " in " + str(message.channel) + " in " + str(message.guild) + ": " + message.content)  # prints messages in console
                # print("a")
                for i in autoactions:
                    # print("for i in autoactions")
                    # if await i.run(message, client):
                    #	return
                    # print(i.name)
                    # await i.run(message, client)
                    self.loop.create_task(i.run(message, client))

                for i in chattriggers:
                    for j in i.triggers:
                        if message.content.startswith(j):
                            await i.run(message, j, client)

        self.client = Client()
        client = self.client

#	client.run(self.token, bot = self.isbotaccount)
