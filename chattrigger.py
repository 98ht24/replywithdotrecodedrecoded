class ChatTrigger:  # base class for when someone say something bot say something else
    def __init__(self, name: str, triggers: list, owneronly: bool = False):
        self.name = name
        self.triggers = [i.casefold() for i in triggers]  # so that links work
        self.owneronly = owneronly

    def run(self, message, trigger, client):
        pass

    def get_name(self):
        return self.name
