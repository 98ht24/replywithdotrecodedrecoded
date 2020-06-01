import autoaction

import os

import discord

from spamqueue import SimpleMessage

class TagResponse(autoaction.AutoAction):

	async def run(self, message: discord.Message, client: discord.Client):
		#print("TAGRESPONSE")
		#guildid = int(os.environ.get("THE_GUILD"))
		#guild = client.get_guild(guildid)
		#guildme = guild.me.mention
		# ^ super old code that is shit

		#guildme = 
		
		guildme = f"<@!{message.guild.me.id}>"
		#print(guildme)
		if not guildme in message.content:
			return
		
		#stub