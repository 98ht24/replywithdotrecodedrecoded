class StartUpTask:
    def __init__(self, name: str):
        self.name = name

    def run(self, client):  # return false if non destructive
        return False
