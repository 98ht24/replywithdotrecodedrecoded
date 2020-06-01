from spamqueue import SpamQueue


class StartUpTask:
    def __init__(self, name: str, spamqueue: SpamQueue = None):
        self.name = name
        self.spamqueue = spamqueue

    def run(self, client):  # return false if non destructive
        return False
