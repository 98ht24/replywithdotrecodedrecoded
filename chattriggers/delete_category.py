import discord

import chattrigger


class DeleteCategory(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):
        if not message.author.guild_permissions.manage_channels:
            await message.channel.send(
                "You do not have the permissions to execute this command. The manage_channels permission is required.")
            return

        args = message.content.split(" ")
        # type value
        category_id = int(args[1])

        category = message.guild.get_channel(category_id)

        for iter_channel in category.channels:
            await iter_channel.delete()

        await category.delete()

        await message.channel.send("Done")
