import io
import os

import discord

import autoaction


class MessageLog(autoaction.AutoAction):

    async def run(self, message, client):
        # print("loggingtriggered")
        excludedchannels = [int(x) for x in os.environ.get("CHATLOG_EXCLUSION").split(",")]
        if message.channel.id in excludedchannels: return  # some channels you dont want to log to avoid lag
        # try:
        # print(f"{str(message.author)} in {str(message.channel)} in {str(message.guild)}: {message.content}")
        embed = discord.Embed(title=f"{str(message.author)} in {str(message.channel)} in {str(message.guild)}",
                              description=f"{message.content}")

        # dmchannel
        if message.guild is None:
            # embed.set_footer(text = f'''v2
            # messageid,authorid,channelid,guildid,senttimeutc
            # {message.id}
            # {message.author.id}
            # {message.channel.id}
            # DMChannel
            # {message.created_at}''')

            embed.set_footer(
                text=f'''v2.compact|messageid,authorid,channelid,guildid,senttimeutc|{message.id},{message.author.id},{message.channel.id},DMChannel,{message.created_at}''')  # v2.compact 2020-05-18
        else:  # not dmchannel
            #			embed.set_footer(text = f'''v2
            # messageid,authorid,channelid,guildid,senttimeutc
            # {message.id}
            # {message.author.id}
            # {message.channel.id}
            # {message.guild.id}
            # {message.created_at}''') # v2 messageid,authorid,channelid,guildid,senttimeutc
            embed.set_footer(
                text=f'''v2.compact|messageid,authorid,channelid,guildid,senttimeutc|{message.id},{message.author.id},{message.channel.id},{message.guild.id},{message.created_at}''')  # v2.compact 2020-05-18
        if len(message.attachments) > 0:  # 2020-02-28 now adds support for recording images
            # embed.set_image(url = message.attachments[0].url)
            # 2020-03-28 now adds support for archiving images, so that the image is kept even when the original message is deleted
            attachment = message.attachments[0]
            # print(type(attachment))
            # print(dir(attachment))
            attachmentfile = await attachment.read()
            imagemessage = await client.get_channel(int(os.environ.get("IMGLOGCHANNELID"))).send(
                file=discord.File(io.BytesIO(attachmentfile), filename=attachment.filename))
            embed.set_image(url=imagemessage.attachments[0].url)

        await client.get_channel(int(os.environ.get("MSG_LOG_CHANNEL_ID"))).send(embed=embed)
# except: passt
