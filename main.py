import asyncio
import datetime
import os
import time
import discord

from discord.ext.commands.context import Context
import requests
from databaseHandle import Database
from tiktokHandle import TikTokHandle
from discord.ext import commands, tasks
from discord.ext.commands.errors import CommandNotFound
from discord import app_commands
from dotenv import load_dotenv
from Streamable import StreamableHandle
from pystreamable.exceptions import StreamableApiServerException
load_dotenv()



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

token = os.environ.get("TOKEN")
DBclient = os.environ.get("CLIENT")
embedURL = os.environ.get("embedURL")
username = None
userid = None
channelID = None
Streamable = bool("True")
ch = int(os.environ.get("ArchiveCH"))
msg = ""

db = Database()

        
@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

    global username, channelID, msg

    username = db.getUsername()
    channelID = db.getChannel()
    loop = db.getloop()
    uploadOption()

    if username != "" and channelID != "" and loop == True:
        newVideos.start()

    msg = db.getMessage()
    if (msg == ""):
        msg = "New TikTok video: "

    else:
        print("Username: " + username)
        print("Channel ID: " + str(channelID))



@bot.command()
async def add(ctx: Context, left: int, right: int):
    """Adds two numbers together."""
    await ctx.reply(left + right)

@bot.hybrid_command(description = "Set user to follow.", aliases = ['su', 'adduser'])
@commands.has_permissions(administrator = True)
@app_commands.describe(user="Username")
async def setuser(ctx: Context, user:str):
    global username
    username = user
    exist = db.getUserID(username)
    if exist == False:
        await ctx.reply("We currently do not support this user.")
        return
    db.setUsername(username)
    print("Username: " + username)
    await ctx.reply(f"Added {user}", ephemeral=False) # Change ephemeral to True if you want only the author to see that message
@setuser.error
async def setuser_error(ctx: Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have permission to do that", ephemeral=True)
    else:
        await ctx.reply("An error occured", ephemeral=True)

@bot.hybrid_command(description = "Set channel to send notification.", aliases=['sc', 'addchannel'])
@commands.has_permissions(administrator = True)
@app_commands.describe(channelid="Channel")
async def setchannel(ctx: Context, channelid: str):
    global channelID
    # channelID = channelid
    if (channelID == None):
        channelID = ctx.channel.id
    # elif ctx.message.channel_mentions:
    #     channelID = str(ctx.message.channel_mentions[0].id)
    elif channelid != "":
        # check if channel exists
        channel = bot.get_channel(int(channelid))
        if channel == None:
            await ctx.reply("Please enter a valid channel", ephemeral=True)
            return
        channelID = channelid
    else:
        print(ctx.message.channel_mentions)
        await ctx.reply("Please enter a valid channel", ephemeral=True)
        return

    db.setChannel(channelID)

    channel = bot.get_channel(int(channelID))
    await ctx.reply(f"Set channel to {channel.mention}", ephemeral=True)
@setchannel.error
async def setchannel_error(ctx: Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have permission to do that", ephemeral=True)
    else:
        await ctx.reply("An error occured", ephemeral=True)

@bot.hybrid_command(description = "Set default message.", aliases = ['sm'])
@commands.has_permissions(administrator = True)
@app_commands.describe(message="Message")
async def setmessage(ctx: Context, message:str):
    global msg
    msg = message
    db.setMessage(message)
    await ctx.reply(f"Added `{message}` as content when new video is posted", ephemeral=False) # Change ephemeral to True if you want only the author to see that message
@setmessage.error
async def setmessage_error(ctx: Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have permission to do that", ephemeral=True)
    else:
        await ctx.reply("An error occured", ephemeral=True)

@bot.hybrid_command(description = "View current stalked user.", aliases=['ul', 'users'])
async def userlist(ctx: Context):
    users = db.getUsername()
    await ctx.reply(f"The poor girl being stalked is: {users}", ephemeral=False)

@bot.event
async def on_command_error(ctx: Context, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not found", ephemeral=True)
    raise error

# https://www.tiktok.com/@hakosbaelz_holoen/video/7100729819205340418

@bot.hybrid_command(description = "Start stalking.", aliases=['s'])
@commands.has_permissions(administrator = True)
async def start(ctx: Context):
    db.setloop(True)
    if newVideos.is_running():
        await ctx.reply("Already running", ephemeral=True)
    else:
        newVideos.start()
        await ctx.reply("Started", ephemeral=True)
@start.error
async def start_error(ctx: Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have permission to do that", ephemeral=True)
    else:
        print(error)
        await ctx.reply("Something went wrong", ephemeral=True)

@bot.hybrid_command(description = "Stop stalking.", aliases=['st'])
@commands.has_permissions(administrator = True)
async def stop(ctx: Context):
    db.setloop(False)
    #cancel loop
    if newVideos.is_running():
        newVideos.cancel()
        # Cancel immediately
        # newVideos.stop()
        await ctx.reply("Stopped", ephemeral=True)
    else:
        await ctx.reply("Loop is not running", ephemeral=True)
@stop.error
async def stop_error(ctx: Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have permission to do that", ephemeral=True)
    else:
        print(error)
        await ctx.reply("Something went wrong", ephemeral=True)


@tasks.loop(hours=24)
async def newVideos():
    global msg, ch, username, userid, Streamable

    tiktok = TikTokHandle(db, username, userid=userid)
    c = tiktok.sortVideos()
    if (c):
        for video in tiktok.newVideos:
            id = video['video_id']
            v = db.getVideo(username, id)
            createTime = v["createTime"]

            url = None

            if Streamable == False:
                url = await DiscordfileHandle(id)
            else:
                url = await uploadToStreamable(id)
            
            if url == False:
                originurl = f'https://www.tiktok.com/@{username}/video/{id}'
                await bot.get_channel(int(channelID)).send(f"{msg} at <t:{createTime}:f> \n {originurl}")
                db.updateVideoURL(username, id, url)
                return
            db.updateVideoURL(username, id, url)
            url = f"{embedURL}/video/{username}/{id}"

            # Ping the server before sending the url (send request to the url)
            r = requests.get(url)
            if r.status_code == 200:
                # If the request is successful, send the url
                print("Sending url")

            await asyncio.sleep(5)
            await bot.get_channel(int(channelID)).send(f"{msg} at <t:{createTime}:f> \n {url}")

@newVideos.before_loop
async def before():
    # Wait until 8am JST to start the loop
    # Get current utc time
    utc = datetime.datetime.utcnow()
    # Convert to JST
    jst = utc + datetime.timedelta(hours=9)
    # Get the hour
    hour = jst.hour
    # If it's not 8am, wait
    if hour != 8:

        # If it's after 8am, wait until 8am tomorrow
        if hour > 8:
            # create datetime object for 8am tomorrow
            tomorrow = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.time(6, 5))
            # Get the difference between now and 8am tomorrow
            diff = tomorrow - datetime.datetime.now()

            # Seconds to hours and minutes

            print(f"Waiting {(24 - hour + 8)} hours (appx {diff.seconds}s) to start the loop [Epoch {today.timestamp()}]")

            # await asyncio.sleep((24 - hour + 8) * 3600)
            await asyncio.sleep(diff.seconds)
        else:
            
            # create datetime object for 8am today
            today = datetime.datetime.combine(datetime.date.today(), datetime.time(6, 5))

            # Get the difference between now and 8am today
            diff = today - datetime.datetime.now()

            # datetime to epoch
            print(today.utctimetuple())

            print(f"Waiting {(8 - hour)} hours (appx {diff.seconds}s) to start the loop [Epoch {today.timestamp()}]")
            # await asyncio.sleep((8 - hour) * 3600)
            await asyncio.sleep(diff.seconds)

    await bot.wait_until_ready()

def uploadOption():
    """
    Are are two services option to upload to.
    1. Streamable
    2. Discord

    Streamable requires you to pass username and password
    Default will upload to discord (will get error if file exceed 8MB)

    """
    global Streamable
    if os.environ.get("UPLOAD_OPTION") == "DISCORD":
        Streamable = False
    elif os.environ.get("UPLOAD_OPTION") == "STREAMABLE":
        Streamable = True
    else:
        Streamable = False
    return Streamable
    
async def DiscordfileHandle(file):
    """
    File handle for uploading to discord.
    Eiter return file url or None if file is too large
    """
    size = os.path.getsize(f"{file}.mp4") 
    if size > 1048576 * 8:
        print("File is too big")
        # If file is too large, upload to streamable
        print("Try uploading to streamable")
        url = await uploadToStreamable(file)
        return url
        # return False
    else:
        url = await uploadToDiscord(file)
        return url

async def uploadToStreamable(file):
    username = os.environ.get("STREAMABLE_USERNAME")
    password = os.environ.get("STREAMABLE_PASSWORD")
    try:
        api = StreamableHandle(username, password)
        video = api.upload(f"{file}.mp4", file)
        url = await api.getVideoUrl(video)
        return url
    except StreamableApiServerException:
        print("Invalid credentials")
        return False
    except Exception as e:
        print("uploadToStreamable - [ERROR]:", e)
        return False

async def uploadToDiscord(file):
    """
        Uploads file to discord.
        return message attachment object
    """
    try:
        m = await bot.get_channel(ch).send(file = discord.File(f"{file}.mp4"))
        return m.attachments[0].url
    except Exception as e:
        print("uploadToDiscord - [ERROR]:", e)
        return False

@bot.command()
@commands.is_owner()
async def upload(ctx: Context, id):
    try:
        await ctx.send(file = discord.File(f"{id}.mp4"))
    except Exception as e:
        await ctx.send("Error: " + str(e))

@bot.command()
@commands.is_owner()
async def sync(ctx: Context):
    bot.tree.copy_global_to(guild=ctx.guild)
    await bot.tree.sync(guild=ctx.guild)
    await ctx.send("Synced!", ephemeral=True)

@bot.command()
@commands.is_owner()
async def clear(ctx: Context):
    db.clearDB()
    await ctx.send("Cleared", ephemeral=True)

@bot.command()
@commands.is_owner()
async def scan(ctx: Context):
    try:
        tiktok = TikTokHandle(db, username, userid=userid)
        c = tiktok.sortVideos()
        if (c):
            newVideoMsg = ""
            for video in tiktok.newVideos:
                id = video['video_id']
                v = db.getVideo(username, id)
                createTime = v["createTime"]
                newVideoMsg += f"{msg} at <t:{createTime}:f> \n https://www.tiktok.com/@{username}/video/{id}\n"

            await ctx.reply(newVideoMsg, ephemeral=True)

    except Exception as e:
        await ctx.reply("Error: " + str(e))

@bot.command()
@commands.is_owner()
async def forcerun(ctx: Context):
    # Run task without waiting for 8am JST
    try:
        global username, userid, channelID, msg, Streamable
        tiktok = TikTokHandle(db, username, userid=userid)
        c = tiktok.sortVideos()
        if (c):
            for video in tiktok.newVideos:
                id = video['video_id']
                v = db.getVideo(username, id)
                createTime = v["createTime"]

                url = None

                if Streamable == False:
                    url = await DiscordfileHandle(id)
                else:
                    url = await uploadToStreamable(id)
                
                if url == False:
                    originurl = f'https://www.tiktok.com/@{username}/video/{id}'
                    await bot.get_channel(int(channelID)).send(f"{msg} at <t:{createTime}:f> \n {originurl}")
                    db.updateVideoURL(username, id, url)
                    return
                db.updateVideoURL(username, id, url)
                url = f"{embedURL}/video/{username}/{id}"
                await asyncio.sleep(10)
                await bot.get_channel(int(channelID)).send(f"{msg} at <t:{createTime}:f> \n {url}")
    except Exception as e:
        await ctx.reply("Error: " + str(e), ephemeral=True)

@bot.command()
@commands.is_owner()
async def info(ctx: Context):
    # reply info about the current loop
    global username, userid, channelID, msg, Streamable
    embed = discord.Embed(title="Stalk Info", color=0x00ff00)
    embed.add_field(name="Username", value=username, inline=True)
    embed.add_field(name="User ID", value=userid, inline=True)
    # embed.add_field(name="\u200b", value="\u200b", inline=False)

    try:
        channel = bot.get_channel(channelID)
        embed.add_field(name="Channel ID", value=f"{channel.mention} ({channel.name})", inline=True)
    except Exception as e:
        print(f"[info] Channel not found: {e}")
        embed.add_field(name="Channel ID", value=f"{channelID} (Channel not found)", inline=True)

    embed.add_field(name="Message", value=msg, inline=True)
    
    embed.add_field(name="Upload Option", value=Streamable, inline=True)
    embed.add_field(name="Loop Status", value=newVideos.is_running(), inline=True)

    await ctx.reply(embed=embed, ephemeral=True)

@info.error
async def info_error(ctx: Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("Only owner or admin can use this command", ephemeral=True)


bot.run(os.environ.get("TOKEN"))
