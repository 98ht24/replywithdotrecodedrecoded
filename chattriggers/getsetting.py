import discord

import chattrigger
from persistentstorage.persstorage import PersistentStorage


class GetSetting(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):
        if not message.author.guild_permissions.administrator:
            await message.channel.send(
                "You do not have the permissions to execute this command. The administrator permission is required.")
            return

        args = message.content.split(" ")
        # type value
        print(args)
        if not len(args) == 2:
            await message.channel.send("Invalid Syntax! The proper syntax is ,get [name]!")
            return
        perstorage = PersistentStorage(client)
        # await perstorage.set_data(message.guild.id, args[1], args[2])
        returned = await perstorage.get_data(message.guild.id, args[1])
        await message.channel.send(f"Value is {returned}")
