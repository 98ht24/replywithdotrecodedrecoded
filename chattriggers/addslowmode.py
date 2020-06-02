import discord

import chattrigger
from persistentstorage.persstorage import PersistentStorage


class AddSlowMode(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):
        # tag Time

        if not message.author.guild_permissions.administrator:
            await message.channel.send(
                "You do not have the permissions to execute this command. The administrator permission is required.")
            return

        args = message.content.split(" ")

        if not len(args) == 3:
            await message.channel.send("Invalid Syntax! The proper syntax is ,asm [@user] [Slow mode seconds]!")
            return

        target_user = message.mentions[0]

        per_storage = PersistentStorage(client)

        await per_storage.append_data(message.guild.id, "slowmodelist", f".{str(target_user.id)},{args[2]}")
        await message.channel.send("Done.")
