import discord


class SlowModeObject:

    def __init__(self, target: discord.Member, slowmodetime: int, mutedrole: discord.Role):
        self.target = target
        self.slowmodetime = slowmodetime
        self.mutedrole = mutedrole
