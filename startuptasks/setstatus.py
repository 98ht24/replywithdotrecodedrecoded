import discord

import startuptask


class BotStatus(startuptask.StartUpTask):

    async def run(self, client):
        await client.change_presence(activity=discord.Activity(name="*help", type=0))
