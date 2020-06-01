import chattrigger

import discord

class Template(chattrigger.ChatTrigger):
	
	async def run(self, message: discord.Message, trigger: str, client: discord.Client):
		return False