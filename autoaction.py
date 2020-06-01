class AutoAction:
    def __init__(self, name: str):
        self.name = name

    def run(self, message, client):  # return false if non destructive
        return False
