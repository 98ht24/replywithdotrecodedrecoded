import os

import discord


class PersistentStorage:

    def __init__(self, client: discord.Client):
        self.client = client
        # noinspection SpellCheckingInspection
        self.host_guild_id = int(os.environ.get("HOSTSERVID"))
        self.host_guild = client.get_guild(self.host_guild_id)

    async def set_data(self, servid: int, datatype: str, data: str):

        for category, channels in self.host_guild.by_category():

            if not category.name == str(servid):  # checks if category is for server
                continue

            for channel in channels:  # goes through the channels if category is for server
                if not channel.name == datatype:
                    continue
                await channel.send(data)  # updates data
                return
            # assume channel for datatype doesnt exist
            new_channel = await category.create_text_channel(datatype)
            await new_channel.send(data)
            return
        # at this point we assume that there is no textchannel or category

        new_category = await self.host_guild.create_category(str(servid))
        new_channel = await new_category.create_text_channel(datatype)
        # so it creates both
        await new_channel.send(data)
        # don't forget to update data
        return

    async def get_data(self, servid: int, datatype: str):

        for category, channels in self.host_guild.by_category():
            if not category.name == str(servid):
                continue

            for channel in channels:
                if not channel.name == datatype:
                    continue
                return (await channel.history(limit=1).flatten())[0].content

        return None  # cant find

    async def append_data(self, servid: int, datatype: str, data: str):

        for category, channels in self.host_guild.by_category():

            if not category.name == str(servid):  # checks if category is for server
                continue

            for channel in channels:  # goes through the channels if category is for server
                if not channel.name == datatype:
                    continue
                # await channel.send(data) # updates data
                previous_data = await self.get_data(servid, datatype)
                await channel.send(previous_data + data)
                return
            # assume channel for datatype doesnt exist
            new_channel = await category.create_text_channel(datatype)
            await new_channel.send(data)
            # previous_data = await self.get_data(servid, datatype)
            # await channel.send(previous_data + data)
            return
        # at this point we assume that there is no textchannel or category

        new_category = await self.host_guild.create_category(str(servid))
        new_channel = await new_category.create_text_channel(datatype)
        # so it creates both
        await new_channel.send(data)
        # previous_data = await self.get_data(servid, datatype)
        # await new_channel.send(previous_data + data)
        # don't forget to update data
        return
