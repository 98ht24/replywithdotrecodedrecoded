import startuptask
import discord

class BotStatus(startuptask.StartUpTask):

	async def run(self, client):
		await client.change_presence(activity = discord.Activity(name = "help comamnd isnt implemented yet ;", type = 0))