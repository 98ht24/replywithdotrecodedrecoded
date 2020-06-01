import os

import startuptask


class StartUpMessage(startuptask.StartUpTask):

    async def run(self, client):
        logchannelid = int(os.environ.get("LOG_CHANNEL"))
        # logchannel = client.get_channel(logchannelid)
        # await logchannel.send("Started! Running in " + str(len(client.guilds)) + " guilds with " + str(len(client.users)) + " users.")
        logchannel = client.get_channel(logchannelid)
        await logchannel.send(
            "Started! Running in " + str(len(client.guilds)) + " guilds with " + str(len(client.users)) + " users.")
        print("startupmessage triggered")
