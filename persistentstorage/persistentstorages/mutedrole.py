import discord

from objects.errors import BotMissingPermissionsError


class MutedRole:

    def __init__(self, guild: discord.Guild):
        self.guild = guild

    async def get_role(self) -> discord.Role:
        for i in self.guild.roles:
            if i.name == "Muted":
                return i

        return await self.create_muted_role()

    async def create_muted_role(self) -> discord.Role:
        try:
            muted_role = await self.guild.create_role("Muted")
        except discord.Forbidden:
            raise BotMissingPermissionsError(f"manage_roles")

        for i in self.guild.text_channels:
            try:
                i.set_permissions(muted_role, send_messages=False)
            except discord.Forbidden:
                raise BotMissingPermissionsError("manage_roles")
