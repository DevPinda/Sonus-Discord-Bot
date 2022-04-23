import os
import discord
import youtube_dl
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv('dotenv.env')
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="p!", intents = intents)


@bot.event
async def on_ready():
    print("Bot online successfully!")

@bot.event
async def on_message(message):
    if message.content == "test":
        await message.channel.send("Test: testing successful!")
    elif message.content == "p!play":
        await message.channel.send("'p!play' command requires an argument [ p!play (YouTube URL) ]")
    elif message.content == "hello":
        await message.channel.send("Hello!")
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    message = await ctx.send("Ping is: ")
    await message.edit(content = f"Ping is:  {round(bot.latency*1000,2)} ms !")

@bot.command()
async def play(ctx, url : str):
    song_file = "song.mp3"
    song = os.path.isfile(song_file)

    try:
        if song:
            os.remove(song_file)
    except PermissionError:
        await ctx.send("Error: Stop the currently playing song using the 'stop' command") 
        return


    channel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, song_file)
    voice.play(discord.FFmpegPCMAudio(song_file))


@bot.command()
async def quit(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()
    await ctx.send("Bot quit the channel successfuly!")

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await voice.pause()
        await ctx.send("Bot paused successfully!")
    else:
        await ctx.send("Error: Bot isn't currently playing anything!")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await voice.resume()
        await ctx.send("Bot resumed successfully!")
    else:
        await ctx.send("Error: Bot isn't currently paused!")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await voice.stop()
    else:
        await ctx.send("Error: Bot isn't currently playing anything!")


bot.run(TOKEN)