# Please don't edit directly on this file
# Copy the code then edit it in VS Code or your Test Bot
# Everytime you edit, please inform others on discord


import os
import time
import discord
from web_server import keep_alive
from replit import db
# Client instance

client = discord.Client(intents=discord.Intents.all())

# register event for callbacks
# Callbacks are function called when something else happens
# events are kind of triggers in Discord
# async is used for multitasking
# await -> prior to finish this
@client.event
async def on_ready():
    print("{0.user} - created by group of friends".format(client))


@client.event
async def on_voice_state_update(member, before, after):
    user_id = str(member.id)

    # If user enter voice room
    if before.channel is None and after.channel is not None:
        join_time = round(time.time())

        # if user already in database -> update join time
        if user_id in db.keys():
            db[user_id]["join_time"] = join_time
        # create a new user if not find
        else:
            db[user_id] = {"join_time": join_time, "total_study_time": 0}
    else:
        leave_time = round(time.time())
        study_time = leave_time - \
                     db[user_id]["join_time"] + db[user_id]["total_study_time"]
        db[user_id]["total_study_time"] = study_time


@client.event
async def on_message(message):
    # Check if the message is sent by the bot
    if message.author == client.user:
        return

    # Command symbol
    if message.content.startswith('$hello'):
        await message.channel.send('Lo cc')

    # Load data
    if message.content.startswith('$study'):
        user_id = str(message.author.id)
        if user_id in db.keys():
            study_time = db[user_id]["total_study_time"]
            await message.channel.send(
                f"<@{user_id}>'s study time is: {study_time} seconds")
        else:
            await message.channel.send('No data found!')

    #Reset data
    if message.content.startswith('$rreset'):
        user_id = str(message.author.id)
        await message.channel.send(f"Deleting <@{user_id}>'s study reccord")
        if user_id in db.keys():
            del db[user_id]
        await message.channel.send('Deleted!')

# Connect with web server
keep_alive()

# Hide TOKEN for privacy
client.run(os.environ['TOKEN'])
