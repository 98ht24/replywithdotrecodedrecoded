
#from itertools import count

#import discord

import os

class SpamQueue:

	#import SimpleMessage

	def __init__(self):
		self.tosend = []
		#print("asdadad")
		self.davidcount = 0
		
		self.spamchannelid = int(os.environ.get("SPAM_CHANNEL_ID"))
	
	#def addclient(self, client: discord.Client):
	#	self.client = client
	#	self.spamchannel = client.get_channel(self.spamchannelid)
	
	def addtoqueue(self, toadd):
		self.tosend.append(toadd)
	
	def addtostartofqueue(self, toadd):
		self.tosend.insert(0, toadd)

	def queue(self):
		#print("hi")
		while 1:
			if len(self.tosend) > 0:
				yield self.tosend.pop(0)
			else:
				yield self.defaultspam()

	def defaultspam(self):
		#print("hixdelol")
		self.davidcount += 1
		return SimpleMessage(self.spamchannelid, f"david has {self.davidcount - 1} bowling balls")


class SimpleMessage:
	def __init__(self, channelid: int, content: str):
		self.channelid = channelid
		self.content = content