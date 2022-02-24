import discord, asyncio
import server
from discord.ext import commands
from discord.ext.commands import Bot
import os


token = os.getenv("TOKEN")
prefix = ">"


padString = "only to notice that they've got a massive padlock on their wallet! You didn't bring your bolt cutters with you, and ended up getting caught by the police, losing"
landString = "placed a landmine in their wallet. It exploded when you opened it, blowing up in your face and killing you instantly."

global dankID
dankID = 270904126974590976

global safeChannel
safeChannel = int(os.getenv("SAFE_CHANNEL"))

global IsLogging
IsLogging = True

People = [int(os.getenv("USER_1")), int(os.getenv("USER_2"))]


help_command = commands.DefaultHelpCommand(
    no_category = 'Management'
)
description = "Dank Memer Anti-Rob Bot"

bot = commands.Bot(
    command_prefix = prefix,
    description = description,
    help_command = help_command,
    case_insensitive = True,
    strip_after_prefix = True,
    user_bot = True
    )


@bot.event
async def on_connect():
    os.system("cls")
    print(f"Running Anti-Rob bot on:\n{bot.user}\n\n{bot.user.id}")


@bot.command(
    name="startLogging",
    description="Starts logging for rob messages",
    aliases=["startL"]
    )
async def startLogging(ctx):
    global IsLogging
    if IsLogging == True:
        return
    
    else:
        IsLogging = True
        await ctx.send("Started logging for rob messages")


@bot.command(
    name="stopLogging",
    description="Stops logging for rob messages",
    aliases=["stopL"]
    )
async def stopLogging(ctx):
    global IsLogging
    if IsLogging == False:
        return
    
    else:
        IsLogging = False
        await ctx.send("Stopped logging rob messages")


@bot.command(
    name="getChannel",
    description="Sends the current safe channel.",
    aliases=["getC", "gChannel", "gC"]
    )
async def getChannel(ctx):
    global safeChannel
    try:
        current = bot.get_channel(int(safeChannel))
    except Exception as err:
        await ctx.send(f"There was an error fetching the safe channel: {err}")
        return
    current = bot.get_channel(safeChannel)
    await ctx.send(f"Current safe channel: #{current.name} - {current.id} - <#{current.id}>")


@bot.command(
    hidden=True,
    name="logout",
    description="Logs out of the bot. (Stops it)",
    aliases=["stop", "out", "close"],
    )
async def logout(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    await bot.close()
    print("Logged out.")
    



@bot.event
async def on_message(message):
    global safeChannel
    global dankID
    
    if IsLogging == False:
        if message.author.id in People:
            await bot.process_commands(message)
            
        return
    
    msgIsReply = message.reference
    if padString in message.content:
        
        if msgIsReply is not None:
            msgReply = await message.channel.fetch_message(message.reference.message_id)
            
            if msgReply.author == bot.user:
                return
            
            else:
                if message.author.id == dankID and "pls rob" in msgReply.content.lower():
                    print(f"Someone tried to rob you (but failed). \n{msgReply.author} in {msgReply.guild.name} at #{msgReply.channel.name}")
                    channel = bot.get_channel(safeChannel)
                    
                    await channel.send("pls use pad")
                    print(f"Used padlock at #{channel.name}")
                    await asyncio.sleep(5)
                    print(f"Used landmine at #{channel.name}\n\n")
                    await channel.send("pls use land")
                    
    elif landString in message.content:
        if msgIsReply is not None:
            msgReply = await message.channel.fetch_message(message.reference.message_id)
            
        if msgReply.author == bot.user:
            return
            
        else:
            if message.author.id == dankID and "pls rob" in msgReply.content.lower():
                print(f"Someone tried to rob you (but died). \n{msgReply.author} in {msgReply.guild.name} at #{msgReply.channel.name}")
                channel = bot.get_channel(safeChannel)
                    
                print(f"Used landmine at #{channel.name}\n\n")
                await channel.send("pls use land")
    
    if message.author.id in People:
        await bot.process_commands(message)
        return

server.keep_alive()
bot.run(token)
