import chattrigger

import discord

from persistentstorage.persstorage import PersistentStorage

class OnSlowMode(chattrigger.ChatTrigger):
	
	async def run(self, message: discord.Message, trigger: str, client: discord.Client):
		
		persstorage = PersistentStorage(client)

		returned = await persstorage.getdata(message.guild.id, "slowmodelist")

		smlist = returned.split(".")[1:]
		print(smlist)
		print(smlist)
		userslist = [x.split(",")[0] for x in smlist]
		timelist = [x.split(",")[1] for x in smlist]
		print(userslist)
		print(timelist)

		memberslist = [message.guild.get_member(int(x)) for x in userslist]

		#combined = [f"{str(x)}, {y}" for x in memberslist for y in timelist]
		combined = ""
		for x, y in zip(memberslist, timelist):
			print(x, y)
			combined += f"{str(x)}, {y} | "

		#combinedstr = " | ".join(combined)

		await message.channel.send(combined)