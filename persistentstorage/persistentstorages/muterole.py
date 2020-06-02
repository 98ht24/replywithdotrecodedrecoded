import discord


class MuteRole:

    def __init__(self, guild: discord.Guild):
        self.guild = guild

    async def getrole(self) -> discord.Role:
        for i in self.guild.roles:
            if i.name == "Muted":
                return i

        pass

    async def createmutedrole(self) -> discord.Role:
        self.guild.create_role("")
