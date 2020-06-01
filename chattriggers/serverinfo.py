import discord

import chattrigger


class ServerInfo(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):
        return False
