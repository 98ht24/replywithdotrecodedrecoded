import asyncio
import time

import autoaction
# import os
from persistentstorage.persstorage import PersistentStorage


class PUSlowMode(autoaction.AutoAction):

    async def run(self, message, client):
        # print("triggered!!!!")
        persstorage = PersistentStorage(client)
        try:
            mutedroleid = int(await persstorage.getdata(message.guild.id, "mutedroleid"))
        except:
            mutedroleid = None

        sml = await persstorage.getdata(message.guild.id, "slowmodelist")

        if sml is None:
            await persstorage.setdata(message.guild.id, "slowmodelist", ".0,0")
            return

        # print(sml)
        sml = sml.split(".")[1:]  # oh
        smla = []

        smt = await persstorage.getdata(message.guild.id, "slowmodetiming")

        if smt is None:
            await persstorage.setdata(message.guild.id, "slowmodetiming",
                                      ".0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0")
            return

        smt = smt.split(".")[1:]

        # print(sml) # <- debugging stuff
        # print(smt)

        for i in sml:  # makes int oone array
            # print("i: " + i)
            # print(i.split(","))
            # print(smt)
            smla.append(i.split(","))

        # print(smla) # EVERYUTHING COMBINES

        for ic, i in enumerate(smla):
            # print(i)
            if i is None:  # avoid errors? not sure if to deprecate
                continue
            # print(i[0])
            # print(message.author)
            if message.author.id == int(i[0]):  # check if user is in slowmodelist
                # if str(message.author.id) in i # im retarded
                # print(True)
                currenttime = int(time.time())
                try:  # if there is previous message time
                    # print (smt[ic])
                    # print (ic)
                    # print (smt)
                    lasttime = int(smt[ic])
                # print(currenttime)
                # print(lasttime)
                except:  # if there isnt previous message time
                    towrite = ""
                    for jc, j in enumerate(smt):
                        if jc == ic:
                            towrite += str(currenttime) + "."
                        else:
                            towrite += smt[jc] + "."
                    # print(towrite)
                    towrite = towrite[:-1]
                    # print(51)

                    # await persstorage.setdata(message.guild.id, "slowmodetiming", towrite) # fix?

                    return False

                if currenttime - lasttime >= int(i[1]):  # check if message delay has passed
                    towrite = ""
                    for jc, j in enumerate(smt):
                        if jc == ic:
                            towrite += str(currenttime) + "."
                        else:
                            towrite += smt[jc] + "."
                    towrite = towrite[:-1]
                    towrite = "." + towrite
                    await persstorage.setdata(message.guild.id, "slowmodetiming", towrite)  # update lastmessagetime
                    # print(62) # for debugging

                    await message.author.add_roles(message.guild.get_role(mutedroleid))

                    await asyncio.sleep(int(i[1]))

                    await message.author.remove_roles(message.guild.get_role(mutedroleid))
                    return False

                else:  # deprecated, shouldnt ever be triggered due to the muted role
                    try:
                        await message.delete()  # enforce slowmode
                    except:  # if bot is in server in which it doesnt have perms (example: direct messages)
                        # print("failed to delete")
                        return False
                    # print(67)
                    return True
    # print(False)

# print("do something")
