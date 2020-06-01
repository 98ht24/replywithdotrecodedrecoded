from spamqueue import SpamQueue


class ChatTrigger:  # base class for when someone say something bot say something else
    def __init__(self, name: str, triggers: list, spamqueue: SpamQueue = None):
        self.name = name
        self.triggers = [i.casefold() for i in triggers]  # so that links work
        self.spamqueue = spamqueue

    def run(self, message, trigger, client):
        message.channel.send("default")

    def get_name(self):
        return self.name
