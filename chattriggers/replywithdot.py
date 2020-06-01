import discord

import chattrigger


class ReplyWithDot(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):
        await message.channel.send(".")
