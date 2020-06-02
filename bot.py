import os

import discord

from autoactions import puslowmode, messagelog
from chattriggers import setsetting, getsetting, addslowmode, onslowmode, helpcmd, listguilds
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
        self.chattriggers.append(listguilds.ListGuilds("List Guilds", ["*listguilds", "*lg"], owneronly=True))
        # ^ We don't want random users finding out what guilds the bot is in. ^

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

                for i in autoactions:
                    self.loop.create_task(i.run(message, client))

                for i in chattriggers:
                    for ii in i.triggers:
                        if message.content.startswith(ii):
                            if not i.owneronly:
                                await i.run(message, ii, client)
                            elif message.author.id:  # Some Commands should only be accessible by the owner
                                if str(message.author.id) == os.environ.get("OWNER_ID"):
                                    await i.run(message, ii, client)

        # noinspection PyAttributeOutsideInit
        self.client = Client()
        client = self.client

#	client.run(self.token, bot = self.isbotaccount)
