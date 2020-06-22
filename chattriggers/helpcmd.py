import discord

import chattrigger


class HelpCMD(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):
        await message.channel.send('''
```Help Command (a bit wip)

Per-User Slowmode
*asm @target [slowmode seconds timer] (adds slowmode to a user)
*osm (shows the users on slowmode)

Server Modification
*deletecategory [category id] (deletes all the channels in a category and the category itself)
```
''')
