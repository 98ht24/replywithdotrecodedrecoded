import discord

import os

class PersistentStorage:

	def __init__(self, client: discord.Client):
		self.client = client
		self.hostservid = int(os.environ.get("HOSTSERVID"))
		self.hostserv = client.get_guild(self.hostservid)
	
	async def setdata(self, servid: int, datatype: str, data: str):
		
		for category, channels in self.hostserv.by_category():
			
			if not category.name == str(servid): # checks if category is for server
				continue
			
			for channel in channels: # goes through the channels if category is for server
				if not channel.name == datatype:
					continue
				await channel.send(data) # updates data
				return
			# assume channel for datatype doesnt exist
			newchannel = await category.create_text_channel(datatype)
			await newchannel.send(data)
			return
		# at this point we assume that there is no textchannel or category

		newcategory = await self.hostserv.create_category(str(servid))
		newchannel = await newcategory.create_text_channel(datatype)
		#so it creates both
		await newchannel.send(data)
		#dont forget to update data
		return
	
	async def getdata(self, servid: int, datatype: str):

		for category, channels in self.hostserv.by_category():
			if not category.name == str(servid):
				continue
			
			for channel in channels:
				if not channel.name == datatype:
					continue
				return (await channel.history(limit = 1).flatten())[0].content
		
		return None # cant find
	
	async def appenddata(self, servid: int, datatype: str, data: str):

		for category, channels in self.hostserv.by_category():
			
			if not category.name == str(servid): # checks if category is for server
				continue
			
			for channel in channels: # goes through the channels if category is for server
				if not channel.name == datatype:
					continue
				#await channel.send(data) # updates data
				prevdata = await self.getdata(servid, datatype)
				await channel.send(prevdata + data)
				return
			# assume channel for datatype doesnt exist
			newchannel = await category.create_text_channel(datatype)
			await newchannel.send(data)
			#prevdata = await self.getdata(servid, datatype)
			#await channel.send(prevdata + data)
			return
		# at this point we assume that there is no textchannel or category

		newcategory = await self.hostserv.create_category(str(servid))
		newchannel = await newcategory.create_text_channel(datatype)
		#so it creates both
		await newchannel.send(data)
		#prevdata = await self.getdata(servid, datatype)
		#await newchannel.send(prevdata + data)
		#dont forget to update data
		return
