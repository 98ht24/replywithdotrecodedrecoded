import discord

import chattrigger


class ListGuilds(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):

        tosend = ", ".join([
            f"{str(x)} ({x.id})" for x in client.guilds
        ])

        await message.channel.send(tosend)
