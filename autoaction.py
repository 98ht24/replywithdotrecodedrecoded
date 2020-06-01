from spamqueue import SpamQueue

class AutoAction:
	def __init__(self, name: str, spamqueue: SpamQueue = None):
		self.name = name
		self.spamqueue = spamqueue
	
	def run(self, message, client): # return false if non destructive
		return False
	